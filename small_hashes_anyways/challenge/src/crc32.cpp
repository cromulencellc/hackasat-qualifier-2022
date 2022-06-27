#include "hton.hpp"

#include "crc32.hpp"

using namespace crc32;

crc_t crc32::calculate(const char* in, std::size_t count) {
  return constexp::calculate(in, count);
}

crc_t crc32::calculate_begin(const char* in, std::size_t count) {
  return constexp::calculate_begin(in, count);
}

crc_t crc32::calculate_inter(crc_t inter, const char* in, std::size_t count) {
  return constexp::calculate_inter(inter, in, count);
}

crc_t crc32::calculate_final(crc_t inter) {
  return constexp::calculate_final(inter);
}
