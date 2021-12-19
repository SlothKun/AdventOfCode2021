#!/usr/bin/env python3
import timeit

MAX_X = 500
MAX_Y = 500

class Probe:
    def __init__(self, targetCoor, velocity):
        self.targetCoor = targetCoor
        self.velocity = velocity
        self.currentCoor = (0, 0)
        self.highestY = 0
        self.allCoor = []
        self.inTarget = False
        self.outOfRange = False

    def getHighestY(self):
        return self.highestY

    def updateVelocity(self):
        newX = self.velocity[0]
        newY = self.velocity[1] - 1 # decrease y velocity by 1
        if self.velocity[0] > 0:
            newX -= 1
        elif self.velocity[0] < 0:
            newX += 1
        self.velocity = (newX, newY)

    def updateCoordinates(self):
        newX = self.currentCoor[0] + self.velocity[0]
        newY = self.currentCoor[1] + self.velocity[1]
        self.currentCoor = (newX, newY)

    def checkCoordinates(self):
        if self.targetCoor[0][0] <= self.currentCoor[0] <= self.targetCoor[0][1] and \
            self.targetCoor[1][0] <= self.currentCoor[1] <= self.targetCoor[1][1]:
            self.inTarget = True
        elif self.currentCoor[0] > self.targetCoor[0][1] or self.currentCoor[1] < self.targetCoor[1][0]:
            self.outOfRange = True

    def checkHighestHeight(self):
        if self.currentCoor[1] > self.highestY:
            self.highestY = self.currentCoor[1]

    def move(self):
        #print("-- Move --")
        while not self.inTarget and not self.outOfRange:
            self.updateCoordinates()
            #print(f"{self.currentCoor=}")
            self.checkCoordinates()
            #print(f"{self.inTarget=}")
            #print(f"{self.outOfRange=}\n")
            if not self.inTarget and not self.outOfRange:
                self.checkHighestHeight()
                self.allCoor.append(self.currentCoor)
                self.updateVelocity()
        return self.inTarget


class ProbeLauncher:
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.targetCoor = []
        self.probeOnTarget = 0

    def loadTarget(self):
        with open(self.inputFile, 'r') as inputFile:
            parsedFile = inputFile.readline().rstrip().split(': ')
            parsedFile = parsedFile[1].split(', ')
            for i in range(2):
                coor = parsedFile[i][2:].split('..')
                self.targetCoor.append((int(coor[0]), int(coor[1])))
            print("target : ", self.targetCoor)

    def launchProbes(self):
        x = 0
        while x < MAX_X: # While it hasn't attained the point of non touching
            x += 1
            y = -250
            while y < MAX_Y:
                probe = Probe(self.targetCoor, (x,y))
                if probe.move():
                    #print(f'On Target :{(x,y)=}')
                    self.probeOnTarget += 1
                y += 1
        print("answer : ", self.probeOnTarget)

    def testProbes(self): # Test certains coordinates
        probe = Probe(self.targetCoor, (7, -1))
        print(probe.move())




def main():
    probeLauncher = ProbeLauncher("input.txt")
    probeLauncher.loadTarget()
    probeLauncher.launchProbes()
    #probeLauncher.testProbes()

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    print("Time : ", timeit.default_timer() - start)
