import xxtea
import base64


import struct

def crack_keys( key_file,   filename ):
    expected_key_length = 16
    
    print("Trying to crack {}".format( filename ))
    f = open( filename , "rb")
    enc_data = f.read()
    f.close()
    f =  open(key_file , "rb")
    key_data = f.read()
    f.close
    n_data = len(enc_data)
    n_key = len(key_data)
    missing_bytes = (expected_key_length) - n_key
    broken_key = key_data
    cypher_text = enc_data
    print("We expect {} bytes but we got {} - {} missing".format(expected_key_length,n_key, missing_bytes))
    print("The following key is broken: {}".format( broken_key ))
    print("Insrting x00 and brute forcing remaining keys")
    print("Cyphertext is: {} bytes".format(  cypher_text))
    tries = pow( 2 , 8*missing_bytes )
    #tries = 1 
    k = 0
    
    keep_going =True
    while( True == keep_going):
        key = broken_key + k.to_bytes(missing_bytes,byteorder="big")
        decrypted    = xxtea.decrypt( cypher_text , key ,padding=False)
        #print(key)
        L = struct.unpack('i', decrypted[64:68])[0]
        if( L==64 ):
            print("Key bruteforced")
            print(key)        
            keep_going = False
        k = k + 1
        if( k >= tries ):
            print("All tries tried")
            keep_going = False
    f2 = open('decrypted.bin','wb')
    f2.write( decrypted )
    f2.close()
    hmac_key = base64.b64decode(decrypted[:32])
    lon = struct.unpack( 'd' , decrypted[56:64])[0]
    period = struct.unpack( 'd' , decrypted[40:48])[0]
    lat = struct.unpack( 'd' , decrypted[48:56])[0]

    print("Period: {}".format(period) )
    print("Latitude: {}".format(lat))
    print("Longitude: {}".format(lon))
    print("HMAC Key: {}".format(hmac_key))
    output = dict()
    output["hmac_key"] = (hmac_key).decode('utf-8')
    output["lat"] = lat
    output["lon"] = lon
    output["period"] = period
    return output

if __name__ == "__main__":
    crack_keys( "../authy.bin" )