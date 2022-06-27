#include "auth.hpp"
#include "secret.h"
#include <string>

#include <iostream>
namespace secrets
{
    Encryptor::Encryptor()
    {
        key = "unset";
        encrypted = nullptr;
    }
    Encryptor::~Encryptor()
    {
        if( nullptr != encrypted)
        {
            delete[] encrypted;
        }
    }

    
    bool Encryptor::decrypt(const char*  key , std::string filename )
    {
        // Read the encrypted file into bytes
        FILE *fp;
        int sz = 0;
        size_t out_len(0);
        size_t bytes_read = 0;
        void *decrypted;
        fp = fopen(filename.c_str(), "rb");

        if(fp == NULL){
            std::cout<<"File open failed"<<std::endl;
            throw secrets::Error();
        }

        fseek(fp, 0L, SEEK_END);
        sz = ftell(fp);

        rewind(fp);
        encrypted = new unsigned char[sz];
        
        if(encrypted == NULL){
            throw secrets::Error();
        }
        std::cout<<"Decrypting "<<sz<<" bytes"<<std::endl;
        std::cout<<"Using key: "<< key  << std::endl;
        bytes_read = fread(encrypted, sizeof(uint8_t), sz, fp);
        
        size_encrypted = bytes_read;
        
        fclose(fp);

        // decrypt the file
        decrypted = secret_decrypt( encrypted , size_encrypted , key , &out_len );

        std::cout<<"Decrypted "<< out_len << " bytes"<<std::endl;
        data = *reinterpret_cast<auth_t*>(decrypted);
        return true;

    }
    bool Encryptor::encrypt(const  char* secret_key)
    {
        void* out(nullptr);
        size_t out_len(0);
        out = secret_encrypt( &data , sizeof( auth_t ) , secret_key , &out_len);
        encrypted = reinterpret_cast<unsigned  char*>(out);
        // THIS IS OUR BUG --- making a string out of something with a \x00 in it will result in the string
        // being truncated
        key = std::string(secret_key);
        size_encrypted = out_len;
        std::cout<<"Encrypted payload: "<< out_len << " bytes "<<std::endl;
        return true;
    }
    bool Encryptor::export_key( std::string filename )
    {
        size_t out_len(0);
        FILE *fp;
        fp = fopen(filename.c_str(), "wb");
        if(fp == NULL)
        {
            throw secrets::Error();
        }
    
        fwrite( key.c_str() , key.length()  , 1 ,fp);
        fclose(fp);
        return true;
    }
    // Write file format 
    bool Encryptor::export_encrypted( std::string filename )
    {
        size_t out_len(0);
        FILE *fp;
        fp = fopen(filename.c_str(), "wb");
        if(fp == NULL)
        {
            throw secrets::Error();
        }
        

        out_len = fwrite(encrypted, size_encrypted, 1, fp);
        fclose(fp);

        return true;
    }

}

std::ostream &operator<<(std::ostream &os, secrets::Encryptor const &m)
{
    std::string out;
    out = "rollover period: " + std::to_string( m.data.rate ) + "\n" 
          + "latitude: " + std::to_string( m.data.lat) + "\n" 
          + "longitude: " + std::to_string(m.data.lon) + "\n" 
          + "HMAC Key: " + std::string( m.data.key) + "\n" 
          + "Secret_Key: " + std::string( m.key );//"key: " + (m.data.key + ;
    return os<< out;// << m.data.key << " rollover period: " << m.data.rate << " lat: " << m.data.lat << " long: " << m.data.lon;  
}