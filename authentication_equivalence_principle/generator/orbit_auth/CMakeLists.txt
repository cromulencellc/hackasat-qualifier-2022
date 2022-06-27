
set( target orbital-totp )

add_library( ${target} SHARED )

target_sources( ${target} PRIVATE dll_stub.cpp )
target_include_directories(${target} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} )