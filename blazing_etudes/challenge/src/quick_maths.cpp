#include <cstdint>

using std::uint32_t;

bool quick_maths(uint32_t run) {
run = run + 14301;
run = run + 5247;
run = run + 14341;
run = run + 9937;
run = run + 1138;
run = run - 147;
run = run / 14;
run = run - 217;
run = run + 9426;
run = run / 16;
run = run - 158;
return (run == 15270033);
}
