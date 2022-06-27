#pragma once

#include <cstddef>

#include "hbytes.hpp"

template <typename T>
constexpr T
hton(const T &host_i)
{
    T net_i = 0;
    const std::size_t byte_count = sizeof(host_i);
    byte* bytes = (byte*)(void*) &net_i;

    for (std::size_t idx = 0; idx < byte_count; idx++) {
        bytes[idx] = host_i >> ((byte_count - idx - 1) * 8);
    }

    return net_i;
}


// yeah it's the same
template <typename T>
constexpr T
ntoh(const T &host_i)
{
    T net_i = 0;
    const std::size_t byte_count = sizeof(host_i);
    byte* bytes = (byte*)(void*) &net_i;

    for (std::size_t idx = 0; idx < byte_count; idx++) {
        bytes[idx] = host_i >> ((byte_count - idx - 1) * 8);
    }

    return net_i;
}
