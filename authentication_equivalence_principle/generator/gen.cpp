#include <stdio.h>
#include <string.h>
#include <iostream>
#include "auth.hpp"

int main(){
    secrets::Encryptor enc;
    secrets::Encryptor dec;
    //Secret key - "YaBoiEinsteinsSecretKey" in base 64
    strncpy((char*)(&enc.data.key), "WWFCb2lFaW5zdGVpbnNTZWNyZXRLZXk=", 33);
    enc.data.rate = 50.0e-6;
    enc.data.lat  = 46.455144;
    enc.data.lon  = -119.407656;

    printf("Exporting:\n");
    // Players need to brute force the last three characters of the XXTEA key
    // prepare to be annoyed when you find out its "KEY" 
    enc.encrypt( "4269d55f91ad\x00KEY");
    std::cout<< enc << std::endl;
    enc.export_key("key.txt");
    enc.export_encrypted("authdata.bin");
    enc.decrypt("4269d55f91ad\x00KEY","authdata.bin" );
    //printf("Decoded:\n");
    //std::cout<< dec << std::endl;
    return 0;
}
