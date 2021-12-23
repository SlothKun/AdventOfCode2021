import uuid

class Packet:
    def __init__(self, packetHeader):
        self._uuid = uuid.uuid4()
        self.version = packetHeader[0]
        self.id = int(packetHeader[1])
        self.parent = None# Non useful
        self.children = []# Non useful
        self.value = None
        self.nb_packet_bits = 0

    def setParent(self, parent): # Non useful
        self.parent = parent
    
    def addChild(self, child):# Non useful
        self.children.append(child)
    
    def addPacketBits(self, nb_bits):
        self.nb_packet_bits += nb_bits

    def __eq__(self, other):
        return self._uuid == other._uuid

import enum

class OpPacketType(enum.Enum):
    _sum    = 0
    _prod   = 1
    _min    = 2
    _max    = 3
    _gt     = 5
    _lt     = 6
    _eq     = 7

class LiteralPacket(Packet): # herite de packet
    def __init__(self, packetHeader):
        super().__init__(packetHeader)
        self.groups = []
        self.children = None# Non useful
        self.addPacketBits(6) # length of packet May not be of use

    def __str__(self):
        return f"Packet [{self.version}, {self.id}] of type Literal with value of {self.value}"

    def addGroup(self, group):
        self.groups.append(group[1:]) # add group of 4 to groups
        self.addPacketBits(5)
        return group[0] == '0' # return true if starting with 0

    def setValue(self):
        self.value = int(''.join(self.groups), 2)


class OperatorPacket(Packet):
    SUBPACKET_INFO = [15, 11] # THERE

    def __init__(self, packetHeader, length_type_ID):
        super().__init__(packetHeader)
        self.length_type_ID = int(length_type_ID)
        self.subpacket_info = OperatorPacket.SUBPACKET_INFO[self.length_type_ID] # Next x bit to read
        self.addPacketBits(7)

        self.nb_subpackets_bits = None
        self.nb_following_subpackets = None
        self.subpackets = []
        self.nb_treated_bits = 0

    def __str__(self):
        return f"Packet [{self.id}] of type Operator with {len(self.subpackets)} packets and value of {self.value}"

    def setSubpacketsInfo(self, subpacket_data):
        # set packet Limit
        if self.length_type_ID == 0:
            self.nb_subpackets_bits = subpacket_data # nb of packet
        elif self.length_type_ID == 1:
            self.nb_following_subpackets = subpacket_data # len of packet
        else:
            # Handle possible value error
            pass
        self.addPacketBits(self.subpacket_info)

    def addSubpackets(self, subpacket):
        self.subpackets.append(subpacket)
        self.nb_treated_bits += subpacket.nb_packet_bits # nb of bit of all subpackets
        self.addPacketBits(subpacket.nb_packet_bits) # nb of bit of itself + subpacket

    def isComplete(self):
        return self.length_type_ID == 0 and self.nb_treated_bits == self.nb_subpackets_bits or\
               self.length_type_ID == 1 and len(self.subpackets) == self.nb_following_subpackets

    def solveOperation(self):
        if self.id == OpPacketType._sum.value:
            res = 0
            for sp in self.subpackets:
                if sp.value is None:
                    sp.solveOperation()
                res += sp.value
            self.value = res
        elif self.id == OpPacketType._prod.value:
            res = 1
            for sp in self.subpackets:
                if sp.value is None: # in case of not complete (should not append) | When subpacket is operator not treated
                    sp.solveOperation()
                res *= sp.value
            self.value = res
        elif self.id == OpPacketType._min.value:
            res = None
            for sp in self.subpackets:
                if sp.value is None:
                    sp.solveOperation()
                if res is None:
                    res = sp.value
                elif res > sp.value:
                    res = sp.value
            self.value = res
        elif self.id == OpPacketType._max.value:
            res = None
            for sp in self.subpackets:
                if sp.value is None:
                    sp.solveOperation()
                if res is None:
                    res = sp.value
                elif res < sp.value:
                    res = sp.value
            self.value = res
        elif self.id == OpPacketType._gt.value:
            if len(self.subpackets) == 2:
                for sp in self.subpackets:
                    if sp.value is None:
                        sp.solveOperation()
                if self.subpackets[0].value > self.subpackets[1].value:
                    self.value = 1
                else:
                    self.value = 0
            else:
                # Handle possible error
                pass
        elif self.id == OpPacketType._lt.value:
            if len(self.subpackets) == 2:
                for sp in self.subpackets:
                    if sp.value is None:
                        sp.solveOperation()
                if self.subpackets[0].value < self.subpackets[1].value:
                    self.value = 1
                else:
                    self.value = 0
            else:
                # Handle possible error
                pass
        elif self.id == OpPacketType._eq.value:
            if len(self.subpackets) == 2:
                for sp in self.subpackets:
                    if sp.value is None:
                        sp.solveOperation()
                if self.subpackets[0].value == self.subpackets[1].value:
                    self.value = 1
                else:
                    self.value = 0
            else:
                # Handle possible error
                pass
        else:
            # Handle possible error
            pass
