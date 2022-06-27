import subprocess 
import pwn
import os
import hashlib
import glob
import argparse
def handle_ticket( io ):
    ticket = os.getenv("TICKET")
    if( ticket == None):
        return
    io.recvuntil("Ticket please:")
    io.send( ticket + "\n")


def verify_hashlist( listFile, imageFolder ):
    print("Verifying hashlist")
    # Get the images and get the hashes from them
    imageHashes = dict()
    files = glob.glob("{}/*.jpg".format(imageFolder)) 
    for file in files:
        filename = os.path.basename( file )
        print("Handling: {}".format( filename ))
        steg_filename = "./work/" + filename.replace(".jpg", ".txt")
        
        write_hash = "steghide extract -f -q -p '' -sf {} -xf {}".format( file,  steg_filename)
        proc = subprocess.Popen( write_hash , shell=True)
        proc.wait()
        f = open( steg_filename , "rt")
        hash = f.read().strip("\n")
        if( filename != "oahu.jpg"):
            imageHashes[ filename  ] = hash

    # Get the hashlist that we think matches the images
    f = open(listFile, 'rt')
    lines = f.readlines()
    passcodes = dict()
    for line in lines:
        v = line.split(",")
        hash = v[0]
        code = v[1].strip("\n")
        passcodes[hash] = code + "\n" 
    # Verify the images have all the hashes
    for name,imageHash in imageHashes.items():
        solved = imageHash in passcodes.keys()
        if( solved == False ):
            print( "Missing: {} {}".format( imageHash , name  ))
            print("Update your hashlist")
            raise ValueError
        else:
            print("{} Verified".format(name))
    print("Your hash list is up to date")
    return passcodes
def create_image_hashes( imageFolder ):
    images = dict()
    print("Image Files")
    print("-----------")
    files = glob.glob("{}/*.jpg".format(imageFolder)) 
    for file in files:
        filename = os.path.basename( file )
        f = open(file , 'rb')
        data = f.read()
        f.close()
        sha_val = hashlib.sha256(data).hexdigest()
        print("{} {}".format( filename , sha_val ))
        images[sha_val] = filename
    return images    
def main(host,port , images ):
    passcodes = verify_hashlist( "hashlist.txt" , images )
    image_shas = create_image_hashes( images )
    sock = pwn.remote(host,port)
    handle_ticket(sock)
    # Wait till we get the prompt
    msg = sock.recvuntil(b">")
    print(msg)
    #
    sock.send(b"PLAYBACK_FILE\n")

    # solve 5 times
    for k in range(0,5):
        image = sock.recvuntil(b"?")
        image = image.strip(b'\n')
        image = image.strip(b"?")
        image = image.decode('utf-8')
        print( "Challenge requested: {}".format( image ) )
        imageFile = image_shas[image]
        print("Getting md5 for {}".format(imageFile))
        f = open( "work/"+ imageFile.replace("jpg","txt") )
        md5 = f.read().strip("\n")
        f.close
        passcode = passcodes[ md5 ]
        print("Sending: {}".format(passcode))
        sock.send(passcode.encode('utf-8'))
        sock.recvuntil("Thank you\n")
    msg = sock.recv(1024).decode("utf-8")
    print(msg)
        


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--images', default="../images")
    args = parser.parse_args()
    host = os.getenv("CHAL_HOST", "localhost")
    port = int( os.getenv("CHAL_PORT",12345) ) 
    main( host,port , args.images)
