#include "DeOrbit.h"
#include <cmath>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <Eigen/Dense>
DeOrbit::DeOrbit( double target ) : State(),
    targetPeriapsis_(target + 13120.0 ),
    controller_( 0.1 , 0.01 , 0.1)
{

}

DeOrbit::~DeOrbit()
{

}

std::string DeOrbit::update()
{
    Eigen::Vector3d pos( in_->pos[0] , in_->pos[1] , in_->pos[2]);
    Eigen::Vector3d vel( in_->vel[0] , in_->vel[1] , in_->vel[2]);
    double mu(2527105.1264); // km^3 / s^2
    Eigen::Vector3d h;
    double h_norm;
    Eigen::Vector3d e_bar;
    double a;
    double e;
    double p;
    double peri;
    double periError;
    double thrustScalar;
    Eigen::Vector3d direction;
    h = pos.cross( vel );
    h_norm = h.norm();
    e_bar = (vel.cross( h )/mu) - ( pos / pos.norm());
    e = e_bar.norm();
    p = h_norm * h_norm / mu ;
    a = p * ( 1 - e*e );
    peri = a * ( 1 - e );        
    periError = peri- targetPeriapsis_;
    if( abs( periError ) < 1.0  )
    {
        out_->force_cmd[0] = 0.0;
        out_->force_cmd[1] = 0.0;
        out_->force_cmd[2] = 0.0;
        //printf("Manuever complete\n");
        return "WaitCool";
    }
    else
    {
        Eigen::Vector3d thrust;
        thrustScalar = controller_.update( periError );
        direction =  -vel / vel.norm();
        thrust = thrustScalar * direction;
 
        out_->force_cmd[0] = thrust[0];
        out_->force_cmd[1] = thrust[1];
        out_->force_cmd[2] = thrust[2];
        return "DeOrbit";
    }
}