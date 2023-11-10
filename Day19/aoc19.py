"""
--- Advent of Code 2021 ---
--- Day 19 - Beacon Scanner ---
"""

TEST = True

DAY = "19"
ROOT = "Advent-of-Code-2021/Day"
REAL_INPUT = ROOT + DAY + "/inputDay" + DAY + ".txt"
TEST_INPUT = ROOT + DAY + "/inputTest.txt"


if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


import pprint

THRESHOLD = 12


class Scanner:
    """A scanner that detects beacons"""

    def __init__(self, name, beacon_list):
        self.name = name
        self.beacon_list = beacon_list
        self.number_of_beacons = len(self.beacon_list)
        self.relative_orientation = 0
        self.relative_position = [0, 0, 0]
        self.relative_scanner = self.name
        self.relative_beacon_positions = self.beacon_list
        self.overlapping_scanners = {}
        self.relative_beacon_list = self.create_relative_beacon_list()
        self.next_hop_to_root_scanner = None
        self.path_to_root_scanner = []

    def __repr__(self):
        return f"Scanner {self.name}"

    def create_relative_beacon_list(self):
        """Produce a list of all the beacons relative positions. Each entry is a list of beacon positions from each beacon in turn"""
        relative_beacon_list = []
        for index, beacon_source in enumerate(self.beacon_list):
            relative_beacon_list.append([])
            for beacon in self.beacon_list:
                relative_beacon_list[index].append(
                    relative_beacon_position(beacon_source, beacon)
                )
        return relative_beacon_list


def relative_beacon_position(position_1, position_2):
    """return the relative position of position_2 from the point of view of position_1"""
    new_position = []
    for coordinate in zip(position_1, position_2):
        a, b = coordinate
        new_position.append(b - a)
    return new_position


def add_coordinates(position_1, position_2):
    """add the values in position_1 to the values in position_2"""
    new_position = []
    for coordinate in zip(position_1, position_2):
        a, b = coordinate
        new_position.append(a + b)
    return new_position


def reverse_coordinate(position):
    """return the poisition with each coordinate multiplied by -1"""
    return [-x for x in position]


def transform_coordinates(coordinate, transform_key):
    """transform the input coordinates"""
    x, y, z = coordinate
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


def reverse_transform(transform):
    """supply the reverse transform from the input"""
    reverse_transform = {
        0: 0,
        1: 3,
        2: 2,
        3: 1,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 16,
        9: 15,
        10: 22,
        11: 11,
        12: 18,
        13: 13,
        14: 20,
        15: 9,
        16: 8,
        17: 17,
        18: 12,
        19: 23,
        20: 14,
        21: 21,
        22: 10,
        23: 19,
    }
    return reverse_transform[transform]


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


def process_input_data(input_data):
    """process the input data creating the scanners"""
    scanners = {}
    scanner_count = 0
    for line in input_data:
        if "scanner" in line:
            scanners[scanner_count] = []
            scanner_count += 1
        elif "," in line:
            coordinates = line.split(",")
            beacon_coordinates = [int(x) for x in coordinates]
            scanners[scanner_count - 1].append(beacon_coordinates)
    return scanners


def produce_pairings(input_items):
    """from the input produce a list of all the pair combinations"""
    list_of_pairs = []
    for index1, item1 in enumerate(input_items):
        for index2, item2 in enumerate(input_items):
            if index1 < index2:
                list_of_pairs.append([item1, item2])
    return list_of_pairs


def count_common_coordinates(coordinate_list_1, coordinate_list_2):
    """given two lists of coordinates, return the number of common coorindates"""
    common_count = 0
    for position in coordinate_list_1:
        if position in coordinate_list_2:
            common_count += 1
    return common_count


def transform_coordinate_list(coordinate_list, transform):
    transformed_coordinate_list = []
    for position in coordinate_list:
        a, b, c = transform_coordinates(position, transform)
        transformed_coordinate_list.append([a, b, c])
    return transformed_coordinate_list


def test_scanner_overlap(scanner1, scanner2):
    """given two scanners test whether they overlap and return the transformation index if they do"""
    for transform in range(24):
        for index2, beacon2 in enumerate(scanner2.relative_beacon_list):
            transformed_positions = transform_coordinate_list(beacon2, transform)
            for index1, beacon1 in enumerate(scanner1.relative_beacon_list):
                count_overlap = count_common_coordinates(transformed_positions, beacon1)
                if count_overlap >= THRESHOLD:
                    return transform, index2, index1
    return None


def main():
    """Main program"""
    input_data = get_input_data(FILENAME)
    scanners = process_input_data(input_data)
    scanner_list = []
    for scanner, beacons in scanners.items():
        scanner_list.append(Scanner(scanner, beacons))

    scanner_pairs = produce_pairings(scanner_list)

    for scanner_pair in scanner_pairs:
        scanner_1, scanner_2 = scanner_pair
        overlap_result = test_scanner_overlap(scanner_1, scanner_2)
        if overlap_result is not None:
            transform, beacon2, beacon1 = overlap_result
            beacon2_transformed_coords = transform_coordinates(
                scanner_2.beacon_list[beacon2], transform
            )
            offset = relative_beacon_position(
                beacon2_transformed_coords, scanner_1.beacon_list[beacon1]
            )
            scanner_2.overlapping_scanners[scanner_1] = {
                "transform": reverse_transform(transform),
                "offset": transform_coordinates(reverse_coordinate(offset), transform),
            }

            scanner_1.overlapping_scanners[scanner_2] = {
                "transform": transform,
                "offset": offset,
            }

    # BFS on the scanners to build the paths and transforms to get from each scanner back to scanner 0
    queue = [scanner_list[0]]
    visited = [scanner_list[0]]
    while len(queue) > 0:
        next_scanner = queue.pop(0)
        for neighbor in next_scanner.overlapping_scanners:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                neighbor.next_hop_to_root_scanner = next_scanner
                for scanner in neighbor.overlapping_scanners.values():
                    scanner["offset"] = transform_coordinates(
                        scanner["offset"],
                        next_scanner.overlapping_scanners[neighbor]["transform"],
                    )
                neighbor.relative_position = add_coordinates(
                    next_scanner.relative_position,
                    next_scanner.overlapping_scanners[neighbor]["offset"],
                )
                for scanner in scanner_list:
                    print(f"{scanner} {scanner.relative_position}")
                    print(f"{scanner.overlapping_scanners}")
                    print()

    for scanner in scanner_list:
        print(f"{scanner} {scanner.relative_position}")
        print(f"{scanner.overlapping_scanners}")
        print(f"{scanner.next_hop_to_root_scanner}")


if __name__ == "__main__":
    main()
