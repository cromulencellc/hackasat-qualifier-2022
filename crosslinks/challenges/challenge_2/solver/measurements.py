import datetime
def gettime(input):
    timeFormat=  """%Y-%m-%dT%H:%M:%S.%f"""

    return datetime.datetime.strptime( input , timeFormat ) 
def unpack(filename):
    data = dict()
    f = open(filename , "rt")
    lines = f.readlines()
    first =  True
    for line in lines:
        if "Observations" in line:
            
            satellite = line.replace("Observations ","")
            satellite = satellite.replace("\n","")
            # its the start of a new set 
            data[satellite] = dict()
            s = data[satellite]
            s["ranges"] = []
            s["rates"] =[]
            s["times"] = []
            first = False
        elif( "Pseudorange" in line ):
            # its a label line do nothing 
            pass
        else:
            if first:
                print( "Bad line: {}".format( line ))
                raise("Wtf mate ^^")
            #its an existing set
            lineMod = line.replace("\n","")
            lineMod = lineMod.strip()
            o =  lineMod.split(",")
            s = data[satellite]
            s["ranges"].append( float(o[1])) 
            s["rates"].append( float( o[2]))
            timeFormat=  """%Y-%m-%dT%H:%M:%S.%f%z"""

            s["times"].append( datetime.datetime.strptime( o[0] , timeFormat ) ) 
    f.close() 
    return data
