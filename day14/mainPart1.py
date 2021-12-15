#!/usr/bin/env python3

class Polymerization:
    def __init__(self):
        self.polymer = ""
        self.rules = {}
        self.lettersCount = {}

    def loadData(self):
        with open("input.txt", 'r') as inputFile:
            lines = inputFile.readlines()
            self.polymer = lines[0].rstrip()
            for line in lines[2:]:
                data = line.rstrip().split(" -> ")
                self.rules[data[0]] = data[1]

    def countLetters(self, letter):
        if letter in self.lettersCount:
            self.lettersCount[letter] += 1
        else:
            self.lettersCount[letter] = 1

    def enforceRules(self):
        newPolymer = self.polymer
        for step in range(10):
            firstChar = self.polymer[0]
            secondChar = ''
            marge = 1
            for index, char in enumerate(self.polymer[1:]):
                secondChar = char
                charPair = firstChar + secondChar
                if self.rules[charPair]:
                    self.countLetters(self.rules[charPair])
                    newPolymer = newPolymer[:index+marge] + self.rules[charPair] + newPolymer[index+marge:]
                    marge += 1
                firstChar = secondChar
                #print(newPolymer)
            self.polymer = newPolymer


    def getPartOneAnswer(self):
        # Sort dict by value
        self.lettersCount = sorted(self.lettersCount.items(), key=lambda x:x[1])
        print(self.lettersCount)
        print(f"Results : {self.lettersCount[-1][1] - self.lettersCount[0][1]}")
        print("nb of letter : ", len(self.polymer))

    def main(self):
        self.loadData()
        for let in self.polymer:
            self.countLetters(let)
        self.enforceRules()
        self.getPartOneAnswer()
        for key in self.rules.keys():
            print(f"{key=} - {self.polymer.count(key)}")


if __name__ == '__main__':
    polymerization = Polymerization()
    polymerization.main()
