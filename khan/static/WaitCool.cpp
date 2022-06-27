#include "WaitCool.h"

#include "Eigen/Dense"
WaitCool::WaitCool(double limit) : State() ,
    velocityLimit_(limit)
{

}

WaitCool::~WaitCool()
{

}

std::string WaitCool::update()
{
    Eigen::Vector3d vel( in_->vel[0] , in_->vel[1] , in_->vel[2]);

    double magVel = vel.norm();
    if( magVel < velocityLimit_ )
    {
        out_->shield = true ; 
        //printf("Popping heat shield\n");
        return "WaitChute";
    }
    else
    {
        return "WaitCool";
    }
}