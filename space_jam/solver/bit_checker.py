import bitstring


def find_offset( file , find_text , debug=False):
    f = open(file,"rb")
    bits= bitstring.Bits(f)

    bits_array = bitstring.BitArray( bits )
    
    for k in range(8):
        skip =8*15 
        start = k + skip 
        N = start  + (int( (len(bits_array)-start)/8 ) * 8 )
        x = bits_array[start:N ]
        
        byte_data = x.bytes

        try:
            if( True == debug ):
                print("offset {}".format(k), flush=True)
                print(byte_data.decode('utf-8'), flush=True)            
            if( find_text in byte_data.decode('utf-8')):
                print("Found what you wanted at offset: {}".format(k), flush=True)
                print(byte_data.decode('utf-8'), flush=True)
                return 
        except:
            #print("Not ascii at offset {}".format(k) ) 

            pass
    print("No flag found - sorry bro", flush=True)
if __name__ == "__main__":
    find_offset("decoded.txt", "flag", True)