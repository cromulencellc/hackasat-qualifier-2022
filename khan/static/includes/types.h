#pragma once
#include <iostream>
namespace Data
{
struct Sensor
{
    Sensor()
    {
        pos[0]=0.0f;
        pos[1]=0.0f;
        pos[2]=0.0f;
        vel[0]=0.0f;
        vel[1]=0.0f;
        vel[2]=0.0f;
        g_sensor=0.0f;
    }
    
    double pos[3];
    double vel[3];
    double g_sensor;

    void print()
    {
        std::cout<<"Pos: "<< pos[0] << " "<<pos[1] <<" "<<pos[2]<<std::endl;
        std::cout<<"Vel: "<< vel[0] << " "<<vel[1] <<" "<<vel[2]<<std::endl;
        std::cout<<"G: "<< g_sensor <<std::endl;
    }

};

struct Command
{
    Command()
    {
        force_cmd[0] =0.0f;
        force_cmd[1] =0.0f;
        force_cmd[2] =0.0f;
        shield=false;
        chute=false;
    }
    double force_cmd[3];
    bool shield;
    bool chute;
};


};