# Advent of Code Day 11 - Dumbo Octopus

import argparse
import copy
import doctest

def readFileData(filename):
    """
    Function to read in data from an input file and return the processed file data

    The input file contains lines of numbers. For example:
    5483143
    2745854
    5264556

    This is processed to return n array of the integers. For example:
    [[5,4,8,3,1,4,3],[2,7,4,5,8,5,4],[5,2,6,4,5,5,6]]
    """
    fileData = []
    fileArray = []
    with open(filename) as file:
        for line in file:
            fileData.append(line.rstrip('\n'))
        for x in range(len(fileData)):
            fileArray.append([])
            for y in range(len(fileData[x])):
                fileArray[x].append(int(fileData[x][y]))
    return fileArray

def printArray(array):
    """Pretty printing for an array"""
    TAB = '\t'
    SPACE = ' '
    for row in array:
        print(f"{SPACE.join(map(str,row))}")

def flashCount(energyMap):
    """
    Function to count the number of flashes and reset all 'X' to 0 in the octopus energy levels

    params
     energyMap is a 2D array of single digit numbers and 'X's
    
    For the energyMap
    3 2 4 1
    5 X 3 X
    3 6 9 X
    X X 9 4

    There would be fve flashes and the energyMap would be updated to be
    3 2 4 1
    5 0 3 0
    3 6 9 0
    0 0 9 4

    >>> energyMap = [[3,2,4,1],[5,'X',3,'X'],[3,6,9,'X'],['X','X',9,4]]
    >>> flashCount(energyMap)
    5
    >>> print(energyMap)
    [[3, 2, 4, 1], [5, 0, 3, 0], [3, 6, 9, 0], [0, 0, 9, 4]]
    """
    flashCount = 0
    for y in range(len(energyMap)):
        for x in range(len(energyMap[y])):
            if energyMap[y][x] == 'X':
                energyMap[y][x] = 0
                flashCount += 1
    return flashCount

def incrementEnergy(energyMap,coordinate):
    """
    Function will check whether the energy level at the suppplied coordinate can be increased
    If it can then increase it or set it to 'X' if it's reached maximum and going to flash
    Then and call adjacent points

    params:
     energyMap is a 2D array of single digit integers
     coordinate is a list containing the y and x coordinate [y,x] as an integer pair
    
    For the energyMap
    3 2 4 1
    5 0 3 0
    3 6 9 0
    0 0 9 4
      and coordinate [1,2]
    The energyMap would be updated to be:
    3 2 4 1
    5 0 4 0
    3 6 9 0
    0 0 9 4

    If a number has reached its maximum and is incremented, it is set to 'X' to indicate that it will flash
    
    >>> energyMap = [[3,2,4,1],[5,0,3,0],[3,6,9,0],['X',0,9,4]]
    >>> incrementEnergy(energyMap,[1,2])
    >>> print(energyMap)
    [[3, 2, 4, 1], [5, 0, 4, 0], [3, 6, 9, 0], ['X', 0, 9, 4]]
    >>> incrementEnergy(energyMap,[3,0])
    >>> print(energyMap)
    [[3, 2, 4, 1], [5, 0, 4, 0], [3, 6, 9, 0], ['X', 0, 9, 4]]
    """
    y = coordinate[0]
    x = coordinate[1]
    if energyMap[y][x] == 9:
        energyMap[y][x] = 'X'
        getAdjacentCoords(energyMap,coordinate)
    elif energyMap[y][x] == 'X':
        pass
    else:
        energyMap[y][x] += 1

def getAdjacentCoords(energyMap,coordinate):
    """
    Funciton will check adjacent coordinate points and call incrementEnergy for each adjacent point

    params:
     energyMap is a 2D array of single digit integers
     coordinate is a list containing the y and x coordinate [y,x] as integer
    """
    y_coord = coordinate[0]
    x_coord = coordinate[1]
    for y in range(y_coord-1,y_coord+2):
        for x in range(x_coord-1,x_coord+2):
            if y < 0 or y > len(energyMap)-1:
                pass
            elif x < 0 or x > len(energyMap[y])-1:
                pass
            else:
                incrementEnergy(energyMap,[y,x])

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    parser.add_argument("--steps", help="Number of steps to run the function")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "inputTest.txt"
    if args.steps:
        steps = int(args.steps)
    else:
        steps = 100
    
    octopusEnergyLevels = readFileData(filename)

    doctest.testmod()

    # Part 1
    octEnergyLevePart1 = copy.deepcopy(octopusEnergyLevels)
    # I have to use deepcopy for the list as the normal copy() only copies the outer list and not the inner lists.
    totalFlashCount = 0
    for step in range(steps):
        for y in range(len(octEnergyLevePart1)):
            for x in range(len(octEnergyLevePart1[y])):
                incrementEnergy(octEnergyLevePart1,[y,x])
        flashes = flashCount(octEnergyLevePart1)
        totalFlashCount += flashes
    print(f"Part 1: Total flashes after {steps} steps is {totalFlashCount}")
    
    # Part 2
    octEnergyLevePart2 = copy.deepcopy(octopusEnergyLevels)
    flashes = 0
    stepCount = 0
    while flashes < 100:
        stepCount += 1
        for y in range(len(octEnergyLevePart2)):
            for x in range(len(octEnergyLevePart2[y])):
                incrementEnergy(octEnergyLevePart2,[y,x])
        flashes = flashCount(octEnergyLevePart2)
    print(f"Part 2: Flashes were 100 when step was {stepCount}")