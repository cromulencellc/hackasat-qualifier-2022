require 'digest'
require 'fileutils'
require 'json'

UINT32_MAX = 0xffffffff

def num_in_range(op)
  case op
  when :/
    rand(2..16)
  when :*
    rand(2..32)
  when :-
    rand(0..256)
  when :+
    rand(0..16384)
  else
    fail "couldn't num_in_range for #{op}"
  end
end

dest = File.join __dir__, 'src', 'quick_maths.cpp'
hint = File.join __dir__, 'hint.txt'

out_f = File.open dest, 'w'

out_f.puts <<~EOS.strip
#include <cstdint>

using std::uint32_t;

bool quick_maths(uint32_t run) {
EOS

want = rand(0..UINT32_MAX)
run = want
File.write(hint, want.to_s + "\n")

rand(10..20).times do
  stmt = nil
  result = nil

  loop do
    operation = %i{+ - * /}.sample
    operand = num_in_range(operation)

    result = run.send operation, operand

    # next here loops again
    next if result >= UINT32_MAX
    next if result <= 0

    stmt = "run = run #{operation} #{operand};"
    break
  end

  out_f.puts stmt
  run = result
end


out_f.puts <<~EOS.strip
return (run == #{ run });
}
EOS

out_f.close

`make clean all`

size = `wc -c build/ominous_etude`.split[0].to_i
digest = `sha256sum build/ominous_etude`.split[0]

File.open('hints.json', 'w') do |h|
  h.write JSON.dump({
    'ominous_etude' => {
      'sha256' => digest,
      'size' => size,
      'answer' => want.to_s
    }
  })
end

FileUtils.mkdir 'ominous_etude'
FileUtils.cp 'build/ominous_etude', 'ominous_etude/'
`tar jfc ominous_etude.tar.bz2 ominous_etude`

FileUtils.mkdir 'lib'
FileUtils.cp_r '/opt/cross/microblaze-linux/lib', 'lib'
`tar jfc lib.tar.bz2 lib`