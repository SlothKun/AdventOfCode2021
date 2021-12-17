#!/usr/bin/env python3

class PacketParser:
    def __init__(self, binPacket=""):
        self.binPacket = binPacket
        self.version = ""
        self.packetId = ""
        self.lengthId = ""
        self.subPacketLength = ""
        self.subPacketNb = ""
        self.literalValue = 0
        self.subPackets = []

    def convertToDec(self, binValue):
        return int(binValue, 2)

    def getHeader(self):
        self.version = self.convertToDec(self.binPacket[:3])
        self.packetId = self.convertToDec(self.binPacket[3:6])
        self.binPacket = self.binPacket[6:]

    def getLengthId(self):
        self.lengthId = self.binPacket[:1]
        self.binPacket = self.binPacket[1:]

    def getSubPacketLength(self):
        self.subPacketLength = self.convertToDec(self.binPacket[:15])
        self.binPacket = self.binPacket[15:]

    def getSubPacketNb(self):
        self.subPacketNb = self.convertToDec(self.binPacket[:11])
        self.binPacket = self.binPacket[11:]

    def getLiteralValue(self):
        literalValue = ''
        stop = False
        while not stop:
            subPacket = self.binPacket[:5]
            self.binPacket = self.binPacket[5:]
            if subPacket[0] == '0':
                stop = True
            literalValue += subPacket[1:]
        print(f"{literalValue= }")
        return literalValue

    def parsePacket(self):
        print("--------")
        print(f"{self.binPacket=}")
        self.getHeader()
        print(f"{self.version=}")
        print(f"{self.packetId=}")
        if self.packetId == 4:
            self.literalValue = self.convertToDec(self.getLiteralValue())
            print(f"Converted {self.literalValue= }")
            print(f"{self.binPacket=}")
            self.subPackets.append(self.binPacket)
        else:
            self.getLengthId()
            if self.lengthId == '0':
                self.getSubPacketLength()
                print(f"{self.subPacketLength=}")
                print(f"{self.binPacket=}")
                self.subPackets.append(self.binPacket)
            else:
                self.getSubPacketNb()
                print(f"{self.subPacketNb=}")
                print(f"{self.binPacket=}")
                self.subPackets.append(self.binPacket)
        return self.version, self.subPackets

def convertToBinary(hexPacket):
    return bin(int('1'+hexPacket, 16))[3:]

def getPacketVersion(encPacket):
    packetParser = PacketParser(encPacket)
    packetVersion, subPackets = packetParser.parsePacket()
    for packet in subPackets:
        if packet.count('0') != len(packet):
            packetVersion += getPacketVersion(packet)
    return packetVersion


def main():
    inputPacket = ""
    with open('input.txt', 'r') as inputFile:
        inputPacket = convertToBinary(inputFile.readline().rstrip())
    answer = getPacketVersion(inputPacket)
    print(f"{answer=}")

if __name__ == '__main__':
    main()
