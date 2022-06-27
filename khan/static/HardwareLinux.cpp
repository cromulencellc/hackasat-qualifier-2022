#include "Hardware.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
Hardware::Hardware(std::string ip , int port)
{
    int portno;
    struct sockaddr_in serv_addr;
    struct hostent *server;


    
    sockfd_ = socket(AF_INET, SOCK_STREAM, 0);
    int iMode( 0 );
    ioctl( sockfd_ , FIONBIO , &iMode );
    if (sockfd_ < 0) 
    {
        throw 1;
    }
    
    server = gethostbyname(ip.c_str());
    if (server == NULL)
    {
        throw 2;
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    serv_addr.sin_port = htons(port);
    if (connect(sockfd_,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
    {
       throw 3;
    }
}


Hardware::~Hardware()
{

}

void Hardware::send(  Data::Command &in)
{
    size_t written;
    HwCommand c;
    c.chute =  in.chute  ? 1 : 0 ;
    c.shield = in.shield ? 1 : 0 ;
    c.cmd[0] = static_cast<float>(in.force_cmd[0]);
    c.cmd[1] = static_cast<float>(in.force_cmd[1]);
    c.cmd[2] = static_cast<float>(in.force_cmd[2]);
    written = write(sockfd_,&c,sizeof( HwCommand));
    //printf("Wrote %lu\n", written);

    if( written != sizeof(HwCommand))
    {
        throw 4;
    }

}

Data::Sensor Hardware::recv( )
{
    Data::Sensor d;
    HwSensor s;
    size_t bytesRead;
    bytesRead = read(sockfd_,&s,sizeof( HwSensor));
    //printf("Read %lu\n", bytesRead);

    if( bytesRead != sizeof(HwSensor))
    {
        throw 5;
    }
    d.pos[0] = static_cast<double>(s.pos[0]);
    d.pos[1] = static_cast<double>(s.pos[1]);
    d.pos[2] = static_cast<double>(s.pos[2]);
    d.vel[0] = static_cast<double>(s.vel[0]);
    d.vel[1] = static_cast<double>(s.vel[1]);
    d.vel[2] = static_cast<double>(s.vel[2]);
    d.g_sensor = static_cast<double>(s.gsensor);
    //d.print();
    return d;
}