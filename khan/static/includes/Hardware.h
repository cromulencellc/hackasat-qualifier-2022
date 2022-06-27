#pragma once

#include "types.h"
#include <string>

struct HwSensor
{

    float pos[3];
    float vel[3];
    float gsensor;

};
struct HwCommand
{

    float cmd[3];
    int chute;
    int shield;
};
class Hardware
{
public:
    Hardware(std::string ip , int port);
    ~Hardware();

    void send(Data::Command &in );
    Data::Sensor recv( );
protected: 
    int sockfd_;
};
