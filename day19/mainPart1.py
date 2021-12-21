#!/usr/bin/env python3
from scanner import Scanner
import re
import timeit

RE_NB = "[0-9]+"
MAX_POS = 24
FILEPATH = "testInput.txt"

class ScannerManager:
    def __init__(self):
        self.uniqueBeacons = []
        self.scanners = []
        self.matchedScanners = 1

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
            #for uniqueIndex, uniqueBeacon in enumerate(self.uniqueBeacons):
                #if beacon.getAbsoluteCoor() == uniqueBeacon.getAbsoluteCoor(): # if in the Unique list
                #    for scanner in beacon.getScannerInRange():
                #        # Update scanner in range list
                #        self.uniqueBeacons[uniqueIndex].addScannerInRange(scanner)
                #else: # if not
                #    print("hhh")
            self.uniqueBeacons.append(beacon) # Add it

    def setReferencePoint(self):
        self.scanners[0].setAbsoluteCoordinates((0,0,0)) # Scanner 0 is the reference point
        self.scanners[0].setOffset((0,0,0)) # Scanner 0 is the reference point
        self.scanners[0].setBeaconsAbsoluteCoor() # So its beacons won't change coordinates
        self.addToUniqueBeacon(self.scanners[0].getBeaconList())
        print(self.uniqueBeacons)
        self.scanners[0].setScannerFromZero() # Flip state, might be handy


    def findIntersect(self):
        for scannerIndex, scanner in enumerate(self.scanners[1:]): # Exclude scanner 0
            intersect = False
            if not scanner.isSet():
                beaconList = scanner.getBeaconList()
                for posIndex in range(MAX_POS): # Position index, include rotation & face
                    for beacon in beaconList:
                        rotatedBeaconPos = beacon.getPosCoordinates(posIndex) # Get position rotated by posIndex
                        for uniqueBeacon in self.uniqueBeacons:
                            offset = tuple(map(lambda i, j: i - j, rotatedBeaconPos, uniqueBeacon.getAbsoluteCoor())) # V1
                            #print(offset)
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
                                # activate flag
                                intersect = True
                                # Beacon that matched mean that they are already in unique
                                # For them, we need to only update coorByScanner with their relative pos to x scanner
                                print("match found : ", len(matchFound))
                                print("Unique bef : ", len(self.uniqueBeacons))
                                for matchedBeacon in matchFound:
                                    if matchedBeacon[1] in self.uniqueBeacons:
                                        print("h ?")
                                        uniqueIndex = self.uniqueBeacons.index(matchedBeacon[1])
                                        self.uniqueBeacons[uniqueIndex].addScannerInRange(scanner.getName(), matchedBeacon[0].getConstCoor())
                                        #print(self.uniqueBeacons[uniqueIndex].scannerInRange)
                                print("Unique aft : ", len(self.uniqueBeacons))
                                # For the rest, we need to set them relative to 0 and add them to unique
                                # Don't forget to set the Scanner too, while saving all necessary data in it
                                # Set Scanner
                                print(len(self.uniqueBeacons))
                                self.scanners[scannerIndex+1].anchorScanner(offset, posIndex)
                                print(self.scanners[scannerIndex+1].name)
                                matchedScannerBeaconList = self.scanners[scannerIndex+1].getBeaconList()
                                self.matchedScanners += 1
                                uniqueAbsoluteCoor = [beacon.getAbsoluteCoor() for beacon in self.uniqueBeacons]
                                print(uniqueAbsoluteCoor)
                                for matchedScannerBeacon in matchedScannerBeaconList:
                                    print(matchedScannerBeacon.getAbsoluteCoor())
                                    if matchedScannerBeacon.getAbsoluteCoor() not in uniqueAbsoluteCoor:
                                        self.uniqueBeacons.append(matchedScannerBeacon)
                                print(len(self.uniqueBeacons))
                                break
                        if intersect:
                            break
                    if intersect:
                        break


def main():
    start = timeit.default_timer()
    scannerManager = ScannerManager()
    scannerManager.loadScanners()
    scannerManager.setReferencePoint()
    while scannerManager.matchedScanners != len(scannerManager.scanners):
        scannerManager.findIntersect()
    print("answer: ",len(scannerManager.uniqueBeacons))
    print("Time : ", timeit.default_timer() - start)

if __name__ == '__main__':
    main()
