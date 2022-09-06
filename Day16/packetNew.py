class Packet():
    """A class to model packets"""

    VERSION_BITS = 3
    TYPE_BITS = 3
    LENGTH_TYPE_BITS = 1
    PACKET_COUNT_BITS = 11
    PACKET_LENGTH_BITS = 15
    LITERAL_BITS = 5
    PREFIX_BITS = 1
    MIN_PACKET_LEN = 10

    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.remaining_packet_count = 1
        self.remaining_packet_length = 0
        self.length = 0
        self.version = self.extract_value(self.VERSION_BITS)
        self.length += self.VERSION_BITS
        self.type_value = self.extract_value(self.TYPE_BITS)
        self.length += self.TYPE_BITS
        self.sub_packets = []
        self.version_sum = 0
        while self.remaining_packet_count > 0 or self.remaining_packet_length > self.MIN_PACKET_LEN:
            self.remaining_packet_count -= 1
            if self.type_value == 4:
                self.literal_value, literal_length = self.extract_literal()
                self.length += literal_length
            else:
                self.length_type = self.extract_value(self.LENGTH_TYPE_BITS)
                if self.length_type == 1:
                    self.packet_count = self.extract_value(self.PACKET_COUNT_BITS)
                    self.remaining_packet_count = self.packet_count
                    self.length += ???????????????
                else:
                    self.packet_length = self.extract_value(self.PACKET_LENGTH_BITS)
                    self.remaining_packet_length = self.packet_length
                    self.length += self.packet_length
                #self.sub_packets.append(Packet(self.binary_string))
                Packet(self.binary_string)
            print(f"--  New packet Version {self.version} Type {self.type_value}\n")

    def extract_value(self,bits):
        value = int(self.binary_string[:bits],2)
        self.binary_string = self.binary_string[bits:]
        self.remaining_packet_length -= bits
        return value

    def extract_literal(self):
        literal_binary = ''
        prefix_bit = 1
        literal_length = 0
        while prefix_bit == 1:
            prefix_bit = int(self.binary_string[:self.PREFIX_BITS],2)
            self.binary_string = self.binary_string[self.PREFIX_BITS:]
            self.remaining_packet_length -= self.PREFIX_BITS
            literal_binary += self.binary_string[:self.LITERAL_BITS-self.PREFIX_BITS]
            self.binary_string = self.binary_string[self.LITERAL_BITS-self.PREFIX_BITS:]
            literal_length += self.LITERAL_BITS
            self.remaining_packet_length -= self.LITERAL_BITS
        return int(literal_binary,2), literal_length
