def make_databit_file( filename , n_1 , n_2 , flag):
    text1 = "HackASat\n"
    text2 = "{}\n".format(flag)
    f = open( filename , "wb")
    text1_out = text1 * n_1 
    text2_out = text2 * n_2
    f.write( text1_out.encode('utf-8'))
    f.write( text2_out.encode('utf-8'))
    f.close()
    print("The flag begins at byte: {}".format( len(text1_out)))

