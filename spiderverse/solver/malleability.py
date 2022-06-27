from functools import partial
from multiprocessing.sharedctypes import Value
from Crypto.Cipher import AES

def byte_xor( b1 , b2):
    arr = []
    for a,b in zip(bytearray(b1),bytearray(b2)):
        v = a^b
        arr.append(v)

    return  arr 
def text_to_block( text ,blocksize ):
    blocks = []

    for k in range( 0, len(text) , blocksize ):
    
        block = text[k:k+blocksize]
        blocks.append( block )
    return blocks



class ExploitError(Exception):
    pass

class CbcEncryptExploit:
    def __init__( self , desired ):
        self.desired = desired 
        
        self.prev = "Arbitrary-Cipher"
        pass
    def attack( self  ,known ,encrypted ):
        desired = self.desired[-16:]
        self.desired = self.desired[:-16]# pop off the last block
        if( AES.block_size != len(desired) ):
            print("Desired text must be AES.block_size")
            raise ExploitError
        Po = known
        Ci_m1 = encrypted
        Xi = byte_xor( Ci_m1 , Po )
        Cm_new = byte_xor( Xi , desired )
        return bytes(Cm_new)
class CbcDecrypExploit:
    def __init__( self , encrypted_bytes ):
        self.blocks = text_to_block( encrypted_bytes , AES.block_size )
    def num_blocks( self ):
        return len(self.blocks)
    def encryption_attack( self , known_cyphertext,  desired_plaintext , known_plaintext ):      
        Ci_m1 = known_cyphertext
        Pi = known_plaintext
        Pi_new = desired_plaintext 
        Cnew_m1 = byte_xor( Pi * Ci_m1 * Pi_new)
        return Cnew_m1
    def decryption_attack(self , attack_start  , known_plaintext ,  malicious_plaintext ):
        #
        # Make a copy of the cipher text for us to mess with
        pwnt = self.blocks
        # Setup the knowns
        Mi = malicious_plaintext
        Pi = known_plaintext
        # Find which block we need to be in
        n = int(attack_start/AES.block_size)
        block_start = attack_start-  n*AES.block_size
        block_end =  block_start + len( known_plaintext )
        # Validate all the numbers are ok
        if len(Mi) > AES.block_size:
            print("Malicious text too big")
            raise ExploitError
        if len( Pi ) != len(Mi):
            print("Malicious and Known Plaintext must be equal length")
            raise ExploitError
        if ( block_start > 16 ) or ( block_end > 16):
            print("Attack start {} Attack end {}".format( block_start , block_end))
            print("Exploit must occur within a single block")
            raise ExploitError
        Ci_m1  = pwnt[n-1]
        # Just manipulate the bytes we care about
        partial_cypher = Ci_m1[block_start:block_end]
        # Create the known value before encryption
        Xi = byte_xor( partial_cypher , Pi)
        # Calculate the new cipher value
        partial_new_cypher = byte_xor( Xi , Mi )
        NewCypher = bytearray(Ci_m1)
        NewCypher[block_start:block_end]= partial_new_cypher
        pwnt[n-1] = NewCypher
        out = bytearray( b"".join(pwnt) ) 
        return out











