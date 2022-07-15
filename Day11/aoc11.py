"""Advent of Code Day 11 - Dumbo Octopus"""

import argparse
import copy
import doctest

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
        for x in range(len(file_data)):
            file_array.append([])
            for y in range(len(file_data[x])):
                file_array[x].append(int(file_data[x][y]))
    return file_array

def print_array(array):
    """Pretty printing for an array"""
    TAB = '\t'
    SPACE = ' '
    for row in array:
        print(f"{SPACE.join(map(str,row))}")

def flash_count(energy_map):
    """
    Function to count the number of flashes and reset all 'X' to 0 in the octopus energy levels

    params
     energy_map is a 2D array of single digit numbers and 'X's

    For the energy_map
    3 2 4 1
    5 X 3 X
    3 6 9 X
    X X 9 4

    There would be fve flashes and the energy_map would be updated to be
    3 2 4 1
    5 0 3 0
    3 6 9 0
    0 0 9 4

    >>> energy_map = [[3,2,4,1],[5,'X',3,'X'],[3,6,9,'X'],['X','X',9,4]]
    >>> flash_count(energy_map)
    5
    >>> print(energy_map)
    [[3, 2, 4, 1], [5, 0, 3, 0], [3, 6, 9, 0], [0, 0, 9, 4]]
    """
    flash_count = 0
    for y in range(len(energy_map)):
        for x in range(len(energy_map[y])):
            if energy_map[y][x] == 'X':
                energy_map[y][x] = 0
                flash_count += 1
    return flash_count

def increment_energy(energy_map,coordinate):
    """
    Function will check whether the energy level at the suppplied coordinate can be increased
    If it can then increase it or set it to 'X' if it's reached maximum and going to flash
    Then and call adjacent points

    params:
     energy_map is a 2D array of single digit integers
     coordinate is a list containing the y and x coordinate [y,x] as an integer pair

    For the energy_map
    3 2 4 1
    5 0 3 0
    3 6 9 0
    0 0 9 4
      and coordinate [1,2]
    The energy_map would be updated to be:
    3 2 4 1
    5 0 4 0
    3 6 9 0
    0 0 9 4

    If a number has reached its maximum and is incremented,
     it is set to 'X' to indicate that it will flash

    >>> energy_map = [[3,2,4,1],[5,0,3,0],[3,6,9,0],['X',0,9,4]]
    >>> increment_energy(energy_map,[1,2])
    >>> print(energy_map)
    [[3, 2, 4, 1], [5, 0, 4, 0], [3, 6, 9, 0], ['X', 0, 9, 4]]
    >>> increment_energy(energy_map,[3,0])
    >>> print(energy_map)
    [[3, 2, 4, 1], [5, 0, 4, 0], [3, 6, 9, 0], ['X', 0, 9, 4]]
    """
    y = coordinate[0]
    x = coordinate[1]
    if energy_map[y][x] == 9:
        energy_map[y][x] = 'X'
        get_adjacent_coords(energy_map,coordinate)
    elif energy_map[y][x] == 'X':
        pass
    else:
        energy_map[y][x] += 1

def get_adjacent_coords(energy_map,coordinate):
    """
    Funciton will check adjacent coordinate points and call increment_energy for each adjacent point

    params:
     energy_map is a 2D array of single digit integers
     coordinate is a list containing the y and x coordinate [y,x] as integer
    """
    y_coord = coordinate[0]
    x_coord = coordinate[1]
    for y in range(y_coord-1,y_coord+2):
        for x in range(x_coord-1,x_coord+2):
            if y < 0 or y > len(energy_map)-1:
                pass
            elif x < 0 or x > len(energy_map[y])-1:
                pass
            else:
                increment_energy(energy_map,[y,x])

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    parser.add_argument("--steps", help="Number of steps to run the function")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day11/inputTest.txt"
    if args.steps:
        steps = int(args.steps)
    else:
        steps = 100

    octopus_energy_levels = read_file_data(filename)

    doctest.testmod()

    # Part 1
    oct_energy_level_01 = copy.deepcopy(octopus_energy_levels)
    # I have to use deepcopy for the list as the normal copy() only copies the outer list.
    total_flash_count = 0
    for step in range(steps):
        for y in range(len(oct_energy_level_01)):
            for x in range(len(oct_energy_level_01[y])):
                increment_energy(oct_energy_level_01,[y,x])
        flashes = flash_count(oct_energy_level_01)
        total_flash_count += flashes
    print(f"Part 1: Total flashes after {steps} steps is {total_flash_count}")

    # Part 2
    oct_energy_level_02 = copy.deepcopy(octopus_energy_levels)
    flashes = 0
    step_count = 0
    while flashes < 100:
        step_count += 1
        for y in range(len(oct_energy_level_02)):
            for x in range(len(oct_energy_level_02[y])):
                increment_energy(oct_energy_level_02,[y,x])
        flashes = flash_count(oct_energy_level_02)
    print(f"Part 2: Flashes were 100 when step was {step_count}")
