#!/usr/bin/env python3

from part2.packet import Packet, OperatorPacket, LiteralPacket

import enum

class packetType(enum.Enum):
    literal             = 0
    operator            = 1
    operator_subpacket  = 2
    operator_bitLen     = 3

class PacketParser:
    def __init__(self, hex_packet, bin_packet=""):
        self.hex_packet = hex_packet
        self.current_bin_packet = ''
        self.current_packet = None
        self.packets = []
        self.parents_stack = [] # contains operators

    def checkNextBitBatch(self, nb_bits_needed): # get next packet
        nb_bits_diff = nb_bits_needed - len(self.current_bin_packet) # Check if enough bits lefts
        if  nb_bits_diff > 0: # if not enough
            nb_hex = int(nb_bits_diff / 4)
            if nb_bits_diff % 4 > 0:
                nb_hex += 1
            self.current_bin_packet += self.convertToBinary(self.hex_packet[0:nb_hex])
            self.hex_packet = self.hex_packet[nb_hex:]

    def convertToBinary(self, hex_packet):
        bin_res = bin(int(hex_packet, 16))[2:]
        len_diff = 4 * len(hex_packet) - len(bin_res)
        return '0' * len_diff + bin_res

    def convertToDec(self, binValue):
        return int(binValue, 2)

    def getHeader(self):
        self.checkNextBitBatch(6)
        header = [self.convertToDec(self.current_bin_packet[:3]), self.convertToDec(self.current_bin_packet[3:6])]
        self.current_bin_packet = self.current_bin_packet[6:] # set current bin
        return header

    def getNextPacket(self):
        packet_header = self.getHeader() # get version / ID

        if packet_header[1] == 4: # id == 4 Literal
            self.current_packet = LiteralPacket(packet_header) # init literal packet
            self.packets.append(self.current_packet) # add the packet to the list
            self.currentType = packetType.literal # set type as literal
        else: # id != 4 : operator
            self.checkNextBitBatch(1)
            self.current_packet = OperatorPacket(packet_header, self.current_bin_packet[0])
            self.packets.append(self.current_packet) # add to list of all packets
            self.parents_stack.append(self.current_packet) # append to parents (because its operator)
            self.current_bin_packet = self.current_bin_packet[1:] # update curr
            self.currentType = packetType.operator # Set type to Operator

        if self.currentType == packetType.literal: # if literal
            self.treatLiteralPacket()
        elif self.currentType == packetType.operator: # if operator
            self.treatOperatorPacket()
        else:
            # Handle possible error
            pass
        return self.hex_packet

    def setParentAndChild(self, target_packet):
        if not target_packet == self.parents_stack[-1]: # avoid avoiding itself (p1 and p1)
            target_packet.setParent(self.parents_stack[-1]) # Fucking useless
            self.parents_stack[-1].addChild(target_packet) # Same for this one
            self.parents_stack[-1].addSubpackets(target_packet) # add it subpacket
        else: # If operator
            if target_packet.isComplete():
                self.parents_stack.pop() # remove itself from the stack
                if len(self.parents_stack) > 0: # if we are in depth
                    self.setParentAndChild(target_packet) # Recurse on itself

    def treatLiteralPacket(self):
        this_local_packet = self.current_packet # copy current packet
        print(f"---Treating Literal packet[{this_local_packet.version}, {this_local_packet.id}]")
        is_packet_complete = False
        while(not is_packet_complete):
            self.checkNextBitBatch(5)
            # Add group of 5 until found group starting by 0
            is_packet_complete = this_local_packet.addGroup(self.current_bin_packet[:5])
            self.current_bin_packet = self.current_bin_packet[5:] # update bin
        this_local_packet.setValue() # concat & convert to Dec
        self.setParentAndChild(this_local_packet) # link literal to most recent operator
        print(f"\t---Finished treating Literal packet[{this_local_packet.version}, {this_local_packet.id}]: value={this_local_packet.value}")

    def treatOperatorPacket(self):
        this_local_packet = self.current_packet # Copy current packet
        print(f"+++Treating Operator packet[{this_local_packet.version}, {this_local_packet.id}]")
        # Make sure you have enough bits in the current bit batch
        self.checkNextBitBatch(this_local_packet.subpacket_info) # Get nb of bit to read for rest of the packer
        # Set the expected number of bits or subpackets in the current operator packet
        self.current_packet.setSubpacketsInfo(self.convertToDec(self.current_bin_packet[:this_local_packet.subpacket_info])) # should be local_packet instead of self.current..
        self.current_bin_packet = self.current_bin_packet[this_local_packet.subpacket_info:] # update current bin

        while not this_local_packet.isComplete(): # While all bit not read or nb of packet not read
            self.getNextPacket() # parse (recursion)
        this_local_packet.solveOperation() # Apply operation to childs
        self.setParentAndChild(this_local_packet)
        print(f"\t+++Finished treating Operator packet[{this_local_packet.version}, {this_local_packet.id}]: value={this_local_packet.value}")

    def resumePacketState(self):
        # print(f"Packets list: {[str(packet) for packet in self.packets]}")
        print(f"Final result = {str(self.packets[0])}") # give result
