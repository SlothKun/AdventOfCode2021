#!/usr/bin/env python3
import time

startingTime = time.time()

inputFile = open("input.txt", "r")

# Get numbers from file in int format and sorted
positions = sorted(list(map(int, inputFile.readline().rstrip().split(','))))

fuelNeeded = -1
bestPos = 0

# Apply math formula that compute the sum of each number in a range
def computeTriangularNumber(n):
    return (n * n + n) / 2

minPos = positions[0]
maxPos = positions[-1] + 1

# For each position, between the min and the max
for currentPos in range(minPos, maxPos):
    tmpFuel = 0
    for nearbyPos in positions:
        # compute the fuel needed
        tmpFuel += computeTriangularNumber(abs(currentPos - nearbyPos))
    # If this fuel consumption is less than the previous best record, replace best record
    if tmpFuel < fuelNeeded or fuelNeeded == -1:
        fuelNeeded = tmpFuel
        bestPos = currentPos

print("fuel needed : ", fuelNeeded)
print("Best pos : ", bestPos)
print("Time : ", time.time() - startingTime)
