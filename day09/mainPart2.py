#!/usr/bin/env python3
import pprint

pp = pprint.PrettyPrinter(indent=2)
blacklist = [] # Contain coordinate that already part of a basin

def lookTop(heightMap, heightIndex, pointIndex, point):
    if heightIndex != 0:
        return [int(heightMap[heightIndex-1][pointIndex]), (heightIndex-1, pointIndex)]
    else:
        return [point, (None, None)]

def lookDown(heightMap, heightIndex, pointIndex, point):
    if heightIndex+1 != len(heightMap):
        return [int(heightMap[heightIndex+1][pointIndex]), (heightIndex+1, pointIndex)]
    else:
        return [point, (None, None)]

def lookLeft(heightMap, heightIndex, pointIndex, point):
    if pointIndex != 0:
        return [int(heightMap[heightIndex][pointIndex-1]), (heightIndex, pointIndex-1)]
    else:
        return [point, (None, None)]

def lookRight(heightMap, heightIndex, pointIndex, point):
    if pointIndex+1 != len(heightMap[0]):
        return [int(heightMap[heightIndex][pointIndex+1]), (heightIndex, pointIndex+1)]
    else:
        return [point, (None, None)]


def lookAround(heightMap, heightIndex, pointIndex, point, disableTop=False):
    surroundingPoints = []
    surroundingPoints.append(lookLeft(heightMap, heightIndex, pointIndex, point))
    if not disableTop:
        surroundingPoints.append(lookTop(heightMap, heightIndex, pointIndex, point))
    surroundingPoints.append(lookRight(heightMap, heightIndex, pointIndex, point))
    surroundingPoints.append(lookDown(heightMap, heightIndex, pointIndex, point))
    return surroundingPoints

def getLowPoints(heightMap):
    lowPointsCoordinates = []
    for heightIndex, heightLine in enumerate(heightMap):
        for pointIndex, point in enumerate(heightLine):
            point = int(point)
            lowPoint = True
            surrounding = lookAround(heightMap, heightIndex, pointIndex, point)
            for sPoint in surrounding:
                if sPoint[0] < point:
                    lowPoint = False
            if lowPoint and point != 9:
                lowPointsCoordinates.append((heightIndex, pointIndex))
    return lowPointsCoordinates

def getBasinSize(heightMap, pointCoordinates):
    lineIndex = pointCoordinates[0]
    pointIndex = pointCoordinates[1]
    point = int(heightMap[lineIndex][pointIndex])
    blacklist.append(pointCoordinates)
    surrounding = lookAround(heightMap, lineIndex, pointIndex, point)
    validNeighbourCount = 1
    for neighbour in surrounding:
        if neighbour[0] != 9 \
            and neighbour[1] not in blacklist and neighbour[1] != (None, None):
            validNeighbourCount += getBasinSize(heightMap, neighbour[1])
    return validNeighbourCount


def main():
    heightMap = []
    with open('input.txt', 'r') as inputFile:
        for line in inputFile:
            heightMap.append(line.rstrip())

    # Part 1
    lowPointsCoordinates = getLowPoints(heightMap)
    print('nb Low :', len(lowPointsCoordinates))
    # Part 2
    allBasinsSize = [] # Contain size of each basins
    for lowPoint in lowPointsCoordinates:
        basinSize = getBasinSize(heightMap, lowPoint)
        #print("Blacklist : ")
        #pp.pprint(blacklist)
        allBasinsSize.append(basinSize)

    allBasinsSize.sort(reverse=True)
    #print("all basins size; ", allBasinsSize)
    print("nb basins size; ", len(allBasinsSize))
    answer = allBasinsSize[0] * allBasinsSize[1] * allBasinsSize[2]
    print("Answer : ", answer)

if __name__ == '__main__':
    main()

# not 959904, too low
