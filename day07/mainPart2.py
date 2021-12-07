#!/usr/bin/env python3
import time

startingTime = time.time()

inputFile = open("input.txt", "r")

# Get numbers from file in int format and sorted
positions = sorted(list(map(int, inputFile.readline().rstrip().split(','))))

fuelNeeded = -1
bestPos = 0

def getFuelNeeded(moveRange):
    fuel = 0
    for i in range(1, moveRange+1):
        fuel += i
    return fuel

minPos = positions[0]
maxPos = positions[-1] + 1

# For each position, between the min and the max
# compute the fuel needed
# Save the least highest sum
for currentPos in range(minPos, maxPos):
    tmpFuel = 0
    for nearbyPos in positions:
        if currentPos > nearbyPos:
            tmpFuel += getFuelNeeded((currentPos - nearbyPos))
        else:
            tmpFuel += getFuelNeeded((nearbyPos - currentPos))
    if tmpFuel < fuelNeeded or fuelNeeded == -1:
        fuelNeeded = tmpFuel
        bestPos = currentPos

print("fuel needed : ", fuelNeeded)
print("Best pos : ", bestPos)
print("Time : ", time.time() - startingTime)
