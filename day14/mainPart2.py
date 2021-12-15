#!/usr/bin/env python3
import math

class Polymerization:
    def __init__(self):
        self.polymer = ""
        self.rules = {}
        self.pairsCount = {}
        self.lettersCount = {}
        self.globalCount = 0
        self.firstAndLastLet = []

    def loadData(self):
        with open("input.txt", 'r') as inputFile:
            lines = inputFile.readlines()
            self.polymer = lines[0].rstrip()
            self.firstAndLastLet = [self.polymer[0], self.polymer[-1]]
            for line in lines[2:]:
                data = line.rstrip().split(" -> ")
                self.pairsCount[data[0]] = self.polymer.count(data[0])
                self.rules[data[0]] = [data[0][0] + data[1], data[1] + data[0][1]]

    def cleanRules(self):
        for key, values in self.rules.items():
            for value in values:
                if value not in self.rules.keys():
                    self.rules[key].remove(value)

    def countLetters(self):
        self.globalCount = -2
        for pair, count in self.pairsCount.items():
            self.globalCount += count
            for letter in pair:
                if letter in self.lettersCount:
                    self.lettersCount[letter] += count
                else:
                    if letter in self.firstAndLastLet:
                        self.lettersCount[letter] = count + 1
                    else:
                        self.lettersCount[letter] = count

    def clearDict(self):
        emptyPairsCount = {}
        for key in self.pairsCount.keys():
            emptyPairsCount[key] = 0
        return emptyPairsCount

    def enforceRules(self):
        for step in range(40):
            tmpPairsCount = self.clearDict()
            for pair, count in self.pairsCount.items():
                if count > 0:
                    for ruleValue in self.rules[pair]:
                        tmpPairsCount[ruleValue] += count
            self.pairsCount = tmpPairsCount

    def getAnswer(self):
        # Sort dict by value
        self.lettersCount = sorted(self.lettersCount.items(), key=lambda x:x[1])
        print("---- Results ----")
        print(self.lettersCount)
        print(f"Results : {(self.lettersCount[-1][1] - self.lettersCount[0][1])/2}")
        print("global count : ", self.globalCount)

    def main(self):
        self.loadData()
        self.cleanRules() # Not sure if necesary but well
        self.enforceRules()
        print(self.pairsCount)
        self.countLetters()
        self.getAnswer()


if __name__ == '__main__':
    polymerization = Polymerization()
    polymerization.main()
