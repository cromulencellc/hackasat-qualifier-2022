require 'zlib'

flag = ENV['FLAG'] || 
  "flag{contact an admin if you see this! shouldn't happen}"

hashes = (1..flag.length).map do |h|
  Zlib.crc32 flag.slice(0, h)
end

File.open(File.join(__dir__, 'src', 'asby.hpp'), 'w') do |f|
  f.write <<~EOF
#pragma once

#include <array>

#include "crc32.hpp"

const std::array<crc32::crc_t, #{flag.length + 1}> asby = {0,
EOF

  hashes.zip(flag.chars) do |h, c|
    f.puts "  #{h}, // #{c}"
  end

  f.puts "};"
end

`make clean all`

puts "build/small_hashes_anyways"