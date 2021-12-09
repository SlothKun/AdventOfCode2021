#!/usr/bin/env python3


def lookTop(heightMap, heightLineIndex, pointIndex, point):
    return int(heightMap[heightLineIndex-1][pointIndex]) if heightLineIndex != 0 else int(point)

def lookDown(heightMap, heightLineIndex, pointIndex, point):
    return int(heightMap[heightLineIndex+1][pointIndex]) if heightLineIndex+1 != len(heightMap) else int(point)

def lookLeft(heightMap, heightLineIndex, pointIndex, point):
    return int(heightMap[heightLineIndex][pointIndex-1]) if pointIndex != 0 else int(point)

def lookRight(heightMap, heightLineIndex, pointIndex, point):
    return int(heightMap[heightLineIndex][pointIndex+1]) if pointIndex+1 != len(heightMap[0]) else int(point)

def main():
    heightMap = []
    with open('input.txt', 'r') as inputFile:
        for line in inputFile:
            heightMap.append(line.rstrip())

    riskLevelSum = 0
    nbLowPoint = 0
    for heightLineIndex, heightLine in enumerate(heightMap):
        for pointIndex, point in enumerate(heightLine):
            lowPoint = True
            if lookTop(heightMap, heightLineIndex, pointIndex, point) < int(point):
                lowPoint = False
            elif lookDown(heightMap, heightLineIndex, pointIndex, point) < int(point):
                lowPoint = False
            elif lookLeft(heightMap, heightLineIndex, pointIndex, point) < int(point):
                lowPoint = False
            elif lookRight(heightMap, heightLineIndex, pointIndex, point) < int(point):
                lowPoint = False

            if lowPoint:
                if point != '9': # Case when 9 is around other 9
                    riskLevelSum += int(point)+1
                    nbLowPoint += 1
    print("SumRisk : ", riskLevelSum)
    print("nbLow : ", nbLowPoint)



if __name__ == '__main__':
    main()
