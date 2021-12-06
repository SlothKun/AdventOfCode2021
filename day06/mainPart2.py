#!/usr/bin/env python3
import sys
import time
from pympler.asizeof import asizeof

startTime = time.time()

MAX_DAYS = 9
CYCLES = 256
NEWBORN_TIMER = 8
DEFAULT_DAYS = 6
fishCount = { 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0 }
dayZeroFish = 0

inputFile = open("input.txt", 'r')

# Get fish from input
starterFish = list(map(int, inputFile.readline().rstrip().split(',')))

# Add fish to the dict
for fish in starterFish:
    fishCount[fish] += 1


# For each cycle, go through each days and move them to the left
# For day 0, keep them in a temp var
# For day 6, get fish from day 7 and add them the fish in temp var
# For day 8, put fish from day 0
for i in range(CYCLES):
    for day in range(MAX_DAYS):
        if day == 0:
           dayZeroFish = fishCount[day]
           fishCount[day] = fishCount[day+1]
        elif day == DEFAULT_DAYS:
            fishCount[day] = fishCount[day+1] + dayZeroFish
        elif day == NEWBORN_TIMER:
            fishCount[day] = dayZeroFish
        else:
            fishCount[day] = fishCount[day+1]

# Sum the fish count of all days
total = 0
for i in range(MAX_DAYS):
    total += fishCount[i]

# Print result, exec time and size of dict
print("nb of fish : ", total)
print("exec time : ", time.time() - startTime)
print("Size at the end : ", asizeof(fishCount))
