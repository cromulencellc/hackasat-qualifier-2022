import numpy as np
import skyfield.api  as sf 
import datetime
from flask import Flask,request,jsonify

class DestructionError( Exception ):
    pass
class PowerError( Exception ):
    pass
class HeatError( Exception ):
    pass

def clamp( value , min , max ):
    if( value < min ):
        return min
    if( value > max):
        return max
    return value


class Constellation:
    def __init__( self , tle_file ,  time ):
        sats = sf.load.tle_file( tle_file)
        satellites = {sat.name: sat for sat in sats}
        self.sats = dict()
        for name,sat in satellites.items():
            self.sats[name] = Satellite( sat , time )
        pass
    def get_sats(self):
        return self.sats
    def propagate( self ,  dt ):
        for name,sat in self.sats.items():
            sat.propagate( dt )
    def laser_on(self,name):
        self.sat[name].sharks_with_lasers( True )
    def laser_off( self, name):
        self.sat[name].sharks_with_lasers( False )
    
    def destroy( self , name ):
        del self.sats[name]
        print("Satellite destroyed")
        raise DestructionError 
    def run_detector( self , junk):
        for name,sat in self.sats.items():
            closest = sat.run_detector( junk )

                    
class Satellite:
    def __init__(self, sat , time ):
        self.ts = sf.load.timescale()
        self.sat = sat
        self.battery = 100
        self.heat = 253.0
        self.time = time
        self.charge_rate = 0.02 # per sec
        self.detector_drain_rate = 0.01
        self.detector_heating = 0.001
        self.laser_drain = 0.04
        self.heat_dissapation = 0.03
        self.laser_heating = 0.05
        self.laser_on = False
        self.detector_on = True
        self.max_range = 5000
        self.heat_limit = 373
        self.laser_cycle = 0 
        self.detector_cycle = 0 
        self.measured_range =self.max_range
        self.solar_system = sf.load( 'de421.bsp')
    def get_state( self ):
        return self.state
    def get_range( self ):
        return self.measured_range 
    def propagate( self , dt_seconds ):
        
        self.time += datetime.timedelta( seconds=dt_seconds )
        state = self.sat.at( self.time )
        self.state = state
        # check if the earth is eclipsing the satellite
        eclipsed = not state.is_sunlit(self.solar_system)
        # calculate chargng 
        if( True == eclipsed ):
            charge = 0
        else:
            charge = self.charge_rate * dt_seconds 
        #
        if( True == eclipsed ):
            dissapation = self.heat_dissapation*dt_seconds
        else:
            dissapation = 0
        if( True == self.laser_on ):
            laser_drain = (self.laser_drain)* dt_seconds
            laser_heating = ( self.laser_heating ) * dt_seconds
            
        else: 
            laser_drain = 0
            laser_heating = 0 
        if( True == self.detector_on):
            detector_drain = (self.detector_drain_rate)*dt_seconds
            detector_heating = self.detector_heating * dt_seconds
            pass
        else:
            detector_drain = 0
            detector_heating = 0
            pass
        
        self.battery += (charge-laser_drain-detector_drain)
        self.heat += (laser_heating+detector_heating-dissapation)

        self.battery = clamp( self.battery , 0 ,  100 )
        self.heat = clamp( self.heat , 250 , 400 )
        if( self.battery <= 0 ):
            print("You drained the battery....now the satellite is spacejunk")
            raise PowerError
        if( self.heat > self.heat_limit):
            print("The satellite got too hot and fried itself!")
            raise HeatError
    def run_detector( self,  junk ):

        if( True == self.detector_on):
            rngs = [self.max_range] # the detector  will ALWAYS return max range if it finds nothing
            for name, jnk in junk.items():
                o = jnk
                bad = o.position.km
                me = self.state.position.km
                dR = np.linalg.norm( bad-me)
                #print("{} - {} = {}".format( bad, me, dR))
                rngs.append( dR )
            min_rng = min( rngs )
            if( min_rng > self.max_range ):
                min_rng = self.max_range
            self.measured_range = min_rng
        else:
            self.measured_range = self.max_range
        return self.measured_range

    def sharks_with_lasers( self , on_off ):
        if( on_off != self.laser_on):
            if( on_off ):
                self.laser_cycle+=1
                print("Satellite Response: Lasers ON")
            else:
                print("Satellite Response: Lasers OFF")
        self.laser_on = on_off
    def detector( self ,on_off):
        self.detector_on = on_off
        if( on_off != self.detector_on):
            if( on_off ):
                self.detector_cycle +=1
                print("Satellite Response: Detector ON")
            else:
                print("Satellite Response: Detector OFF")
    def get_laser(self):
        return (self.laser_on,self.laser_cycle)
    def get_temperature(self):
        return self.heat
    def get_battery(self):
        return self.battery
    def get_detector( self ):
        return (self.detector_on, self.detector_cycle) 
    
        
        




