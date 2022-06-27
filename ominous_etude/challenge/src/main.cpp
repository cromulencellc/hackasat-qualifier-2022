#include <cstdint>
#include <cstdlib>
#include <iostream>

using std::uint32_t;

bool quick_maths(uint32_t run);

int main() {
  std::cout << "enter decimal number: ";

  uint32_t candidate;
  std::cin >> candidate;

  bool happy = quick_maths(candidate);

  if (! happy) {
    std::cout << "hmm… not happy :(" << std::endl;
    std::exit(1);
  }

  std::cout << "cool :)" << std::endl;
  std::exit(0);
}
