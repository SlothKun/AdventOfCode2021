#!/usr/bin/env python3

class Beacon:
    def __init__(self, coordinates, scannerName):
        self.constCoor = coordinates
        self.absoluteCoor = (None, None, None)
        self.allPosCoor = []
        self.scannerInRange = {}
        self.loadPosCoordinates()
        self.addScannerInRange(scannerName, coordinates)

    def __eq__(self, other):
        return self.absoluteCoor == other.getAbsoluteCoor()

    def getConstCoor(self):
        return self.constCoor

    def getAbsoluteCoor(self):
        return self.absoluteCoor

    def getScannerInRange(self):
        return self.scannerInRange

    def getAllPosCoordinates(self):
        return self.allPosCoor

    def getPosCoordinates(self, index):
        return self.allPosCoor[index]

    def compareConstCoor(self, secondBeacon):
        return self.constCoor == secondBeacon.getConstCoor()

    def compareAbsoluteCoor(self, secondBeaconPos):
        return self.absoluteCoor == secondBeaconPos

    def loadPosCoordinates(self):
        # Facing +x
        self.allPosCoor.append((self.constCoor[0], self.constCoor[1], self.constCoor[2])) # Rot : 0
        self.allPosCoor.append((self.constCoor[0], self.constCoor[2], -self.constCoor[1])) # Rot : 90
        self.allPosCoor.append((self.constCoor[0], -self.constCoor[1], -self.constCoor[2])) # Rot : 180
        self.allPosCoor.append((self.constCoor[0], -self.constCoor[2], self.constCoor[1])) # Rot : 270
        # Facing -x
        self.allPosCoor.append((-self.constCoor[0], -self.constCoor[1], self.constCoor[2])) # Rot : 0
        self.allPosCoor.append((-self.constCoor[0], self.constCoor[2], self.constCoor[1])) # Rot : 90
        self.allPosCoor.append((-self.constCoor[0], self.constCoor[1], -self.constCoor[2])) # Rot : 180
        self.allPosCoor.append((-self.constCoor[0], -self.constCoor[2], -self.constCoor[1])) # Rot : 270
        # Facing +y
        self.allPosCoor.append((self.constCoor[1], -self.constCoor[0], self.constCoor[2])) # Rot : 0
        self.allPosCoor.append((self.constCoor[1], self.constCoor[2], self.constCoor[0])) # Rot : 90
        self.allPosCoor.append((self.constCoor[1], self.constCoor[0], -self.constCoor[2])) # Rot : 180
        self.allPosCoor.append((self.constCoor[1], -self.constCoor[2], -self.constCoor[0])) # Rot : 270
        # Facing -y
        self.allPosCoor.append((-self.constCoor[1], self.constCoor[0], self.constCoor[2])) # Rot : 0
        self.allPosCoor.append((-self.constCoor[1], self.constCoor[2], -self.constCoor[0])) # Rot : 90
        self.allPosCoor.append((-self.constCoor[1], -self.constCoor[0], -self.constCoor[2])) # Rot : 180
        self.allPosCoor.append((-self.constCoor[1], -self.constCoor[2], self.constCoor[0])) # Rot : 270
        # Facing +z
        self.allPosCoor.append((self.constCoor[2], self.constCoor[1], -self.constCoor[0])) # Rot : 0
        self.allPosCoor.append((self.constCoor[2], -self.constCoor[0], -self.constCoor[1])) # Rot : 90
        self.allPosCoor.append((self.constCoor[2], -self.constCoor[1], self.constCoor[0])) # Rot : 180
        self.allPosCoor.append((self.constCoor[2], self.constCoor[0], self.constCoor[1])) # Rot : 270
        # Facing -z
        self.allPosCoor.append((-self.constCoor[2], -self.constCoor[1], -self.constCoor[0])) # Rot : 0
        self.allPosCoor.append((-self.constCoor[2], -self.constCoor[0], self.constCoor[1])) # Rot : 90
        self.allPosCoor.append((-self.constCoor[2], self.constCoor[1], self.constCoor[0])) # Rot : 180
        self.allPosCoor.append((-self.constCoor[2], self.constCoor[0], -self.constCoor[1])) # Rot : 270

    def setAbsoluteCoordinates(self, posIndex, offset):
        self.absoluteCoor = (self.allPosCoor[posIndex][0]-offset[0],
                             self.allPosCoor[posIndex][1]-offset[1],
                             self.allPosCoor[posIndex][2]-offset[2])
        self.addScannerInRange('0', self.absoluteCoor)

    def addScannerInRange(self, scannerName, relativeCoor):
        if scannerName not in self.scannerInRange:
            self.scannerInRange[scannerName] = relativeCoor
