# Advent of Code Day 11

import argparse
import copy

def readFileData(filename):
    """Function to read in data from an input file and return the processed file data"""
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
    """Function to count the number of flashes and reset all 'X' to 0 in the octopus energy levels"""
    flashCount = 0
    for y in range(len(energyMap)):
        for x in range(len(energyMap[y])):
            if energyMap[y][x] == 'X':
                energyMap[y][x] = 0
                flashCount += 1
    return flashCount

def incrementEnergy(energyMap,coordinate):
    """Function will check whether the energy level at the suppplied coordinate can be increased, increase it or set it to 'X' and call adjectent points"""
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
    """will check adjacent coordinate points and call incrementEnergy"""
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

    # Part 1
    octEnergyLevePart1 = copy.deepcopy(octopusEnergyLevels)
    # I have to use deepcopy for the list as the normal copy() only copies the outer list and not the inner lists.
    # This is a shallow copy and I need  deepcopy
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