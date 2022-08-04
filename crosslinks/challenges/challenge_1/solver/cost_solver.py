from numpy import linalg
import tlehelp as tlehelp
import measurements
import numpy as np
import skyfield.api as sf
import argparse
import sys

class BruteForceSolver:
    """
    The brute force solver uses the tle database and the measurements to take an expensive but effective approach to solving the satellite
    """
    def __init__(self, tlefile , samples ):
        """
        Constructor 
        :param tlefile: path to a text file of TLEs representing the constellation of satellites
        :param samples: a csv file of saples in the format created by the generator module
        """
        self.available = tlehelp.available(tlefile)
        self.available = tlehelp.available(tlefile)
        sats = sf.load.tle_file( tlefile)
        self.satellites = {sat.name: sat for sat in sats}        
        self.data = measurements.unpack( samples )
        pass
    

    def solve( self ):
        """
        :return: Satellite name in the constellation which has the minimum "cost"

        Calculate the following cost function for all satellites in the TLE database provided in the constructor

        .. math:: p_{i,k} = \left|  \\vec{r_k} - \\vec{r_c} \\right|

        .. math:: J_{c,k} = \\sum_{i=0}^{m} \left(  p_{i,k} - p_{model}\\right)

        Where

        .. math:: J_{c} = \\sum_{k=0}^{n} \left(  J_{c,k} \\right)




        - J_c is the "cost function" for the candidate satellite
        - k is an index representing each non-candidate satellite in the constellation
        - n is the number of non-candidate satellites in the constellation
        - i is an index for each time at which a measurement is made
        - m is the number of time measurments available
        - t_i is the time at which a range measurment at index i was taken
        - r_k is the position of the target satellite in the constellation
        - r_c is the position of the candidate satellite 
        - p_i is the range measurement at index i
        - p_model is the range estimated by the TLE model between the candidate satellite and the target satellite "k"
         Rdata is
         Rmodel is the expected position of the satellite 
        

        The candidate satellite which best matches the measurements will minimize the cost function

        Assumptions:

        - The satellite doing the ranging is in the TLE database 
        - Any noise on the range measurements should be approx 0
        - The range measurements are "true range" not pseudorange
        """
        error = dict()
        # loop over 
        ts = sf.load.timescale()

        costs = dict()
        for candidate in self.available:
            candidateOrbit  = self.satellites[ candidate ]
            
            # loop over all the satelliites in measurements 
            cost = 0 

            for satellite,data in self.data.items():
                
                
                targetOrbit  = self.satellites[ satellite ]
                # Define a cost function that starts as zero
                for tMeasured,rMeasured,rrMeasured in zip( data["times"] , data["ranges"] , data["rates"]):
                    time = ts.from_datetime(tMeasured) 

                    o1 = candidateOrbit.at( time)
                    o2 = targetOrbit.at( time  )
                    
                    p1 = o1.position.km
                    p2 = o2.position.km
                    
                    rangeExpected = np.linalg.norm( p2 - p1 )    
                    
                    cost += ( rMeasured - rangeExpected ) # do not normalize cost during integration
            costs[ candidate] = abs( cost )
        cost_view = [ (v,k) for k,v in costs.items() ]
        cost_view.sort( )
        #print("Satellite , Cost ")
        #for s , v in cost_view:
        #    print( "{},{}".format( s, v))
        solution = cost_view[0]
        print( "The satellite is {} calculated cost is {}".format( solution[1] , solution[0]))
        return solution[1]
        # Find the entry in cost dictioanry with lowesst value     


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solve cross link via a brute force method, output the satellite ID')
    parser.add_argument("--tle", dest="tle", required=True)
    parser.add_argument("--measurements", dest="measurements", required=True)
    inputs = parser.parse_args(sys.argv[1:] )

    b = BruteForceSolver( inputs.tle , inputs.measurements)
    b.solve( )

