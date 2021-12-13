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

    def checkRules(self, path, newPoint):
        #print("--- Check rules ---")
        #print(f"{(path+[newPoint])=}")
        found = []
        alreadyDuplicate = False
        for point in (path+[newPoint]):
            found.append(point)
            if found.count(point) >= 2 and point.islower() and alreadyDuplicate:
                #print("--- False : Quitting ---")
                return False
            elif found.count(point) >= 2 and point.islower() and not alreadyDuplicate:
                alreadyDuplicate = True
        #print("--- True : Quitting ---")
        return True

    def findWays(self, point, visited):
        copyVisited = visited + [point]
        for newWay in self.caveMap[point]:
            if newWay == "end":
                print(copyVisited + ["end"])
                self.pathsFound += 1
            elif self.checkRules(copyVisited, newWay):
                self.findWays(newWay, copyVisited)



    def main(self):
        self.loadCaveMap("input.txt")
        self.cleanCaveMap()
        for startPoint in self.caveMap["start"]:
            self.findWays(startPoint, ['start'])
        print(self.pathsFound)


if __name__ == '__main__':
    cave = Cave()
    cave.main()
