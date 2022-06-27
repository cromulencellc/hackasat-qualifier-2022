#pragma once

#include <stdint.h>
#include <exception>
#include <string>


namespace secrets 
{
    // Struct Definitions
    struct auth_t 
    {
        // Making the key "33" in length even though it is 32 bytes will make the compiler insert some padding bytes
        // between the key and the next double variable to achieve alignment of the doubles on a 8 byte boundary
        char key[33];   // Base64 TOTPP Key and Salt for HMAC
        double rate;    // Rate variable for TOTPP alg
        double lat;     // Latitude position of GS
        double lon;     // Longitude position of GS
    } ;
    struct encoded_t{
    unsigned char encrypted_data[68];
    } ;


class Error : public std::exception 
{
    virtual const char* what() const throw()
    {
        return "Secrets: Exception";
    };
} ;



class Encryptor
{
    public:
        Encryptor();
        ~Encryptor();

        bool decrypt(const char* key, std::string filename );
        bool encrypt(const  char* secret_key);
        bool export_encrypted( std::string filename );
        bool export_key( std::string filename );
        auth_t data;
        std::string key;

    protected:
        unsigned char *encrypted;
        size_t size_encrypted;

  
};

};

std::ostream &operator<<(std::ostream &os, secrets::Encryptor const &m);
