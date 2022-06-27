#pragma once

#include "StateMachine.h"
#include "types.h"

class WaitChute : public State< Data::Sensor,  Data::Command > 
{
public:
    WaitChute(double limit );
    ~WaitChute();
    std::string update();
protected:
    double accelLimit_;
}; 