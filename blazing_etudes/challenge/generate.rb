require 'digest'
require 'fileutils'
require 'json'
require 'set'

UINT32_MAX = 0xffffffff

NUMBER_TO_GENERATE = 189 # EM_MICROBLAZE magic number

# 1024 omens should be enough for anyone

PORTENTS = %w{ ominous portentious baleful forbidding menacing sinister 
  threatening ill inauspicious dire doomy minatory bleak funereal glum 
  dreary sad trepidatious fearful scary spooky alarming anxious shocking
  terrible terrifying ghastly direful foreboding formidable spine-chilling
  frightening
}.uniq

ETUDES = %w{ etude study drill form composition dirge piece canon 
  arrangement scale concerto waltz dance ball prom formal mixer
  masque masquerade reception shindig mambo polka jitterbug twist
  shuffle shimmy jig gavotte bop boogey honkytonk
}.uniq

SEEN_OMENS = Set.new
hints = Hash.new

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

def new_omen
  found_omen = nil

  loop do
    p = PORTENTS.sample
    e = ETUDES.sample
    found_omen = "#{p}_#{e}"

    break
  end

  SEEN_OMENS.add found_omen

  return found_omen
end

FileUtils.mkdir "blazing_etudes"

NUMBER_TO_GENERATE.times do 
  dest = File.join __dir__, 'src', 'quick_maths.cpp'

  out_f = File.open dest, 'w'

  out_f.puts <<~EOS.strip
  #include <cstdint>

  using std::uint32_t;

  bool quick_maths(uint32_t run) {
  EOS

  want = rand(0..UINT32_MAX)
  run = want

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

  new_omen_name = new_omen
  FileUtils.mv 'build/ominous_etude', "blazing_etudes/#{new_omen_name}"

  hints[new_omen_name] = {
    'sha256' => digest,
    'size' => size,
    'answer' => want.to_s
  }

end

File.open('hints.json', 'w') do |h|
  h.write JSON.dump(hints)
end

`tar jfc blazing_etudes.tar.bz2 blazing_etudes`

FileUtils.mkdir 'microblaze-linux'

FileUtils.cp_r '/opt/cross/microblaze-linux', 'microblaze-linux'
`cd microblaze-linux; tar jfc microblaze-linux.tar.bz2 microblaze-linux/`