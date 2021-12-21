#!/usr/bin/env python3
from beacon import Beacon

class Scanner:
    def __init__(self, name):
        self.name = name
        self.beaconInRange = []
        self.offset = 0
        self.posIndex = 0
        self.absoluteCoor = (None, None, None)
        self.setFromZero = False

    def getName(self):
        return self.name

    def getFirstBeacon(self):
        return self.beaconInRange[0]

    def getBeaconList(self):
        return self.beaconInRange

    def isSet(self):
        return self.setFromZero

    def loadBeacon(self, coordinates):
        coordinates = (coordinates[0], coordinates[1], coordinates[2])
        self.beaconInRange.append(Beacon(coordinates, self.name))

    def setAbsoluteCoordinates(self, coordinates):
        self.absoluteCoor = coordinates

    def anchorScanner(self, offset, posIndex):
        self.setOffset(offset)
        self.setPosIndex(posIndex)
        self.setBeaconsAbsoluteCoor()
        self.setScannerFromZero()
        #for beacon in self.beaconInRange:
        #    if intersection[0] == beacon.getAbsoluteCoor():
        #        scannerCoor = tuple(map(lambda i, j: i + j, beacon.getConstCoor(), intersection[0]))
        #        print("Scanner Coor : ", scannerCoor)
        self.setAbsoluteCoordinates(offset)

    def setScannerFromZero(self):
        self.setFromZero = True

    def setOffset(self, offset):
        self.offset = offset

    def setPosIndex(self, posIndex):
        self.posIndex = posIndex

    def setBeaconsAbsoluteCoor(self):
        for beacon in self.beaconInRange:
            beacon.setAbsoluteCoordinates(self.posIndex, self.offset)
