#!/usr/bin/env python3
import pprint
import itertools

pp = pprint.PrettyPrinter(indent=4)

octoGrid = []


def findNeighbours(fLineIndex, fOctoIndex):
    neighbours = []
    lineMin = fLineIndex-1 if fLineIndex-1 >= 0 else 0
    lineMax = fLineIndex+2 if fLineIndex+1 <= len(octoGrid) else len(octoGrid)
    octoMin = fOctoIndex-1 if fOctoIndex-1 >= 0 else 0
    octoMax = fOctoIndex+2 if fOctoIndex+1 <= len(octoGrid[0]) else len(octoGrid[0])

    for lineIndex in range(lineMin, lineMax):
        for octoIndex in range(octoMin, octoMax):
            if (lineIndex, octoIndex) != (fLineIndex, fOctoIndex) and (lineIndex, octoIndex) not in flashedCoordinates:
                neighbours.append((lineIndex, octoIndex))

    print(f"for {fLineIndex}:{fOctoIndex} - {neighbours}")
    return neighbours

def incrementNeighbours(flashCoordinates):
    flashedNeighbours = []
    neighbours = findNeighbours(flashCoordinates[0], flashCoordinates[1])
    for neighbour in neighbours:
        octo = octoGrid[neighbour[0]][neighbour[1]]
        octo = checkFlash(octo + 1)
        octoGrid[neighbour[0]][neighbour[1]] = octo
        if (octo == 0):
            flashedNeighbours.append(neighbour)
            flashedCoordinates.append(neighbour)
    return flashedNeighbours

def checkNeighbours(flashCoordinates, flashCount):
    flashedNeighbours = incrementNeighbours(flashCoordinates)
    for flashedNeighbour in flashedNeighbours:
        flashCount += 1
        checkNeighbours(flashedNeighbour, flashCount)
    return flashCount

def checkFlash(octo):
    if octo == 10:
        return 0
    else:
        return octo

def incrementWholeGrid():
    flashed = []
    for lineIndex, line in enumerate(octoGrid):
        for octoIndex, octo in enumerate(line):
            newOcto = checkFlash(octo + 1)
            if (newOcto == 0):
                flashed.append((lineIndex, octoIndex))
            octoGrid[lineIndex][octoIndex] = newOcto
    return flashed


def main():
    global flashedCoordinates
    flashedCoordinates = []
    with open("testInput1.txt", 'r') as inputFile:
        for line in inputFile:
            octoGrid.append([int(octo) for octo in line.rstrip()])

    flashCount = 0
    pp.pprint(octoGrid)
    for i in range(2):
        flashedCoordinates.clear()
        flashed = incrementWholeGrid()
        originalFlashs = flashed
        flashedCoordinates += flashed
        print("flashed coor :", flashedCoordinates)
        flashCount += len(flashedCoordinates)
        for flashCoordinates in originalFlashs[:3]:
            flashCount += checkNeighbours(flashCoordinates, flashCount)
        pp.pprint(octoGrid)
    print(f"{flashCount=}")



if __name__ == '__main__':
    main()
