
from part2.parser import PacketParser

def main():
    with open('part2/input_skido.txt', 'r') as inputFile:
        hex_packet = inputFile.readline()
        packet_parser = PacketParser(hex_packet)
        # print(f"{hex_packet=}")
        while len(hex_packet) > 6: # on s'en fout
            hex_packet = packet_parser.getNextPacket()
        packet_parser.resumePacketState()

if __name__ == '__main__':
    main()
