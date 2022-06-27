#include "dll_stub.hpp"
#include <iostream>

orbital_totp::orbital_totp(std::string hash)
{
    std::cout<<"STUB: using hash: "<<hash << std::endl;
}
orbital_totp::~orbital_totp()
{

}

void orbital_totp::set_loc( double lat , double lon)
{
    std::cout<<"STUB: ground station at "<< lat << " " << lon << std::endl;
}
void orbital_totp::set_encrypt( std::string secret_key )
{
    std::cout<<"STUB: Secret Key is "<< secret_key << std::endl;
}
std::string orbital_totp::keygen(  double time , double rate)
{
    // this is just a stub because the user wont get the keygen library
    std::cout<<"STUB: calculate auth for "<< time <<" at rate "<< rate << std::endl;
    return "Fake Key";
}


extern "C" orbital_totp* create_auth(std::string hash )
{
    return new orbital_totp(hash);
}

extern "C" void delete_auth( orbital_totp *auth)
{
    delete auth;

}
