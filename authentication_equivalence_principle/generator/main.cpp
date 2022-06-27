#include <iostream>
#include <string>
#include "dll_stub.hpp"
#include <dlfcn.h>
#include "auth.hpp"
#include <cstring>
void generate_keys(void)
{
    double lat;
    double lon;
    double period;
    // we wont provide them with this file - so they wont be able to run this thing at all
    void *handle = dlopen("liborbital-totp.so", RTLD_LAZY);

    // Without the auth they are going to fail here in the block where we load sos
    if( !handle )
    {
        fprintf(stderr, "dlopen failed: %s\n", dlerror()); 
        return;
    }



    orbital_totp* (*create)(std::string);
    void (*destroy)(orbital_totp*);
    create = (orbital_totp* (*)(std::string))dlsym(handle, "create_auth");
    destroy = (void (*)(orbital_totp*))dlsym(handle, "delete_auth");
    orbital_totp* auth = (orbital_totp*)create("hmac");
    // 
    // The encryptor will be here - but they arent going to be able to decode wihtout brute forcing stuff
    std::cout<<"Decrypting protected data"<<std::endl;
    char key[17] = "0123456789abcdef";
    secrets::Encryptor enc;
    enc.decrypt(key , "authdata.bin");
    lat = enc.data.lat;
    lon = enc.data.lon;
    period = enc.data.rate;

    std::cout<<"Decrypted"<<std::endl;
    std::cout<< enc << std::endl;
    
    auth->set_loc( lat, lon );
    std::string hmackey( enc.data.key );
    auth->set_encrypt( hmackey );

    double time;
    std::cout<<"Time since last sync when satellite receives auth? "<<std::endl;
    std::cin >> time;
    std::string out;
    out = auth->keygen( time , period  );
    std::cout<<"Key is: "<< out << std::endl;
    destroy( auth);
}

void protect_data()
{
    secrets::Encryptor enc;
    char satkey[33] = {0} ;
    char key[17] = "0123456789abcdef";
    //std::cout<<"Key for data encrpytion?"<<std::endl;
    //std::cin >> key;
    std::cout<<"Satellite MFA HMAC key?"<<std::endl;
    std::cin >> satkey;
    
    memcpy((char*)(&enc.data.key), satkey, 33);
    std::cout<<"Rollover Period?"<<std::endl;
    std::cin >> enc.data.rate;
    std::cout<<"Latitude?"<<std::endl;
    std::cin >> enc.data.lat;
    std::cout<<"Longitude?"<<std::endl;
    std::cin >> enc.data.lon;

    std::cout<<"ENCRYPTING"<<std::endl;
    enc.encrypt( key );
    enc.export_key("key.txt");
    enc.export_encrypted("authdata.bin");

}   

int main(void)
{
    std::cout<<"Welcome"<<std::endl;
    std::cout<<"---------------------"<<std::endl;
    std::cout<<"1) Create protected data file"<<std::endl;
    std::cout<<"2) Generate auth keys"<<std::endl;
    std::cout<<"Choice? "<<std::endl;

    int choice;
    std::cin >> choice;

    switch(choice)
    {
        case 1:
            protect_data();
            break;
        case 2:
            generate_keys();
            break;
        default:
            std::cout<<"invalid choice"<<std::endl;
    }
}