#!/usr/bin/env python3
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=5)

class Paper:
    def __init__(self):
        self.page = []
        self.marks = []
        self.folds = []
        self.dims = ()

    def loadData(self):
        with open("input.txt", 'r') as inputFile:
            for line in inputFile:
                if len(line.rstrip()) != 0:
                    if "fold along" in line:
                        line = line.rstrip().replace("fold along ", '')
                        foldInfo = line.split('=')
                        self.folds.append({ 'axis': foldInfo[0], 'value': int(foldInfo[1]) })
                    else:
                        coordinates = tuple(int(coor) for coor in (line.rstrip().split(',')))
                        self.marks.append(coordinates)

    def getPageDimensions(self):
        for i in range(2):
            self.marks.sort(key=lambda a: a[i])
            self.dims += (self.marks[-1][i] + 1,)

    def createPage(self):
        self.page = np.full((self.dims[1], self.dims[0]), '.')

    def placeMarks(self):
        # x move horizontally
        # y move vertically
        for y, x in self.marks:
            self.page[x][y] = '■'

    def mergePages(self, pagePart):
        for yIndex, yValue in enumerate(pagePart):
            for xIndex, xValue in enumerate(pagePart[yIndex]):
                if xValue == "■":
                    self.page[yIndex, xIndex] = "■"

    def foldHorizontally(self, lineIndex):
        # When y = colIndex
        print("------ FOLd ------")
        modifiedArray = np.delete(self.page, lineIndex, 0)
        self.page, pagePart = np.vsplit(modifiedArray, [lineIndex])
        pagePart = np.flipud(pagePart)
        self.mergePages(pagePart)

    def foldVertically(self, colIndex):
        # When x = colIndex
        print("------ FOLd ------")
        modifiedArray = np.delete(self.page, colIndex, 1)
        self.page, pagePart = np.hsplit(modifiedArray, [colIndex])
        pagePart = np.fliplr(pagePart)
        self.mergePages(pagePart)

    def countMarks(self):
        return (self.page == '#').sum()

    def splitLetters(self):
        indexes = [i for i in range(0, (5*8), 5)]
        print(indexes)
        let = np.hsplit(self.page, indexes)
        for letter in let:
            pp.pprint(letter.tolist())
            print("----")
    
    def main(self):
        self.loadData()
        self.getPageDimensions()
        self.createPage()
        self.placeMarks()
        pp.pprint(self.page)
        for fold in self.folds:
            if fold["axis"] == 'y':
                self.foldHorizontally(fold["value"])
            else:
                self.foldVertically(fold["value"])
            ## PART 1
            print("Marks : ", self.countMarks())
        ## PART 2
        self.splitLetters()

if __name__ == '__main__':
    paper = Paper()
    paper.main()


# not FAGURZME
# not PAGURZME
