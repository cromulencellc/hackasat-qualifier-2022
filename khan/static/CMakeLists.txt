cmake_minimum_required(VERSION 3.15.0 )
set( CMAKE_TOOLCHAIN_FILE aarch64.cmake )
project( LANDER )


# Create a list of cpp files that is a little easier to manage
set( sources 
    DeOrbit.cpp
    HardwareLinux.cpp
    main.cpp
    Touchdown.cpp
    WaitChute.cpp
    WaitCool.cpp )

add_executable( Lander ${sources} )

target_include_directories( Lander PUBLIC /usr/include/eigen3 includes)
target_link_libraries( Lander PUBLIC m c)
target_compile_definitions(Lander PUBLIC EIGEN_NO_MALLOC )
target_compile_options( Lander PUBLIC -std=c++11 -static)
