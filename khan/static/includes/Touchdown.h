#pragma once

#include "StateMachine.h"
#include "types.h"


class Touchdown : public State< Data::Sensor,  Data::Command > 
{
public:
    Touchdown();
    ~Touchdown();
    std::string update();
} ;