#!/usr/bin/env python3
import pprint
import itertools

pp = pprint.PrettyPrinter(indent=4)

octoGrid = []

class OctoGrid:
    def __init__(self):
        self.grid = []
        self.flashCount = 0
        self.alreadyFlashed = []

    def clearAlreadyFlashed(self):
        self.alreadyFlashed = []

    def loadGrid(self):
        with open("input.txt", 'r') as inputFile:
            for line in inputFile:
                self.grid.append([int(octo) for octo in line.rstrip()])

    def updateGrid(self, lineIndex, colIndex, value):
        self.grid[lineIndex][colIndex] = value

    def getGridValue(self, lineIndex, colIndex):
        return self.grid[lineIndex][colIndex]

    def isFlash(self, octo):
        if octo == 10:
            self.flashCount += 1
            return 0
        else:
            return octo

    def isAlreadyFlashed(self, coordinates):
        return True if coordinates in self.alreadyFlased else False

    def incrementWholeGrid(self):
        for lineIndex, line in enumerate(self.grid):
            for colIndex, col in enumerate(line):
                octo = self.isFlash(col+1)
                if octo == 0:
                    self.alreadyFlashed.append((lineIndex, colIndex))
                self.updateGrid(lineIndex, colIndex, octo)

    def getLineMinMax(self, lineIndex):
        lineMin = lineIndex-1 if lineIndex-1 >= 0 else 0
        lineMax = lineIndex+2 if lineIndex+2 <= len(self.grid) else len(self.grid)
        return (lineMin, lineMax)

    def getColMinMax(self, colIndex):
        colMin = colIndex-1 if colIndex-1 >= 0 else 0
        colMax = colIndex+2 if colIndex+2 <= len(self.grid[0]) else len(self.grid[0])
        return (colMin, colMax)

    def getNeighbours(self, targetLineIndex, targetColIndex):
        neighbours = []
        lineMinMax = self.getLineMinMax(targetLineIndex)
        colMinMax = self.getColMinMax(targetColIndex)
        for lineIndex in range(lineMinMax[0], lineMinMax[1]):
            for colIndex in range(colMinMax[0], colMinMax[1]):
                if (lineIndex, colIndex) != (targetLineIndex, targetColIndex):
                    neighbours.append((lineIndex, colIndex))
        print(f"Neighbour for {targetLineIndex}:{targetColIndex} - {neighbours}")
        return neighbours

    def checkNeighbours(self, octo):
        neighbours = self.getNeighbours(octo[0], octo[1])
        for neighbour in neighbours:
            if neighbour not in self.alreadyFlashed:
                print(f"{neighbour=}")
                neighbourValue = self.getGridValue(neighbour[0], neighbour[1])
                neighbourValue = self.isFlash(neighbourValue+1)
                self.updateGrid(neighbour[0], neighbour[1], neighbourValue)
                if neighbourValue == 0:
                    self.alreadyFlashed.append(neighbour)


    def main(self):
        pp.pprint(self.grid)
        print("-----")
        for i in range(100):
            self.incrementWholeGrid()
            for flashed in self.alreadyFlashed:
                self.checkNeighbours(flashed)
            print("grid after : ")
            self.clearAlreadyFlashed()
        pp.pprint(self.grid)
        print(f"{self.flashCount=}")
                

if __name__ == '__main__':
    octoGrid = OctoGrid()
    octoGrid.loadGrid()
    octoGrid.main()
