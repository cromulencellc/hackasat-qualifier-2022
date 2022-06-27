#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <vector>

#include "hbytes.hpp"

namespace crc32 {
  constexpr std::size_t _table_size = 256;

  using crc_t = uint32_t;
  using table_t = std::array<crc_t, _table_size>;

  constexpr table_t _make_table() {
    table_t tbl{};

    for (std::size_t n = 0; n < _table_size; n++) {
      crc_t c = n;

      for (byte k = 0; k < 8; k++) {
        if (1 & c) {
          c = 0xedb88320L ^ (c >> 1);
        } else {
          c = c >> 1;
        }
      }
      tbl[n] = c;
    }

    return tbl;
  }

  static constexpr table_t table = _make_table();

  static_assert(0x00000000 == table[  0]);
  static_assert(0x77073096 == table[  1]);
  static_assert(0x2d02ef8d == table[255]);

  crc_t calculate(const char* in, std::size_t count);
  crc_t calculate_begin(const char* in, std::size_t count);
  crc_t calculate_inter(crc_t inter, const char* in, std::size_t count);
  crc_t calculate_final(crc_t inter);

  namespace constexp {
    constexpr crc_t calculate_inter(crc_t inter,
                                    const char* in,
                                    std::size_t count) {
      crc_t crc = inter;

      for (std::size_t i = 0; i < count; i++) {
        byte b = in[i];
        crc_t cursor = (crc ^ b) & 0xFF;
        crc = table[cursor] ^ (crc >> 8);
      }

      return crc;
    }

    constexpr crc_t calculate_begin(const char *in, std::size_t count) {
      return calculate_inter(0xFFFFFFFF, in, count);
    }

    constexpr crc_t calculate_final(crc_t inter) {
      return ~inter;
    }

    constexpr crc_t calculate(const char* in, std::size_t count) {
      crc_t intermediate = calculate_begin(in, count);
      return calculate_final(intermediate);
    }

    static_assert(0 == calculate("", 0));
    static_assert(0x6783f342 == calculate("hamlin", 6));
  }
}
