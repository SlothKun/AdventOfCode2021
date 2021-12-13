#!/usr/bin/env python3
import pprint

pp = pprint.PrettyPrinter(indent=3)
paths = []
pathsFound = 0

class Cave:
    def __init__(self):
        self.caveMap = {}
        self.pathsFound = 0

    def loadCaveMap(self, filePath):
        # Get all possible cave link and put them in a dict
        inputLink = {1:0, 0:1}
        with open(filePath, 'r') as inputFile:
            for line in inputFile:
                caveConn = line.rstrip().split('-')
                for index, conn in enumerate(caveConn):
                    if conn in self.caveMap:
                        self.caveMap[conn].append(caveConn[inputLink[index]])
                    else:
                        self.caveMap[conn] = [caveConn[inputLink[index]]]

    def cleanCaveMap(self):
        # get rid of end as key
        self.caveMap.pop("end")
        # Get rid of start inside conn
        for key, value in self.caveMap.items():
            if "start" in value:
                self.caveMap[key].remove("start")

    def findWays(self, point, visited):
        copyVisited = visited + [point]
        for newWays in self.caveMap[point]:
            if newWays == "end":
                print(copyVisited + ["end"])
                self.pathsFound += 1
            elif not (newWays in copyVisited and newWays.islower()):
                self.findWays(newWays, copyVisited)

    def main(self):
        self.loadCaveMap("input.txt")
        self.cleanCaveMap()
        for startPoint in self.caveMap["start"]:
            self.findWays(startPoint, ['start'])
        print(self.pathsFound)


if __name__ == '__main__':
    cave = Cave()
    cave.main()
