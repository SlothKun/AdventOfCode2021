#!/usr/bin/env python3
from lanternFish import LanternFish
import time
import sys
from pympler.asizeof import asizeof

startTime = time.time()

inputFile = open("input.txt", 'r')

# Get fish from input
starterFish = list(map(int, inputFile.readline().rstrip().split(',')))

NEW_BORN_TIMER = 8
tempFishList = []
allFishs = []

# Create fish objects
for fish in starterFish:
    allFishs.append(LanternFish(fish))


# for X days
for i in range(80):
    # Get every fish
    for fish in allFishs:
        # Decrease time before new fish
        fish.decreaseTimer()
        # If timer's up, create a new fish (in a temp list) & reset the time
        if fish.getDaysLeft() == -1:
            tempFishList.append(LanternFish(NEW_BORN_TIMER))
            fish.resetTimer()
    # Merge lists together and clear the temps list
    allFishs = allFishs + tempFishList
    tempFishList = []

print("nb of fish : ", len(allFishs))
print("exec time : ", time.time() - startTime)
print("Size at the end : ", asizeof(allFishs))
