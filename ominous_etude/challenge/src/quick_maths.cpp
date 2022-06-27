#include <cstdint>

using std::uint32_t;

bool quick_maths(uint32_t run) {
run = run / 4;
run = run + 9356;
run = run + 13607;
run = run / 12;
run = run - 254;
run = run * 24;
run = run / 8;
run = run * 12;
run = run / 11;
run = run * 20;
run = run / 5;
run = run - 164;
return (run == 812310692);
}
