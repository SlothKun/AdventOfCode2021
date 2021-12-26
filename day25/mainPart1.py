#!/usr/bin/env python3

class Radar:
    def __init__(self):
        self.wholeMap = []
        self.nbCol = 0
        self.nbLine = 0
        self.step = 0
        self.moved = True

    def __str__(self):
        return f"Answer : {self.step}"

    def loadMap(self, filePath):
        with open(filePath, 'r') as fileInput:
            for line in fileInput:
                if self.nbCol == 0:
                    self.nbCol = len(line.rstrip())
                self.nbLine += 1
                col = [c for c in line.rstrip()]
                self.wholeMap.append(col)
        print(f"{self.nbCol=}")
        print(f"{self.nbLine=}")

    def getNextLine(self, line):
        return (line+1) % self.nbLine

    def getNextCol(self, col):
        return (col+1) % self.nbCol

    def printMap(self):
        for line in self.wholeMap:
            print("".join(line))

    def moveCucumber(self, cucumber):
        tmpMap = [[col for col in row] for row in self.wholeMap]
        for lineIndex, line in enumerate(self.wholeMap):
            for colIndex, col in enumerate(line):
                if cucumber == "v" and col == "v":
                    if self.wholeMap[self.getNextLine(lineIndex)][colIndex] == '.':
                        tmpMap[lineIndex][colIndex] = '.'
                        tmpMap[self.getNextLine(lineIndex)][colIndex] = 'v'
                        self.moved = True
                elif cucumber == ">" and col == ">":
                    if self.wholeMap[lineIndex][self.getNextCol(colIndex)] == '.':
                        tmpMap[lineIndex][colIndex] = '.'
                        tmpMap[lineIndex][self.getNextCol(colIndex)] = '>'
                        self.moved = True
        self.wholeMap = tmpMap

    def getAnswer(self):
        print("Start")
        self.printMap()
        while self.moved:
            self.moved = False
            self.moveCucumber(">")
            self.moveCucumber("v")
            self.step += 1
            print(f"\n{self.step=}")
            self.printMap()


def main():
    radar = Radar()
    radar.loadMap("input.txt")
    radar.getAnswer()
    #radar.printMap()
    print(radar)

if __name__ == '__main__':
    main()
