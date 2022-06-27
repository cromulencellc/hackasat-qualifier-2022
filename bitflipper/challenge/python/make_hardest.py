#!/usr/bin/env python3

import json
from math import ceil

with open("lookup.json", "r") as f:
    nums = json.loads(f.read())

nums = nums[1:]

for i in range(len(nums)):
    nums[i] -= 1

nums_small = [0] * (ceil(len(nums) / 2))

for idx, num in enumerate(nums):
    nums_small[idx//2] |= (num << (4 if idx&1 else 0))

with open("hnums.h", "w") as f:
    f.write("#include <stdint.h>\n")
    f.write(f"uint8_t hardest_lookup[{len(nums_small)}] = {{")
    for idx, num in enumerate(nums_small):
        if idx % 16 == 0:
            f.write("\n")
        f.write(f"{hex(num)}, ")

    f.seek(f.tell()-2, 0)
    
    f.write("\n};")