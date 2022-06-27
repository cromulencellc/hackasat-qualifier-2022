#include <iostream>
#include <string>

#include "check.hpp"

int main() {
  std::cout << "small hashes anyways: " << std::endl;

  std::string got;
  std::getline(std::cin, got);

  return check(got);
}