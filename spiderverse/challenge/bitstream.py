import argparse
import hmac
from sys import byteorder
from Crypto.Cipher import AES
import hashlib
from Crypto import Random
import hmac
import yaml
import math
from dict_helper import get_key
import argparse
import binascii
# Constants and other stuff thats hardcoded
correct_header = "HAS3FABIC-SECURE".encode('utf-8')
correct_footer = "HAS3-TAG--SECURE".encode('utf-8')
hmac_key = "MyV3ryS3c(ur3K3y".encode('utf-8')
aes_pw   = "S3(ur3MyFp6aPlzz".encode('utf-8')
encrypt_command = b"\xc0\xff\xee!"
jtag_mode = b"jtag"
flash_mode = b"file"
commands = {"write":b"\x01" , "read":b"\x10", 'no-op':b"\x11"}
registers = {"CONFIG":1,"FABRIC":2,"NVMEM":3, "STATUS":4,"FABRIC_ADDR":5,"NV_ADDR":6,"RESERVED_1":7,"RESERVED_2":8}
exploitable = ["RESERVED_1" , "RESERVED_2"]
write_only = ["CONFIG","FABRIC","NVMEM"]
# An exception that helps us reset the FPGA if needed
class BitStreamError(Exception):
    pass
class SecureBitstream:
    # A class that is used for creating and loading 'secure' bitstreams
    def __init__(self):
        self.data = dict()
        self.data["print_flag"] = 4 
        # These are in bytes
        self.positions = { "header":0 , "encrypt":16  , "footer":-16}
        self.encrypt = {"key":0 , "commands":16 , "tag":-32 }
        pass
    # A function that will load a FPGA bit file into memory
    def load( self , filename ):
        # Load up the data 
        f = open( filename , 'rb')
        data = f.read()
        f.close()
        # Get header and footer
        header_start = self.positions['header']
        header_end =  self.positions['header'] + 16
        header = data[header_start : header_end]
        footer_start = self.positions['footer']
        footer = data[ footer_start : ]# the footer is at the  end
        # Validate the first and last 16 byte words are header and footer - otherwise bail
        if( header != correct_header ):
            print("Header incorrect in binary")
            raise BitStreamError
        if( footer != correct_footer ):
            print("Footer incorrect in binary")
            raise BitStreamError 

        # THhe first piece of data after the header MUST be the encryption command
        enc_start = self.positions["encrypt"]
        enc_end   = enc_start + len(encrypt_command)
        enc_command = data[ enc_start : enc_end ]
        if( enc_command != encrypt_command ):
            print("Encryption command is incorrect. All bitstreams must be encrypted")
            raise BitStreamError
        
        # Decrypt the data in the bitstream 
        enc_data = data[ enc_end : footer_start ]
        decrypted = self.decrypt_aes( enc_data )
        # Get HMAC key from the decrypted data
        key = decrypted[self.encrypt["key"]:self.encrypt["commands"]]
        # Get HMAC tag from the encrypted data
        tag = decrypted[ self.encrypt["tag"] : ]
        # Calculate the HMAC tag of the encrypted data without the key or the tag
        tag_data_start = self.encrypt["commands"]
        tag_data_end = self.encrypt["tag"]
        calculated_tag = self.gen_tag( decrypted[tag_data_start : tag_data_end ] , key)
        out = dict()
        # Store it all
        out["calculated-hmac-tag"] = calculated_tag
        out["hmac-key"] = decrypted[:self.encrypt["key"]:16]
        out["commands"] = self.unpack_payload( decrypted )
        out["hmac-tag"] = tag
        return out
    # A function that will generate a bitstream file based on a list of commands
    def dump( self , filename , command_list ):
        out = bytearray( b'' )
        data = bytearray( b'')
        # Add header
        out.extend(correct_header) 
        # Add Encryption command
        out.extend(encrypt_command)
        # Add HMAC key
        data.extend( hmac_key )
        # Add plaintext
        payload_plaintext = self.gen_payload(command_list) 
        # pad plaintext with no-ops until we are a multiple of teh aes blocksize
        noops = self.aes_pad_cmd( payload_plaintext )
        payload_plaintext.extend( noops )
        data.extend(payload_plaintext)
        # Add HMAC Tag
        tag = self.gen_tag( bytes(payload_plaintext) , hmac_key )
        data.extend( tag )
        # Encrypt the key,tag,commands
        encrypted = self.encrypt_aes( bytes(data) )
        out.extend( encrypted )
        # Add footer
        out.extend(correct_footer)
        # OK - we did it! now write the file!!!
        f = open(filename,'wb')
        f.write(out)
        f.close()
    # A helper function for AES encryption
    def encrypt_aes( self , data ):
        private_key = hashlib.sha256(aes_pw).digest()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(data)
    # A helper function for AES decryption
    def decrypt_aes( self, ciphertext ):
        private_key = hashlib.sha256(aes_pw).digest()
        iv = ciphertext[:16]
        n_blocks = int( ( len(ciphertext)/ AES.block_size) - 1  ) 
        print("Decrypted {} blocks of plain-text".format(n_blocks) , flush=True )
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return  cipher.decrypt(ciphertext[16:]) 
    # Generate the tag based on data and the key
    def gen_tag( self, data , key ):
        keygen =  hmac.new(key, msg = data , digestmod='sha256')
        tag = keygen.hexdigest()
        tag_binary = binascii.unhexlify( tag )
        return tag_binary
    # End crypto stuff
    
    # Create the binary command list from a yml file of payload commands
    def gen_payload( self , payload_yml ):
        # process the yaml file into a dictionary
        with open( payload_yml , "r") as stream:
            try: 
                d = yaml.safe_load( stream )
            except yaml.YAMLError as exec:
                print(exec)
        # Make an empty byte payload
        payload = bytearray(b'')
        # for each item in the dictionary turn it into a command
        for item in d:
            
            rw =list(item.keys())[0]

            cmds = item[rw]
            addr  = cmds["addr"]
            
            newcmd = bytearray(b'')
            # The read-write command is the first byte
            rw_cmd = commands[rw]
            newcmd.extend( rw_cmd ) 
            # The address byte is next telling us which register to use
            if( rw != "no-op"):
                # No-op is only a 1 byte command
                addr_cmd = registers[addr]
                newcmd.append( addr_cmd )
            # Things get different here depending on if its a read/write/no-o[]
            if( rw == "write"):    
                # If the command is a read calculate the length of the data
                # store it as a 2 byte number
                data = cmds["data"]
                L = len(data)
                len_bytes = L.to_bytes(2,byteorder='big')
                newcmd.extend( len_bytes )
                # Then append however many bytes of data
                newcmd.extend( data.encode('utf-8') )
            else:
                # If the command is a read or a noop its only 2 bytes long
                pass
            payload.extend( newcmd )
        return payload
    # This function helps unpack the binary command data into a dictionary of 
    # commands that we can properly iterate over
    def unpack_payload( self , data_bytes ):
        # Format is 
        keep_going = True 
        # Start after the HMAC key
        idx = self.encrypt["commands"]
        out = dict()
        N = len(data_bytes) + self.encrypt["tag"]
        out = []
        # Loop over all the data
        while(keep_going):
            cmd = dict()
            # find the read write byte and turn it into a text based action
            rw = data_bytes[idx]
            key = rw.to_bytes(1,byteorder="big")
            action = get_key( commands , key )
            cmd["action"] = action
            idx += 1 
            
            if( action in commands):
                # If the action is valid process it
                if( action != 'no-op'):
                    # Get the address 
                    addr = data_bytes[idx]
                    cmd["addr"] = get_key( registers , addr )
                    idx += 1 
                    if( action == "write"):
                        length = int.from_bytes( data_bytes[idx:idx+2] , byteorder="big")
                        if( length <= 0 ):
                            print("Writes must be positive in length")
                            raise BitStreamError 
                        idx += 2
                        # the next length bytes are data!
                        data = data_bytes[idx:idx+length]
                        idx += length
                        cmd["length"] = length
                        cmd["data"] = data
                else: 
                    # Noop commands are 1 byte
                    pass 
            else: 
                cmd["action"] = "invalid"
                #print("Invalid command in bitstream")
                # If the action isnt a valid action get mad and reset
                #raise BitStreamError
            if( idx < N ):
                keep_going = True
            else:
                keep_going = False
            out.append( cmd )
            
        return out
    
    # A helper function that will pad text with no-ops up to the aes blocksize
    def aes_pad_cmd( self , text_to_pad ):
        N = len( text_to_pad )
        N_blocks =  math.ceil( N/ AES.block_size)
        pad_bytes = N_blocks*AES.block_size - N 

        pad_cmd = commands['no-op']
        out = bytearray(b'')
        for k in range( pad_bytes ):
            out.extend( pad_cmd )
        return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create and manage bitstream files')
    parser.add_argument('--input-file', dest='commands', help='A yml file containing the commands you want to run', required=True)
    parser.add_argument('--output', dest='output',help='Filename of binary file', required=True)
    args = vars(parser.parse_args())
    b = SecureBitstream()
    b.dump( args["output"], args["commands"])
    #i = SecureBitstream() 
    #o = i.load( "out.bit")
    #f = open("out.yml","wt")
    #f.write( yaml.dump( o ) ) 
    #f.close()