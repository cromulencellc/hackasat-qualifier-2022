#!/usr/bin/env ruby

BINARY_PATH = ENV['BINARY_PATH'] || '/mnt/small_hashes_anyways'
LIB_PATH = ENV['LIB_PATH'] || '/opt/cross/microblaze-linux'
QEMU_EXECUTABLE = ENV['QEMU_EXECUTABLE'] || 'qemu-microblaze'

ALPHABET = 0x20..0x7e

smoke_test = nil
IO.popen("#{QEMU_EXECUTABLE} -L #{LIB_PATH} #{BINARY_PATH}", 'r+') do |sha|
  puts sha.gets
  sha.puts
  smoke_test = sha.gets
end

smoek = /wrong length wanted (\d+) got 0/.match smoke_test

unless smoek
  p smoke_test
  fail "wanted this to tell me length, but it beefed"
end

length = smoek[1].to_i

skip = 0

CANDIDATE = (ENV['CANDIDATE'] || (ALPHABET.first.chr * length)).dup
if CANDIDATE.length > length
  fail "given candidate was too long"
elsif CANDIDATE.length < length
  skip = CANDIDATE.length - 1
  CANDIDATE << (ALPHABET.first.chr * (length - CANDIDATE.length))
end

(skip..length).each do |l|
  ALPHABET.each do |a|
    print "#{CANDIDATE}\r"
    CANDIDATE[l] = a.chr
    got = nil
    IO.popen("#{QEMU_EXECUTABLE} -L #{LIB_PATH} #{BINARY_PATH}", 'r+') do |sha|
      sha.gets
      sha.puts CANDIDATE
      got = sha.gets
    end
    fail "length mismatch: #{got}" if got =~ /wrong length/

    m = /mismatch (\d+) wanted \d+ got \d+/.match got

    unless m
      puts CANDIDATE
      puts got
      exit 0
    end

    mismatch_idx = m[1].to_i - 1

    if mismatch_idx > l
      puts CANDIDATE
      break
    end
  end
end

puts CANDIDATE