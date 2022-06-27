#include <iostream>

#include "asby.hpp"
#include "crc32.hpp"

int check(const std::string &got) {
  std::size_t max_len = asby.size();

  if (got.size() != (asby.size() - 1)) {
    std::cout << "wrong length wanted " 
    << (asby.size() - 1) << " got "
    << got.size() << std::endl;
    return 1;
  }

  for (std::size_t i = 0; i < max_len; i++) {
    const crc32::crc_t h = crc32::calculate(got.data(), i);
    if (h != asby.at(i)) {
      std::cout << "mismatch " << i 
        << " wanted " << asby.at(i) << " got " << h
        << std::endl;
      return 1;
    }
  }

  std::cout << "🏀 swish bay bee 😎" << std::endl;

  return 0;
}