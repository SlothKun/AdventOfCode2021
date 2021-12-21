#!/usr/bin/env python3
from scanner import Scanner
import re
import threading
import timeit

RE_NB = "[0-9]+"
MAX_POS = 24
FILEPATH = "input.txt"


class ScannerManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.uniqueBeacons = []
        self.scanners = []
        self.matchedScanners = 1
        self.bestMDistance = 0

    def translatePoint(self, point, offset):
        return (point[0]-offset[0], point[1]-offset[1], point[2]-offset[2])

    def loadScanners(self):
        with open(FILEPATH, 'r') as inputFile:
            for line in inputFile:
                if "--" in line:
                    scannerName = int((re.search(RE_NB, line)).group(0))
                    self.scanners.append(Scanner(scannerName))
                elif len(line) > 1:
                    coordinates = [int(i) for i in line.rstrip().split(',')]
                    self.scanners[-1].loadBeacon(coordinates)
        print(f"{len(self.scanners)} scanners loaded.")

    def addToUniqueBeacon(self, beaconList):
        for beacon in beaconList:
            self.uniqueBeacons.append(beacon) # Add it

    def setReferencePoint(self):
        self.scanners[0].setAbsoluteCoordinates((0,0,0)) # Scanner 0 is the reference point
        self.scanners[0].setOffset((0,0,0)) # Scanner 0 is the reference point
        self.scanners[0].setBeaconsAbsoluteCoor() # So its beacons won't change coordinates
        self.addToUniqueBeacon(self.scanners[0].getBeaconList())
        self.scanners[0].setScannerFromZero() # Flip state, might be handy


    def findIntersect(self, scannerIndex):
        scanner = self.scanners[scannerIndex]
        intersect = False
        if not scanner.isSet():
            beaconList = scanner.getBeaconList()
            for posIndex in range(MAX_POS): # Position index, include rotation & face
                for beacon in beaconList:
                    rotatedBeaconPos = beacon.getPosCoordinates(posIndex) # Get position rotated by posIndex
                    for uniqueBeacon in self.uniqueBeacons:
                        offset = tuple(map(lambda i, j: i - j, rotatedBeaconPos, uniqueBeacon.getAbsoluteCoor())) # V1
                        matchFound = [[beacon, uniqueBeacon]]
                        tmpUniqueBeacons = self.uniqueBeacons[:] # Create a copy by value
                        tmpUniqueBeacons.remove(uniqueBeacon)
                        for secondBeacon in beaconList:
                            if not beacon.compareConstCoor(secondBeacon):
                                rotatedSecondBeaconPos = secondBeacon.getPosCoordinates(posIndex) # Get position rotated by posIndex
                                translatedCoor = self.translatePoint(rotatedSecondBeaconPos, offset)
                                for secondUniqueBeacon in tmpUniqueBeacons:
                                    if secondUniqueBeacon.compareAbsoluteCoor(translatedCoor):
                                        # Same point, Match, we can stop looking
                                        matchFound.append([secondBeacon, secondUniqueBeacon])
                                        tmpUniqueBeacons.remove(secondUniqueBeacon)
                                        break
                        if len(matchFound) >= 12:
                            print("intersect")
                            self.lock.acquire()
                            # activate flag
                            intersect = True
                            # Beacon that matched mean that they are already in unique
                            # For them, we need to only update coorByScanner with their relative pos to x scanner
                            for matchedBeacon in matchFound:
                                if matchedBeacon[1] in self.uniqueBeacons:
                                    uniqueIndex = self.uniqueBeacons.index(matchedBeacon[1])
                                    self.uniqueBeacons[uniqueIndex].addScannerInRange(scanner.getName(), matchedBeacon[0].getConstCoor())
                            # For the rest, we need to set them relative to 0 and add them to unique
                            # Don't forget to set the Scanner too, while saving all necessary data in it
                            # Set Scanner
                            self.scanners[scannerIndex].anchorScanner(offset, posIndex)
                            matchedScannerBeaconList = self.scanners[scannerIndex].getBeaconList()
                            self.matchedScanners += 1
                            uniqueAbsoluteCoor = [beacon.getAbsoluteCoor() for beacon in self.uniqueBeacons]
                            for matchedScannerBeacon in matchedScannerBeaconList:
                                if matchedScannerBeacon.getAbsoluteCoor() not in uniqueAbsoluteCoor:
                                    self.uniqueBeacons.append(matchedScannerBeacon)
                            print("Unique Beacon : ", len(self.uniqueBeacons))
                            self.lock.release()
                            return intersect
        return intersect

    def getLargestManhattanDistance(self):
        for scannerOne in self.scanners:
            for scannerTwo in self.scanners:
                mDist = sum(abs(val1-val2) for val1,val2 in zip(scannerOne.getAbsoluteCoor(), scannerTwo.getAbsoluteCoor()))
                self.bestMDistance = mDist if mDist > self.bestMDistance else self.bestMDistance
        return self.bestMDistance

def main():
    scannerManager = ScannerManager()
    scannerManager.loadScanners()
    scannerManager.setReferencePoint()

    while scannerManager.matchedScanners != len(scannerManager.scanners):
        threads = []
        for i in range(1, len(scannerManager.scanners)):
            threads.append(threading.Thread(target=scannerManager.findIntersect(i), name=('Scanner '+str(i))))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    print("answer: ",len(scannerManager.uniqueBeacons))
    mDist = scannerManager.getLargestManhattanDistance()
    print("mDist : ", mDist)

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    print("Time : ", timeit.default_timer() - start)
