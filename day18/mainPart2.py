#!/usr/bin/env python3
import re
import math

RE_SPLIT = "[1-9][0-9]+"
RE_NB = "[0-9]+"
RE_PAIR = "\[[0-9]+,[0-9]+\]"

class Combinator:
    def __init__(self):
        self.snailfishNb = ""
        self.nextNb = []
        self.startPairIndex = ""
        self.endPairIndex = ""
        self.nbLeftIndex = ""
        self.nbRightIndex = ""
        self.bestMagnitude = 0

    def loadNb(self, filepath):
        with open(filepath, 'r') as fileInput:
            fileInput = fileInput.readlines()
            for nb in fileInput:
                self.nextNb.append(nb.rstrip())

    def checkDepth(self):
        depth = 0
        for index, letter in enumerate(self.snailfishNb):
            if letter == '[':
                depth += 1
            elif letter == ']':
                depth -= 1

            if depth == 5:
                return index
        return None

    def getNbAtLeft(self, endIndex):
        allNbMatch = re.finditer(RE_NB, self.snailfishNb[:endIndex])
        match = ''
        for match in allNbMatch:
            pass
        if match == '':
            return None
        else:
            return (match.span()[0], match.span()[1])

    def getNbAtRight(self, beginIndex):
        match = re.search(RE_NB, self.snailfishNb[beginIndex:])
        if match:
            return (beginIndex+match.span()[0], beginIndex+match.span()[1])
        else:
            return None

    def removeSubstring(self, begin, end):
        self.snailfishNb = self.snailfishNb[:begin] + self.snailfishNb[end:]
        return (begin - end)

    def addSubstring(self, begin, substring):
        self.snailfishNb = self.snailfishNb[:begin] + substring + self.snailfishNb[begin:]
        return len(substring)

    def updateIndexes(self, modifier):
        self.startPairIndex = self.startPairIndex+modifier if self.startPairIndex else None
        self.endPairIndex = self.endPairIndex+modifier if self.endPairIndex else None
        self.nbLeftIndex = (self.nbLeftIndex[0]+modifier, self.nbLeftIndex[1]+modifier) if self.nbLeftIndex else None
        self.nbRightIndex = (self.nbRightIndex[0]+modifier, self.nbRightIndex[1]+modifier) if self.nbRightIndex else None

    def explodeNb(self, startPairIndex):
        self.startPairIndex = startPairIndex
        # End the ']' char
        self.endPairIndex = self.snailfishNb[startPairIndex:].find(']') + self.startPairIndex + 1
        # get nb into int (the + and - is for removing [])
        pair = [int(nb) for nb in self.snailfishNb[self.startPairIndex+1:self.endPairIndex-1].split(',')]
        self.nbLeftIndex = self.getNbAtLeft(self.startPairIndex)
        self.nbRightIndex = self.getNbAtRight(self.endPairIndex)
        if self.nbLeftIndex:
            newNb = str(int(self.snailfishNb[self.nbLeftIndex[0]:self.nbLeftIndex[1]]) + pair[0])
            indexModifier = self.removeSubstring(self.nbLeftIndex[0], self.nbLeftIndex[1])
            indexModifier += self.addSubstring(self.nbLeftIndex[0], newNb)
            self.updateIndexes(indexModifier)
        if self.nbRightIndex:
            newNb = str(int(self.snailfishNb[self.nbRightIndex[0]:self.nbRightIndex[1]]) + pair[1])
            self.removeSubstring(self.nbRightIndex[0], self.nbRightIndex[1])
            self.addSubstring(self.nbRightIndex[0], newNb)
        indexModifier = self.removeSubstring(self.startPairIndex, self.endPairIndex)
        self.updateIndexes(indexModifier)
        self.addSubstring(self.endPairIndex, '0')

    def splitNb(self, regularMatch):
        regularNb = int(regularMatch.group(0))
        regularIndexes = regularMatch.span()
        self.removeSubstring(regularIndexes[0], regularIndexes[1])
        newPair = '[' + str(math.floor(regularNb/2)) + ',' + str(math.ceil(regularNb/2)) + ']'
        self.addSubstring(regularIndexes[0], newPair)

    def checkReduce(self):
        reduced = True
        while reduced:
            reduced = False
            explodeMatch = self.checkDepth()
            splitMatch = re.search(RE_SPLIT, self.snailfishNb)
            if explodeMatch:
                self.explodeNb(explodeMatch)
                reduced = True
            elif splitMatch:
                self.splitNb(splitMatch)
                reduced = True

    def addNbs(self):
        for firstNbIndex, firstNb in enumerate(self.nextNb):
            for secondNbIndex, secondNb in enumerate(self.nextNb):
                if firstNbIndex != secondNbIndex:
                    self.snailfishNb = '['+ firstNb + ',' + secondNb + ']'
                    print(f"{self.snailfishNb=}")
                    self.checkReduce()
                    self.getMagnitude()

    def getMagnitude(self):
        matched = True
        while matched:
            matched = False
            allPairMatch = re.finditer(RE_PAIR, self.snailfishNb)
            match = ''
            for match in allPairMatch:
                pass
            if match != '':
                matched = True
                matchIndex = match.span()
                pair = [int(nb) for nb in self.snailfishNb[matchIndex[0]+1:matchIndex[1]-1].split(',')]
                magnitude = 3*pair[0] + 2*pair[1]
                indexModifier = self.removeSubstring(matchIndex[0], matchIndex[1])
                self.addSubstring(matchIndex[0], str(magnitude))
        print("last magnitude : ", self.snailfishNb)
        if int(self.snailfishNb) > self.bestMagnitude:
            self.bestMagnitude = int(self.snailfishNb)
        print("bestMagnitude : ", self.bestMagnitude)




def main():
    combinator = Combinator()
    combinator.loadNb('input.txt')
    combinator.addNbs()
    combinator.getMagnitude()


if __name__ == '__main__':
    main()
