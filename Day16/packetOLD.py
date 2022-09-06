"""A set of classes to deal with hex streams and packets"""

class HexStream:
    """This class takes a stream of hexadecimal characters and processes it to determing the packets"""
    VERSION_BITS = 3
    TYPE_BITS = 3
    LENGTH_TYPE_BITS = 1
    PACKET_COUNT_BITS = 11
    PACKET_LENGTH_BITS = 15
    LITERAL_BITS = 5
    PREFIX_BITS = 1

    def __init__(self, hex_string):
        """Initialise the object"""
        self.packet_hex = list(hex_string)
        self.packet_list = []
        self.process_packet_string(self.packet_hex)


    def convert_hex_to_binary(self, hex_char):
        """given a hex charcter, return the four binary bits as a string"""
        if hex_char == "0":
            return "0000"
        if hex_char == "1":
            return "0001"
        if hex_char == "2":
            return "0010"
        if hex_char == "3":
            return "0011"
        if hex_char == "4":
            return "0100"
        if hex_char == "5":
            return "0101"
        if hex_char == "6":
            return "0110"
        if hex_char == "7":
            return "0111"
        if hex_char == "8":
            return "1000"
        if hex_char == "9":
            return "1001"
        if hex_char == "A":
            return "1010"
        if hex_char == "B":
            return "1011"
        if hex_char == "C":
            return "1100"
        if hex_char == "D":
            return "1101"
        if hex_char == "E":
            return "1110"
        if hex_char == "F":
            return "1111"

    def extract_value(self, binary_string, packet_hex, bit_length):
        """
        Extract the value from the packet based on the bit_length
        return the value, the updated binary string and the updated packet_hex  # though this is updated by reference
        """
        while len(binary_string) < bit_length:
            binary_string += self.convert_hex_to_binary(packet_hex.pop(0))
            binary_string += self.convert_hex_to_binary(packet_hex.pop(0))
        value = int(binary_string[:bit_length],2)
        binary_string = binary_string[bit_length:]
        return value, binary_string

    def _get_literal_value(self, binary_string, packet_hex_list):
        """Extract the literal value from the a packet"""
        literal_binary = ''
        prefix_bit = 1
        while prefix_bit == 1:
            while len(binary_string) < self.LITERAL_BITS:
                binary_string += self.convert_hex_to_binary(packet_hex_list.pop(0))
                binary_string += self.convert_hex_to_binary(packet_hex_list.pop(0))
            prefix_bit = int(binary_string[:self.PREFIX_BITS])
            binary_string = binary_string[self.PREFIX_BITS:]
            literal_binary += binary_string[:self.LITERAL_BITS-self.PREFIX_BITS]
            binary_string = binary_string[self.LITERAL_BITS-self.PREFIX_BITS:]
        return int(literal_binary,2), binary_string

    def process_packet_string(self, packet_hex_list):
        """
        Process the input hex string to delineate packets
        hex_list is a list of the hex values
        """
        binary_string = ''
        operational_pkt_depth = 0
        while len(packet_hex_list) > 0:
            # Get Version
            version, binary_string = self.extract_value(binary_string, packet_hex_list, self.VERSION_BITS)
            # Get Type ID
            packet_type_value, binary_string = self.extract_value(binary_string, packet_hex_list, self.TYPE_BITS)
            if packet_type_value == 4:
                literal, binary_string = self._get_literal_value(binary_string, packet_hex_list)
                packet_type = 'literal'
                self.packet_list.append(Literal(version,packet_type_value,literal))
            if packet_type_value != 4:
                packet_type = 'operational'
                operational_pkt_depth += 1
                # Get Length Type
                packet_length_type, binary_string = self.extract_value(binary_string, packet_hex_list, self.LENGTH_TYPE_BITS)
                if packet_length_type == 1:
                    length_type = 'PacketCount'
                    # Get Packet Count
                    sub_packet_count, binary_string = self.extract_value(binary_string, packet_hex_list, self.PACKET_COUNT_BITS)
                if packet_length_type == 0:
                    length_type = 'BitLength'
                    # Get Packet Length
                    sub_packet_length, binary_string = self.extract_value(binary_string, packet_hex_list, self.PACKET_LENGTH_BITS)
                self.packet_list.append(Operational(version,packet_type_value,length_type))


class Packet():
    """A class to store packet information"""
    def __init__(self, pkt_version, pkt_type_value):
        """Initialise the packet with a version and a type"""
        self.pkt_version = pkt_version
        self.pkt_type_value = pkt_type_value


class Literal(Packet):
    """A class of Literal Packets"""
    def __init__(self, pkt_version, pkt_type_value, literal_value):
        Packet.__init__(self, pkt_version, pkt_type_value)
        self.literal_value = literal_value


class Operational(Packet):
    """A class of Operational Packets"""
    def __init__(self, pkt_version, pkt_type_value, length_type):
        Packet.__init__(self, pkt_version, pkt_type_value)
        self.length_type = length_type
        self.sub_packets = []

    def add_sub_packet(self, packet):
        """Method to add a packet to this operational packet"""
        self.sub_packets.append(packet)

    # Can I add operator type based on the packet's type?
