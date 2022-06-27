# Small Hashes Anyways

SHA is a very simple and easy to automate microblaze crackme.
It's a close relative of [asby][asby] from SHA-2017 CTF,
which acceepts a string and tells you which spot the first
incorrect character is in.

[asby]: https://derbenoo.github.io/ctf/2017/08/11/sha2017_ctf_asby/

It's designed to get players comfortable with
scripting and `qemu-microblaze` operation,
since the easiest way to solve it is just cranking on that with
`popen` and a script.

It depends on [microblaze-user-toolchain][mut] for compiling,
and the `/opt/cross/microblaze-linux/lib` directory from that
needs to be distributed to players.
Grab one out of
<https://gitlab.mlb.cromulence.com/has3/quals/challenges/ominous_etude/-/jobs>
imo, that's what I tested with.

[mut]: https://gitlab.mlb.cromulence.com/has3/quals/microblaze-user-toolchain
