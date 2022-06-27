
set( target secret )

add_library( ${target} )

target_sources( ${target} PRIVATE secret.cpp auth.cpp)
target_include_directories(${target} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})