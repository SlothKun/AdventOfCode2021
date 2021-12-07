#!/usr/bin/env python3

inputFile = open("input.txt", "r")

# Get numbers from file in int format and sorted
positions = sorted(list(map(int, inputFile.readline().rstrip().split(','))))

fuelNeeded = -1
bestPos = 0

# For each position, add nb of step needed between each other pos
# Save the least high sum
for currentPos in positions:
    tmpFuel = 0
    for nearbyPos in positions:
        if currentPos > nearbyPos:
            tmpFuel += (currentPos - nearbyPos)
        else:
            tmpFuel += (nearbyPos - currentPos)
    if tmpFuel < fuelNeeded or fuelNeeded == -1:
        fuelNeeded = tmpFuel
        bestPos = currentPos

print("fuel needed : ", fuelNeeded)
