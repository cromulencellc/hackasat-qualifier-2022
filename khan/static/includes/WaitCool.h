#pragma once

#include "StateMachine.h"
#include <string>
#include "StateMachine.h"
#include "types.h"
class WaitCool : public State< Data::Sensor , Data::Command > 
{
public:
    WaitCool( double limit );
    ~WaitCool();

    std::string update();
protected:
    double velocityLimit_;

};