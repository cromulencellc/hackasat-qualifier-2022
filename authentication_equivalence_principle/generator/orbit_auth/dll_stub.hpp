#pragma once
#include <string>


class orbital_totp
{
    public: 
        orbital_totp(std::string key);
        ~orbital_totp();
        virtual void set_encrypt( std::string secret_key);
        virtual std::string keygen(  double time , double rate);
        virtual void set_loc( double lat , double lon);
};