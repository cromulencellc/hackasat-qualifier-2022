import argparse
import skyfield.api as sf
import sys
import datetime
def getPosition( tle , sat , time):
        timeFormat=  """%Y-%m-%dT%H:%M:%S.%f%z"""

        sats = sf.load.tle_file( tle )
        satellites = {sat.name: sat for sat in sats}
        ts = sf.load.timescale()
        dto = datetime.datetime.strptime( time , timeFormat ) 
        t = ts.from_datetime( dto )
        me = satellites[sat]
        pos = me.at( t )
        return ( pos.position.km , pos.velocity.km_per_s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get a satllites state')

    parser.add_argument("--tle", dest="tle", required=True)
    parser.add_argument("--satellite", dest="satellite", required=True)
    parser.add_argument("--time", dest="time", required=True)
    inputs = parser.parse_args(sys.argv[1:] )
    pos = getPosition(inputs.tle , inputs.satellite, inputs.time)
    print("Position: {}".format(pos[0]))
    print("Velocity: {}".format(pos[1]))
    print("Time: {}".format(inputs.time))