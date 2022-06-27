#include <iostream>
#include "StateMachine.h"
#include "WaitCool.h"
#include "DeOrbit.h"
#include "WaitChute.h"
#include "Touchdown.h"
#include "Hardware.h"
#include "types.h"


int main( void )
{
    try
    {
        Hardware hw("127.0.0.1", 6000);
        StateMachine<Data::Sensor, Data::Command> sm; 
        DeOrbit deorbit( 100.0 ); // deorbit burn to periapsis of 100km
        WaitCool waitcool( 1.0 ); // wait until V < 1.0 km/s
        WaitChute waitchute( 15.0 ); // wait until g measured < 15 m/s2
        Touchdown touchdown;
        sm.add( "DeOrbit", &deorbit);
        sm.add( "WaitCool", &waitcool);
        sm.add( "WaitChute", &waitchute);
        sm.add( "Touchdown", &touchdown);
        sm.forceState("DeOrbit");
        while( true )
        {   

            Data::Sensor in;
            Data::Command out;
            in = hw.recv();
            sm.set( in );
            sm.update( );
            out = sm.get();
            hw.send( out );
        }
    }
    catch(int e)
    {
        std::cout<<"Exception: "<< e <<std::endl;
    }
    return 0;
}