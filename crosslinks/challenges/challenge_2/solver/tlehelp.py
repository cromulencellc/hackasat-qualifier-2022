

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

def getStartTime( filename , satellite):
    return 0