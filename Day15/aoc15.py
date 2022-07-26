"""
Day 15 - Chiton
"""
import argparse
import doctest
from riskmap import RiskMap
from arrayExpansion import ArrayExpansion

def read_file_data(filename):
    """
    Function to read in data from an input file and return the processed file data

    The input file contains lines of numbers. For example:
    5483143
    2745854
    5264556

    This is processed to return an array of the integers. For example:
    [[5,4,8,3,1,4,3],[2,7,4,5,8,5,4],[5,2,6,4,5,5,6]]
    """
    file_data = []
    file_array = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip('\n'))
        for y in range(len(file_data)):
            file_array.append([])
            for x in range(len(file_data[y])):
                file_array[y].append(int(file_data[y][x]))
    return file_array

def print_array(array):
    """Pretty printing for an array"""
    TAB = '\t'
    SPACE = ' '
    for row in array:
        print(f"{SPACE.join(map(str,row))}")

def main():
    """The main program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day15/inputTest.txt"

    file_data = read_file_data(filename)

    my_risk_map = RiskMap(file_data)
    # print(f"Risk map is {my_risk_map.y_map_size} by {my_risk_map.x_map_size}")
    START = (0,0)
    END = (my_risk_map.y_map_size-1,my_risk_map.x_map_size-1)
    print(f"Part 1 - Lowest cost is: {my_risk_map.shortest_path(START,END)}")

    new_file_data = ArrayExpansion(file_data)
    my_new_risk_map = RiskMap(new_file_data.expand_array(5,5))
    START = (0,0)
    END = (my_new_risk_map.y_map_size-1,my_new_risk_map.x_map_size-1)
    print(f"Part 2 - Lowest cost is: {my_new_risk_map.shortest_path(START,END)}")
    # print_array(part_two_risk_map.expand_array(2,2,1))

if __name__ == "__main__":
    doctest.testmod()
    main()
