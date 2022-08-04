import skyfield.api as sf
import tlehelp as tlehelp
import measurements
import numpy as np
from numpy import linalg
import argparse
import sys



class SmartSolver:
    """ 
    The smart solver calculates the position and velocity vector of the satellite making ranging measurements and does not need the satellite to be in a TLE file in order to do the solution.

    This solver used a batch filter estimation technique

    """
    def __init__(self , tlefile , samples ):
        """
        :param tlefile: A text file containing the two line elements for the consetllation 
        :param samples: 
        """
        self.available = tlehelp.available(tlefile)
        sats = sf.load.tle_file( tlefile)
        self.satellites = {sat.name: sat for sat in sats}

        self.data = measurements.unpack( samples )
        pass
    def solve(self):
        pos = self.pvt_batch( self.data )
        return pos 

    def pvt_batch(self  , samples):
        """
        :return: A tuple in the form (position,velocity)

        :param samples: A dictionary of samples returned by measurements.unpack

        This solver uses a batch filter to solve the linear equation:

        .. math:: y = Hx

        Where:
        
        - y is a m x 1 vector of measurements
        - x is a n x 1 vector that is the state we want to calculate
        - H is a m x n matrix that defines the linear mapping from x to y

        This equation can be solved for x as follows

        .. math:: x = \left( H^TH \\right) H^T y

        However the equation for a single pseudo-range measurement between satellites is:

        .. math:: \\rho_k = \sqrt{ \left(X_k - X_c \\right)^2 + \left(Y_k - Y_c \\right)^2 + \left(Z_k - Z_c \\right)^2 } + cT_b + \\eta

        Where:

        - :math:`X_k, Y_k, Z_k` is the position coordinates vector of the satellite in the constellation
        - Xc is the position coordinates of the satellite in question
        - Tb is the time bias of the receiver measuring pseudo rnage
        - c is the speed of light
        
        And we are interested in the state vector: lils

        .. math:: x = \\begin{pmatrix}  X_C \\\ Y_C \\\ Z_C \\\ T_b \end{pmatrix}

        

        Since the relationship between x and y is non-linear we must extend the linear estiamtor. This is done by linearizing the nonlinear equations so that the measuremnt matrix, H, has components such that:
        
        .. math:: H_{i,j} = \\frac{ \\delta Y_i}{ \\delta X_j}     
        


        This strategy results in the ability to calculate  a correction to the state vector X. Taking the partial derivatives we can calculate the elemnets of the measurement matrix:

        .. math:: H_k = \\begin{pmatrix} 2\\frac{ X_k - X_C }{\\rho_k} &   2\\frac{ Y_k - Y_C}{\\rho_k} & 2\\frac{ Z_k - Z_C }{\\rho_k} & 0 & 0& 0& 1 \\\  \\frac{ \\rho_k \\left( V_{Xk} - V_{XC} \\right) - 2 \\dot{\\rho_k} \\Delta_X }{ \\rho_k^2}  & \\frac{ \\rho_k \\Delta_{Vy} - 2 \\dot{\\rho_k} \\Delta_Y }{ \\rho_k^2} & \\frac{ \\rho_k \\Delta_{Vz} - 2 \\dot{\\rho_k} \\Delta_Z }{ \\rho_k^2}  & \\frac{ X_k - X_C }{ \\rho_k}  & \\frac{ Y_k - Y_C }{ \\rho_k} & \\frac{ Z_k - Z_C }{ \\rho_k} & 0  \end{pmatrix}

        Such that:

        .. math:: H = \\begin{pmatrix}  H_0 \\\ H_1 \\\ .. \\\ H_n \end{pmatrix}

        Where:

        - :math:`X_C, Y_C, Z_C` are the estimated position coordinates of the satellite in question
        - :math:`X_k, Y_k, Z_K` are the position coordinates of the satellite in the constelation accoridng to the TLE model
        - :math:`V_{XC}, V_{YC}, V_{ZC}` are the estimated velocity coordinates of the satellite in question
        - :math:`V_{Xk}, V_{Yk}, V_{Zk}` are the velocity coordinates of the satellite in the constellation according to the TLE model



        Based on this form of the vector of measurments is:

        .. math:: y_k = \\begin{pmatrix} \\rho_k \\\ \\dot{ \\rho_k } \\end{pmatrix}
        
        Such that:

        .. math:: y = \\begin{pmatrix} y_0 \\\ y_1 \\\ ... \\\ y_k \\end{pmatrix}

        With these matricies and vectors calculated we can now calculate a correction to our state vector, X, as:

        .. math:: dX = \left( H^T H \\right) H^T y

        .. math:: X = X + dX

                
        """
        x = np.zeros((7,1))
        x[0] = 6356
        ts = sf.load.timescale()

        for i in range(40):
            print( "Iter {}".format(i))
            n = len( samples.keys() )
            H = np.zeros( (0,7) )
            y = np.zeros( (0,1))
            # Loop over every satellite in the constellation
            idx = 0
            for satellite, measurement in  samples.items():
                times = measurement["times"]
                ranges = measurement["ranges"]
                rates = measurement["rates"]
                time = ts.from_datetime( times[0] ) 
                rng = ranges[0]
                rate = rates[0]
                #Estimate in x
                xi = x[0][0] # estimated position x
                yi = x[1][0] # estimated position y 
                zi = x[2][0] # estimated position z
                vxi = x[3][0] # estimated velocity x
                vyi = x[4][0] # estimated velocity y
                vzi = x[5][0] # estimated velocity y
                rT = x[6][0] # estimated range error from clock bias
                # Position of satellite in the constellation which is being communicated with 
                orbit = self.satellites[satellite]
                state = orbit.at( time )
                
                position = state.position.km
                velocity = state.velocity.km_per_s
                # Calculate line of sight and rate between the target and the constellation satellite
                estLineOfSight = position - np.array([xi,yi,zi])
                estRelativeVelocity = velocity - np.array([vxi,vyi , vzi])
                rdv = np.dot( estLineOfSight , estRelativeVelocity ) 
                estRange = np.linalg.norm( estLineOfSight ) 
                estLosRate = rdv / estRange
              

                # Assemble a measurement matrix 
                # first solve the measurement matrix for the range measurement
                # Hi = [ 2*( xs-xi)/r 2*(ys-yi)/r 2*(zs-zi)/r 1]   --- note we are estimating c*tb so that we dont have a poorly scaled matrix
                dx = estLineOfSight[0]
                dy = estLineOfSight[1]
                dz = estLineOfSight[2]                 
                H_r = np.array( [2*dx/estRange , 2*dy/estRange , 2*dz/estRange, 0 , 0 , 0 ,1 ] ).reshape(1,7)
                # Next solve the measurment matrix for the range rate measurement
                dvx =estRelativeVelocity[0]
                dvy = estRelativeVelocity[1]
                dvz = estRelativeVelocity[2]
                H_v = np.array( [ (estRange*dvx - rdv*2*dx/estRange)/ np.square(estRange) ,\
                                   (estRange*dvy - rdv*2*dy/estRange)/np.square(estRange) ,\
                                   (estRange*dvz - rdv*2*dz/estRange)/np.square(estRange) ,\
                                   (dx / estRange) , \
                                   (dy / estRange) , \
                                   (dz / estRange) ,\
                                    0]).reshape(1,7)
                
                # Stack up teh measurement matrix
                Hi = np.vstack( (H_r , H_v) ) 
                

                H = np.vstack( (H , Hi ))
                dRange = [estRange - rng]

                dRangeRate = [estLosRate - rate ]

                delta_y = np.vstack( (dRange , dRangeRate))
                y = np.vstack( ( y , delta_y ))
            Ht = np.transpose(H)
            inv = np.linalg.inv(   Ht @ H )
            x_correction =inv @ ( Ht @  y ) 
            x = x + x_correction
            range_residual= linalg.norm(x_correction[0:2])
            vel_residual = linalg.norm(x_correction[3:5])
            time_residual = x_correction[6]
            print("Residuals pos: {} vel: {} time:{}".format(range_residual,vel_residual ,time_residual    ), flush=True)
            


        print( "Estimated position vector is {}".format(x[0:3].reshape(1,3)))
        print( "Estimated velocity vector is {}".format(x[3:6].reshape(1,3)))
        print( "Estimated clock bias (km) vector is {}".format(x[6]))
        print( "Time: {}".format( time.utc_strftime("""%Y-%m-%dT%H:%M:%S.%f%z""")  ) , flush=True)
        position = x[0:3].flatten()
        velocity = x[3:6].flatten()
        return ( position  , velocity )
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve cross link via a batch filter')
    parser.add_argument("--tle", dest="tle", required=True)
    parser.add_argument("--measurements", dest="measurements", required=True)
    inputs = parser.parse_args(sys.argv[1:] )

    s = SmartSolver( inputs.tle , inputs.measurements )
    s.solve()


    print("Done ")
    