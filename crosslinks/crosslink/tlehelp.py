

def available(  filename ):
    
        tleFile  = open(filename , "rt")
        lines = tleFile.readlines()

        # 
        available = []
        for line in lines:
            if (line[0] != "1" ) and (line[0] != "2") :
                #this means its a name
                
                sat = line.replace("\n","")
                sat = sat.rstrip()
                available.append( sat )
                #print("{} is in the database".format(sat))
        tleFile.close()
        return( available )

def print_sats( filename , sats ):
    tleFile  = open(filename , "rt")
    lines = tleFile.readlines()

    for sat in sats:
        
        for line, ind in zip( lines , range(len(lines))):
            
            if( True == line.startswith(sat) ):
                startInd = ind
        ###
        for ind in range( startInd, startInd + 3):
            print( lines[ind].replace("\n", "") )