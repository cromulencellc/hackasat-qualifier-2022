#pragma once
#include <cstring>

template<typename T , typename U=T> class PID
{
public:
    PID( T Kp , T Ki , T Kd ) :
        Kp_(Kp),
        Ki_(Ki),
        Kd_(Kd),
        last_(0.0),
        integral_(0.0),
        count_(0)
    {

    }
    ~PID()
    {

    }

    U update(const U &in )
    {
        U out;
        U deriv;
        integral_ = integral_ + ( Ki_ * in );
        if( 0 != count_ )
        {
            deriv = Kd_ *( in - last_ );
        }
        out =  Kp_*in +  integral_ + deriv;
        count_++;
        return out;
    }
    void reset()
    {
        count_ = 0 ;
    }
protected:
    T Kp_;
    T Ki_;
    T Kd_;
    U last_;
    U integral_;
    size_t count_;
};