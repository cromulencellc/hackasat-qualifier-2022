from sys import byteorder
import bitstream 
import json


class FpgaResetError(Exception):
    # An exception for reseting the fpga!
    pass

class FPGA:
    # This class acts as a model of a "custom" FPGA that 
    # does not match any FPGA on the market.
    # This FPGA is vulnerable to startbleed.
    # If something invalid occurs in configuration this class
    # will raise FPGA reset error
    def __init__(self , flag , sock):
        # Setup a dictionary of configuration registers - set them all to zero
        self.config_reg = dict()
        for key in bitstream.registers.keys():
            self.config_reg[key] = 0
        # Call the FPGA reset function
        self.reset() 
        # Save the flag and the socket we want to communicate with
        self.flag = flag
        self.sock = sock
        pass
    # This function implmenents the FPGAs fallback capbility
    # which is supposed to protect you from attacks like starbleed
    # However there is an intentional bug in here to mimic starbleed
    def reset( self ):
        print("FPGA re-booting", flush=True)
        # Set mode
        self.mode = None 
        # Fabric is fine again
        self.fabric_corrupted = False 
        self.commands = { "no-op":0 }
        # make sure the truncated flag is empty
        self.flag_truncated = ""
        # no data in memory
        self.memory = bytearray( b'' ) 
        for key,val in  bitstream.registers.items():
            # The fallback pattern of a starbleed vulnerable
            # FPGA doesnt reset all registers on reset 
            if key in bitstream.exploitable:
                pass
            else:
                # for non vulnerable registers this must be reset
                self.config_reg[key] = 0
    # Load a bitstream file into the FPGA
    def load_bitstream( self ,filename ):
        bs = bitstream.SecureBitstream()
        out = bs.load( filename )
        self.bitstream = out     
        # Validate the HMAC tag
        if( out["calculated-hmac-tag"] != out["hmac-tag"]):
            return False
        return True
    # Run the list of commands that the configuration engine has unpacked
    def run_config_cmds( self ):
        for item in self.bitstream['commands']:
            cmd    = item['action']
            if( cmd == 'write'):
                
                target = item['addr']
                data   = item['data']
                if target == "FABRIC":
                    self.write_fabric( data )
                elif target == "NVMEM":
                    self.write_nvmem( data )
                elif target == "CONFIG":
                    self.write_config( data )
                else:
                    self.write_default( target ,data )
                pass
            elif( cmd == 'read'):
                target = item['addr']
                out = self.config_reg[target].to_bytes(4,byteorder="big")
                self.sock.send( out )
            elif( cmd == 'no-op'):
                # do nothing
                pass
            else:
                print("Corrupted command sent to FPGA configuration engine")
                raise FpgaResetError()
            
    # A helper function for the 'Write to fabric' command
    # This function does two things.
    # - Mark the 'fabric corrupted' flag as true. We dont tell the user how to make their own fabric so if they write anything to the fabric they get messed up
    # - increment the fabric addr counter by however many bytes we write. The user can read this register out to see what position they are at in fabric.
    def write_fabric( self , data ):
        N = len( data )
        self.config_reg["FABRIC"] = data[-4]
        self.config_reg["FABRIC_ADDR"] += N
        self.fabric_corrupted = True
    # A helper function for the 'Write NVMEM' command
    # This function does a few things:
    # - Write the entire payload into our memory variable for later use
    # - Write the last word into the NVMEM register
    # - Increment the NV_ADDR register by the length of the data
    def write_nvmem( self, data): 
        N = len( data )
        self.config_reg["NV_ADDR"] += N
        self.config_reg["NVMEM"] = int.from_bytes( data[-4:], "big") 

        self.memory.extend( data )
    # A default wrtie helper function for all simple registers
    def write_config( self , data ):
        if( data == bitstream.jtag_mode ):
            self.mode = "JTAG"
        elif( data == bitstream.flash_mode ):
            self.mode = "FLASH"
        else:
            print("Invalid configuration mode requested")
            raise FpgaResetError
    def write_default( self , addr , data ):
        self.config_reg[addr] = int.from_bytes( data[-4:], "big")
    # A helper function to take what is in the nvmemory and run it
    # Since this data is expected to be a json file we load up a json text as a dict
    # then we process it 
    def process_nvm_payload( self ):
        # Load the memory as json text
        try:

            json_text = self.memory.decode('utf-8')
            payload_dict = json.loads( json_text )
        except:
            print("NVM payload cant be loaded")
            raise FpgaResetError
        # Go through the json text and process it
        for key,value in payload_dict.items():
            # Theres only one valid command!
            if( key == "print_flag"):
                N = value
                truncated_flag = self.flag[0:N]
                print("Printing {} bytes of the flag:".format(N))
                print( truncated_flag )
            else:
                print("Invalid command {} in NVMEM payload".format(key))
                raise FpgaResetError
    # Main run function for the FPGA
    def run( self , filename ):
        authentic = self.load_bitstream( filename )
        # Run all the decrypted bitstream commands
        self.run_config_cmds()
        # Authenticate the bitstream
        # NOTE: a key component of the starbleed vulnerability is that
        # authentication is done AFTER the commands are actually run
        if( False == authentic ):
            print("Bitstream authentication failed")
            raise FpgaResetError()
        print("Bitstream Authentic", flush=True)
        
        # If we get here:
        # - The bitstream file is authentic
        if( "FLASH" == self.mode ):
            # If the user did anything that corrupts the fabric reset
            if( True == self.fabric_corrupted ):
                print("FPGA Fabric Corrupted")
                raise FpgaResetError
            print("FPGA Fabric Running", flush=True)
            self.process_nvm_payload()
        elif( "JTAG" == self.mode  ):
            print("Invalid FGPA image in fabric")
            raise FpgaResetError
        else:
            print("Invalid configruation mode")
            raise FpgaResetError

if __name__ == "__main__":
    b = FPGA( "flag{testFlagLulz}")
    b.run( "readout.bit")