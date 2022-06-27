#pragma once
#include "StateMachine.h"
#include <string> 
#include "PID.h"
#include "types.h"
class DeOrbit : public State< Data::Sensor , Data::Command >
{
public:
    DeOrbit(double target);
    ~DeOrbit();
    virtual std::string update();
protected:
    PID< double> controller_; 
    double targetPeriapsis_;
};