"""
Day 19 - Beacon Scanner

A Scanner detects all Beacons within 1000 units of itself
A Scanner can have any orientation and cannot detect other Scanners
The area a Scanner covers can overlap with other Scanners
 and so two scanners can detect the same beacons

"""


class Scanner:
    """a class to model a scanner"""

    def __init__(self, name, beacon_list) -> None:
        self.beacon_list = self.build_beacon_list(beacon_list)
        self.scanner_name = name
        self.detected_beacons = len(self.beacon_list)
        self.absolute_scanner_position = None
        self.relative_beacon_positions_list = self.relative_beacon_positions()

    def build_beacon_list(self, input_list):
        beacon_list = []
        for beacon in input_list:
            x, y, z = beacon
            beacon_position = (x, y, z)
            beacon_list.append(beacon_position)
        return beacon_list

    def display_beacon_list(self):
        print(f"Scanner - {self.scanner_name}")
        for beacon in self.beacon_list:
            print(f"{beacon}")

    def display_relative_beacon_list(self):
        TAB = "\t"
        print(f"Scanner - {self.scanner_name}")
        for index, beacon in enumerate(self.relative_beacon_positions_list):
            print(f"{TAB.join(map(str,beacon))}")

    def relative_beacon_positions(self):
        """For each beacon produce a list of relative positions to all the other beacons"""
        realtive_beacon_positions = []
        for index1, beacon_position_1 in enumerate(self.beacon_list):
            realtive_beacon_positions.append([])
            for index2, beacon_position_2 in enumerate(self.beacon_list):
                realtive_beacon_position = relative_position(
                    beacon_position_1, beacon_position_2
                )
                realtive_beacon_positions[index1].append(realtive_beacon_position)
        return realtive_beacon_positions


def extract_beacon_list(filename):
    """take the input file and return a list of scanners with their list of beacons"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    scanner_list = []
    scanner_count = 0
    for line in file_data:
        if "scanner" in line:
            scanner_list.append([])
            scanner_count += 1
        elif "," in line:
            coordinates = line.split(",")
            beacon_coordinates = [int(x) for x in coordinates]
            scanner_list[scanner_count - 1].append(beacon_coordinates)
    return scanner_list


def transform_coordinates(x, y, z, transform_key):
    """transform the input coordinates"""
    coordinate_transforms = {
        0: (x, y, z),
        1: (x, z, -y),
        2: (x, -y, -z),
        3: (x, -z, y),
        4: (-x, -y, z),
        5: (-x, -z, -y),
        6: (-x, y, -z),
        7: (-x, z, y),
        8: (z, x, y),
        9: (-y, x, z),
        10: (-z, x, -y),
        11: (y, x, -z),
        12: (z, -x, -y),
        13: (-y, -x, -z),
        14: (-z, -x, y),
        15: (y, -x, z),
        16: (y, z, x),
        17: (z, -y, x),
        18: (-y, -z, x),
        19: (-z, y, x),
        20: (-y, z, -x),
        21: (-z, -y, -x),
        22: (y, -z, -x),
        23: (z, y, -x),
    }
    return coordinate_transforms[transform_key]


def transform_list(transform_key, position_list):
    """Take list of positions and return the list once each position has been transformed"""
    return_list = []
    for position in position_list:
        x, y, z = position
        return_list.append(transform_coordinates(x, y, z, transform_key))
    return return_list


def relative_position(position_1, position_2):
    """return the position of position2 from the point of view of position1"""
    x_1, y_1, z_1 = position_1
    x_2, y_2, z_2 = position_2
    return (x_2 - x_1, y_2 - y_1, z_2 - z_1)


def compare_lists(list1, list2):
    """compare two lists and return a list of the common members"""
    return_list = []
    for member1 in list1:
        if member1 in list2:
            return_list.append(member1)
    return return_list


def produce_pairings(input_list):
    """from the input_list produce a list of all the pair combinations"""
    return_list = []
    for index1, item1 in enumerate(input_list):
        for index2, item2 in enumerate(input_list):
            if index1 < index2:
                return_list.append([item1, item2])
    return return_list


def main():
    """the main program"""
    filename = "Day19/inputTest.txt"
    scanner_data = extract_beacon_list(filename)
    scanner_list = []
    for index, beacon_list in enumerate(scanner_data):
        scanner_list.append(Scanner(index, beacon_list))

    scanner_pairs = produce_pairings(scanner_list)

    common_beacon_count = 0
    for scanners in scanner_pairs:
        scanner_1, scanner_2 = scanners
        for index1, beacon1 in enumerate(scanner_1.relative_beacon_positions_list):
            for index2, beacon2 in enumerate(scanner_2.relative_beacon_positions_list):
                for transform_key in range(24):
                    beacon_transform = transform_list(transform_key, beacon2)
                    common_positions = compare_lists(beacon1, beacon_transform)
                    if len(common_positions) > 11:
                        common_beacon_count += 1

    total_beacons_detected = 0
    for scanner in scanner_list:
        total_beacons_detected += scanner.detected_beacons

    print(
        f"Part I: Total Beacons detected {total_beacons_detected} common beacons {common_beacon_count} total unique beacons {total_beacons_detected - common_beacon_count}"
    )


if __name__ == "__main__":
    main()
