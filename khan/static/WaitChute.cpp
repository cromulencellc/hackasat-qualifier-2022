#include "WaitChute.h"

WaitChute::WaitChute( double limit ) : State(),
    accelLimit_( limit )
{

}
WaitChute::~WaitChute()
{


}

std::string WaitChute::update()
{
    
    if( in_->g_sensor < accelLimit_ )
    {
        out_->chute = true ;
        //printf("Parachute deployed\n");
        return "Touchdown";
    }
    else
    {
        return "WaitChute";
    }
}