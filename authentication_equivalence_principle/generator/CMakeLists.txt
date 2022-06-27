
cmake_minimum_required(VERSION 3.10)

project( Authenticator )

add_subdirectory( xxtea )
add_subdirectory( orbit_auth)
add_executable( gen gen.cpp)
target_link_libraries( gen secret )
add_executable( authenticator main.cpp )
target_link_libraries( authenticator PRIVATE orbital-totp secret ${CMAKE_DL_LIBS}) 