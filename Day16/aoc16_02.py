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

Differnet type codes determine how the packets gets its value
TYPE_CODES = {
    0: 'sum of the values of the sub-packets',
    1: 'product of the values of the sub-packets',
    2: 'minimum of the values of the sub-packets',
    3: 'maximum of the values of the sub-packets',
    4: 'Literal value',
    5: 'greater than - value is 1 if first sub-packet is greater than the second sub-packet',
    6: 'less than - value is 1 if first sub-packet is less than the second sub-packet',
    7: 'equal to - value is 1 if first sub-packet is euqal to the second sub packet'
}
"""

import doctest
from cmath import inf

HEX2BIN = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

class Packet():

    VERSION_BITS = 3
    TYPE_BITS = 3
    TYPE_LENGTH_BITS = 1
    PACKET_COUNT_BITS = 11
    PACKET_LENGTH_BITS = 15
    LITERAL_BITS = 4
    PREFIX_BITS = 1
    MIN_PACKET_LEN = 11

    def __init__(self, packet_binary, position_pointer=0, depth=0):
        self.packet_binary = packet_binary
        self.position_pointer = position_pointer
        self.packet_depth = depth + 1
        self.remaining_sub_packet_count = 0
        self.remaining_sub_packet_length = 0
        self.length = 0
        self.sub_packets = []
        self.set_version()
        self.set_type()
        if self.type != 4:
            self.set_type_length()
            if self.type_length == 0:
                self.set_sub_packet_length()
                self.remaining_sub_packet_length = self.sub_packet_length
            else:
                self.set_sub_packet_count()
                self.remaining_sub_packet_count = self.sub_packet_count
            while self.remaining_sub_packet_count > 0 or self.remaining_sub_packet_length > 0:
                self.sub_packets.append(Packet(self.packet_binary, self.position_pointer, self.packet_depth))
                if self.remaining_sub_packet_count > 0:
                    self.remaining_sub_packet_count -= 1
                elif self.remaining_sub_packet_length > 0:
                    self.remaining_sub_packet_length -= self.sub_packets[-1].length
                self.length += self.sub_packets[-1].length
                self.position_pointer += self.sub_packets[-1].length
        self.set_packet_value()
        self.evaluate_version_total()
        # self.display_packet()

    def get_value(self, start_position, bit_length):
        # self.display_binary()
        return int(self.packet_binary[start_position:start_position + bit_length] ,2)

    def set_version(self):
        self.version = self.get_value(self.position_pointer, self.VERSION_BITS)
        self.position_pointer += self.VERSION_BITS
        self.length += self.VERSION_BITS

    def set_type(self):
        self.type = self.get_value(self.position_pointer, self.TYPE_BITS)
        self.position_pointer += self.TYPE_BITS
        self.length += self.TYPE_BITS

    def set_literal_value(self):
        literal_value_list = []
        prefix_bit_value = 1
        while prefix_bit_value == 1:
            prefix_bit_value = self.get_value(self.position_pointer, self.PREFIX_BITS)
            self.position_pointer += self.PREFIX_BITS
            self.length += self.PREFIX_BITS
            literal_value_list.append(self.get_value(self.position_pointer, self.LITERAL_BITS))
            self.position_pointer += self.LITERAL_BITS
            self.length += self.LITERAL_BITS
        literal_value_list.reverse()
        literal_value = 0
        for index, value in enumerate(literal_value_list):
            literal_value += (value * (2 ** (index * 4)))
        self.value = literal_value

    def set_type_length(self):
        self.type_length = self.get_value(self.position_pointer, self.TYPE_LENGTH_BITS)
        self.position_pointer += self.TYPE_LENGTH_BITS
        self.length += self.TYPE_LENGTH_BITS

    def set_sub_packet_length(self):
        self.sub_packet_length = self.get_value(self.position_pointer, self.PACKET_LENGTH_BITS)
        self.position_pointer += self.PACKET_LENGTH_BITS
        self.length += self.PACKET_LENGTH_BITS

    def set_sub_packet_count(self):
        self.sub_packet_count = self.get_value(self.position_pointer, self.PACKET_COUNT_BITS)
        self.position_pointer += self.PACKET_COUNT_BITS
        self.length += self.PACKET_COUNT_BITS

    def set_packet_value(self):
        if self.type == 0:
            self.value = 0
            for packet in self.sub_packets:
                self.value += packet.value
        elif self.type == 1:
            self.value = 1
            for packet in self.sub_packets:
                self.value *= packet.value
        elif self.type == 2:
            self.value = float(inf)
            for packet in self.sub_packets:
                if self.value > packet.value:
                    self.value = packet.value
        elif self.type == 3:
            self.value = 0
            for packet in self.sub_packets:
                if self.value < packet.value:
                    self.value = packet.value
        elif self.type == 4:
            self.set_literal_value()
        elif self.type == 5:
            if self.sub_packets[0].value > self.sub_packets[1].value:
                self.value = 1
            else:
                self.value = 0
        elif self.type == 6:
            if self.sub_packets[0].value < self.sub_packets[1].value:
                self.value = 1
            else:
                self.value = 0
        elif self.type == 7:
            if self.sub_packets[0].value == self.sub_packets[1].value:
                self.value = 1
            else:
                self.value = 0

    def evaluate_version_total(self):
        self.version_total = self.version
        for packet in self.sub_packets:
            self.version_total += packet.version_total

    def display_packet(self):
        print("-"*self.packet_depth + f"Packet version {self.version} and type {self.type} with value {self.value} and length {self.length} and sub-packets {len(self.sub_packets)}")

    def display_binary(self):
        print(f"{self.packet_binary}\n"+" "*self.position_pointer+"^")

    def display_version_total(self):
        print(f"Part I - Packet Version total is {self.version_total}")

    def display_value(self):
        print(f"Part II - Packet Value is {self.value}")

def read_file_data(filename):
    """Read in the file input"""
    file_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            file_data.append(line.rstrip('\n'))
    return file_data

def main():
    """The main program"""
    FILENAME = "Day16/inputDay16.txt"
    STRING1 = "8A004A801A8002F478"             # Packet value is 
    STRING2 = "620080001611562C8802118E34"     # Packet value is 
    STRING3 = "C0015000016115A2E0802F182340"   # Packet value is 
    STRING4 = "A0016C880162017C3686B18A3D4780" # Packet value is 
    STRING5 = "C200B40A82"                     # Packet value is  3
    STRING6 = "04005AC33890"                   # Packet value is 54
    STRING7 = "880086C3E88112"                 # Packet value is  7
    STRING8 = "CE00C43D881120"                 # Packet value is  9
    STRING9 = "D8005AC2A8F0"                   # Packet value is  1
    STRINGA = "F600BC2D8F"                     # Packet value is  0
    STRINGB = "9C005AC2F8F0"                   # Packet value is  0
    STRINGC = "9C0141080250320F1802104A08"     # Packet value is  1
    STRINGD = "D25548"                         # Packet value is 601

    packet_hex = read_file_data(FILENAME)[0]
    # packet_hex = STRING6

    packet_binary = ''
    for char in packet_hex:
        packet_binary += HEX2BIN[char]
    
    my_packet = Packet(packet_binary)
    my_packet.display_version_total()
    my_packet.display_value()

if __name__ == "__main__":
    doctest.testmod()
    main()
