# Advent of Code Day 9 - Smoke Basin

import argparse

def readFileData(filename):
    """
    Function to read in data from an input file and return the list containing the file data
    
    If the file contains the following:
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678

    The then returned fileDate is:
    ["2199943210","3987894921","9856789892","8767896789","9899965678"]
    """
    fileData = []
    with open(filename) as file:
        for line in file:
            fileData.append(line.rstrip('\n'))
    return fileData

def find_string_low_points(string):
    """
    Funciton to find the low points in a string and return a disctionary with their positions and values
    
    A low point is a number in the string that is less than the values adjacent to it

    For example, in the string '8767896789', the returned dictionary is
    {
        2: '6',
        6: '6'
    }
    """
    low_points = {}
    for index, char in enumerate(string):
        if index == 0:                     # Case for the first number in the string
            if char < string[index+1]:
                low_points[index] = char
        elif index == len(string)-1:       # Case for the last number in the string
            if char < string[index-1]:
                low_points[index] = char
        else:
            if char < string[index-1] and char < string[index+1]:
                low_points[index] = char
    return low_points

def increment_list_values(input_list,increment):
    """Function increments each value in the list by the 'increment' parameter"""
    input_list = [int(x) for x in input_list]
    for x in range(len(input_list)):
        input_list[x] = input_list[x] + increment
    return input_list

def get_adjacent_coordinates(height_map,coordinate):
    """
    At the given coordinate in the height_map return the adjacent coordinates
    Adjacent coorcindates are to the left, right, above and below in the height_map
    For example, coordinate [4,2] has adajcent coordinates [4,1], [4,3], [5,2] and [6,2]
    At the limits of the height_map then the coordinate may only have 2 or 3 adjacent coorindates
    """
    new_coordinates = []
    if  coordinate[0] != 0:
        coord = [coordinate[0]-1,coordinate[1]]
        new_coordinates.append(coord)
    if coordinate[0] != len(height_map)-1:
        coord = [coordinate[0]+1,coordinate[1]]
        new_coordinates.append(coord)
    if coordinate[1] != 0:
        coord = [coordinate[0],coordinate[1]-1]
        new_coordinates.append(coord)
    if coordinate[1] != len(height_map[0])-1:
        coord = [coordinate[0],coordinate[1]+1]
        new_coordinates.append(coord)
    return new_coordinates

def find_basin_coords(height_map,height,coordinate,basin_list):
    """
    Function is given a height_map, a height, a coordinate and a basin_list
    It returns a list containing all the coordinates of the basin
    The basin_list reocrds all the coordinates of the current basin
    For the coordinate supplied, check the height_map to see if it's less than the height
    If it is, add it to the basin list then find the adjactent points
    The function is recusive, finding all coordinates that make up the basin
    """
    if int(height_map[coordinate[0]][coordinate[1]]) < height:
        if coordinate not in basin_list:
            basin_list.append(coordinate)
            new_coordinates = get_adjacent_coordinates(height_map,coordinate)
            for coord in new_coordinates:
                find_basin_coords(height_map,height,coord,basin_list)
    return basin_list

def list_product(integerList,number):
    """
    Given a list of integers and a number, multiply the number of largest integers together
    For exampls, if the function is supplied this list:
    [2,5,3,1,7,4,9]
    And the number 3, it will return the product of 9 x 7 x 5 (the three largest integers in the list)
    """
    integerList.sort(reverse = True)
    product = 1
    for x in range(0,number):
        product *= integerList[x]
    return product

if __name__ == "__main__":

    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day9/inputTest.txt"
    
    height_map = readFileData(filename)

    # List allLowPoints will store values of each low point found in the height_map
    all_low_points = []
 
    # Part 1 - find the low points in the height Map, increment each one by "1" and return the sum
    # Work through each line in the height_map, i is the index of the row in the height_map
    for i, value in enumerate(height_map):
        height_map_depth = len(height_map)
        row_low_points = find_string_low_points(value)
        # Work through each low point found in the row and find the adjacent values in adjacent rows in the height_map
        # pos is the position of the low point found in the row
        for pos in row_low_points:
            if i == 0:                         # Case for the first row in the height_map
                if row_low_points[pos] < height_map[i+1][pos]:
                    all_low_points.append(row_low_points[pos])
            elif i == height_map_depth-1:      # Case for the last row in the height_map
                if row_low_points[pos] < height_map[i-1][pos]:
                    all_low_points.append(row_low_points[pos])
            else:
                if row_low_points[pos] < height_map[i-1][pos] and row_low_points[pos] < height_map[i+1][pos]:
                    all_low_points.append(row_low_points[pos])
    print(f"Part 1 answer {sum(increment_list_values(all_low_points,1))}")


    # Part 2 - Finding the three largest basins in the map and multiply them together
    """
    Keep track of all the coordinates that form basins in all_basin_coordinates
    This is done to prevent us from re-discovering the same basins as we work through the height_map
    We find a basin by calling find_basin_coords and record the size of each basin in basin_sizes
    """
    all_basin_coordinates = []
    basin_sizes = []
    for y, row in enumerate(height_map):
        for x, value in enumerate(row):
            coordinate = [y,x]
            if coordinate not in all_basin_coordinates:
                basin = find_basin_coords(height_map,9,coordinate,[])
                all_basin_coordinates.extend(basin)
                basin_size = (len(basin))
                if basin_size > 0:
                    basin_sizes.append(basin_size)
    
    answer = list_product(basin_sizes,3)
    print(f"Part 2 answer {answer}")
