"""
Day 16 - Packet Decoder

Every packet begins with a standard header; three bits for Version and three for Type ID

Type ID 4 represent a literal value in binary
The binary number is padded with leading zeros until its length is a multiple of 4 bits
Each group of 4 bits is prefixed with a single bit of value
'1' bit except the last group which is prefixed with '0'
For example 0xD2FE28
110100101111111000101000
VVVTTTAAAAABBBBBCCCCC
The final "000" are due to the hex coding and are ignored

Any other Type IDs are operator packets that contain sub-packets
The bit following the Type ID is the Length Type ID
A value of 0 means the next 15 bits represent the length in bits of the sub-packets in this packet
A value of 1 means the next 11 bits represent the number of sub-packets contained in this packet
"""
import argparse
import doctest
import packets

def read_file_data(filename):
    """Read in the file input"""
    file_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            file_data.append(line.rstrip('\n'))
    return file_data

def main():
    """The main program"""
    STRING1 = "8A004A801A8002F478"
    STRING2 = "620080001611562C8802118E34"
    STRING3 = "C0015000016115A2E0802F182340"
    STRING4 = "A0016C880162017C3686B18A3D4780"

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day16/inputDay16.txt"

    test_string = read_file_data(filename)[0]

    my_packets = packets.HexStream(test_string)
    version_sum = 0
    for packet in my_packets.packet_list:
        version_sum += packet.pkt_version
    print(f"Part 1. Packet version Sum is: {version_sum}")

if __name__ == "__main__":
    doctest.testmod()
    main()
