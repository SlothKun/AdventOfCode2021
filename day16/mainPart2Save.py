#!/usr/bin/env python3
packetList = []

class PacketParser:
    def __init__(self, binPacket=""):
        self.binPacket = binPacket
        self.version = ""
        self.packetId = ""
        self.lengthId = ""
        self.subPacketLength = ""
        self.subPacketNb = 0
        self.literalValue = -1
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
        #print(f"{literalValue= }")
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
        else:
            self.getLengthId()
            print(f"{self.lengthId=}")
            if self.lengthId == '0':
                self.getSubPacketLength()
                self.subPacketNb = 2
                print(f"{self.subPacketLength=}")
            else:
                self.getSubPacketNb()
                print(f"{self.subPacketNb=}")
        return self.literalValue, self.packetId, self.subPacketNb, self.binPacket


def convertToBinary(hexPacket):
    return bin(int('1'+hexPacket, 16))[3:]

def applyOperation(operationId, values):
    print(f"{operationId=} - {values=}")
    answer = values[0]
    for value in values[1:]:
        if operationId == 0:
            print(f"{operationId=} : {answer} + {value}")
            answer += value
        elif operationId == 1:
            print(f"{operationId=} : {answer} * {value}")
            answer *= value
        elif operationId == 2:
            print(f"{operationId=} : {answer} <= {value}")
            answer = answer if answer <= value else value
        elif operationId == 3:
            print(f"{operationId=} : {answer} >= {value}")
            answer = answer if answer >= value else value
        elif operationId == 5:
            print(f"{operationId=} : {answer} > {value}")
            answer = 1 if answer > value else 0
        elif operationId == 6:
            print(f"{operationId=} : {answer} < {value}")
            answer = 1 if answer < value else 0
        elif operationId == 7:
            print(f"{operationId=} : {answer} == {value}")
            answer = 1 if answer == value else 0
    return answer

def getPacketList(encPacket):
    packetParser = PacketParser(encPacket)
    packetLitVal, packetId, subPacketNb, packet = packetParser.parsePacket()
    packetList.append({'id': packetId, 'value':packetLitVal})
    print(f"{packetLitVal=} - {packetId=} - {subPacketNb=} - {packet=}")
    if packet.count('0') != len(packet):
        getPacketList(packet)

def getPacketHierarchy():
    lp = None # Last packet
    depth = 0 # actual depth
    for index, packet in enumerate(packetList):
        packet['depth'] = depth
        packetList[index] = packet
        if lp is not None:
            if packet['id'] != 4 and lp['id'] == 4:
                print(f"{packet=} | {depth=}")
                packetList[depth-1]
                depth -= 1
                packetList[index]['depth'] = depth
        if packet['id'] != 4:
            depth += 1
        lp = packet

def main():
    inputPacket = ""
    with open('testInput2.txt', 'r') as inputFile:
        inputPacket = convertToBinary(inputFile.readline().rstrip())
    getPacketList(inputPacket)
    """
    packetList.append({'id':7, 'value':-1})
    packetList.append({'id':0, 'value':-1})
    packetList.append({'id':0, 'value':-1})
    packetList.append({'id':4, 'value':1})
    packetList.append({'id':4, 'value':1})
    packetList.append({'id':0, 'value':-1})
    packetList.append({'id':4, 'value':2})
    packetList.append({'id':4, 'value':2})
    packetList.append({'id':1, 'value':-1})
    packetList.append({'id':4, 'value':2})
    packetList.append({'id':4, 'value':3})
    """
    getPacketHierarchy()
    print("----------")
    for a in packetList:
        print(f"{a=}")

    #print(f"{getAnswer(1, packetList[0]['id'])= }")
    #print(getAnswer())


if __name__ == '__main__':
    main()


# 72103500

"""
# pIndex : packetIndex | opId : operationId
def getAnswer(pIndex, opId):
    print(f"{pIndex=} - {opId=}")
    if pIndex+1 == len(packetList):
        return packetList[pIndex]['value']
    elif packetList[pIndex]['id'] == 4: # if ID 4
        return applyOperation(opId, packetList[pIndex]['value'], getAnswer(pIndex+1, opId))
    elif packetList[pIndex-1]['id'] != 4: # if ID not 4 and last package not 4
        return applyOperation(opId, packetList[pIndex]['value'], getAnswer(pIndex+1, packetList[pIndex]['id']))
    elif packetList[pIndex-1]['id'] == 4: # if ID not 4 and last package 4
        # BUG doesn't work for nested packets
        # Maybe use a while loop
        # Maybe update the list
        packetList[pIndex]['value'] = applyOperation(opId, packetList[pIndex]['value'], getAnswer(pIndex+1, packetList[pIndex]['id']))
        return 1
"""
