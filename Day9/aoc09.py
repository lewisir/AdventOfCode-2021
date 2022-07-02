# Advent of Code Day 9 - Smoke Basin

import argparse

def readFileData(filename):
    """Function to read in data from an input file and return the list containing the file data"""
    fileData = []
    with open(filename) as file:
        for line in file:
            fileData.append(line.rstrip('\n'))
    return fileData

def find_string_low_points(string):
    """Funciton to find the low points in a string and return their positions and values"""
    # A low point is a number in the string that is less than the values adjacent to it
    # low_points dictionary contains keys of the position of the low points and values with are the values of the low points
    low_points = {}
    for index, char in enumerate(string):
        if index == 0:                     # Case for the first number in the string (there's only one number adjacent to it)
            if char < string[index+1]:
                low_points[index] = char
        elif index == len(string)-1:       # Case for the last number in the string (there's only one number adjacent to it)
            if char < string[index-1]:
                low_points[index] = char
        else:
            if char < string[index-1] and char < string[index+1]:
                low_points[index] = char
    return low_points

def incrementListValues(inputList,increment):
    inputList = [int(x) for x in inputList]
    for x in range(len(inputList)):
        inputList[x] = inputList[x] + increment
    return inputList

def findadjactentCoords(heightMap,coordinate):
    """At the given position in the heightMap return the coordinates to the left, right, above and below"""
    newCoords = []
    if  coordinate[0] != 0:
        coord = [coordinate[0]-1,coordinate[1]]
        newCoords.append(coord)
    if coordinate[0] != len(heightMap)-1:
        coord = [coordinate[0]+1,coordinate[1]]
        newCoords.append(coord)
    if coordinate[1] != 0:
        coord = [coordinate[0],coordinate[1]-1]
        newCoords.append(coord)
    if coordinate[1] != len(heightMap[0])-1:
        coord = [coordinate[0],coordinate[1]+1]
        newCoords.append(coord)
    return newCoords

def findBasin(heightMap,height,coordinate,basinList):
    """For the coordinate in the heightMap test if it's less than height and add it to the basin list then find the adjactent points and repeat"""
    if int(heightMap[coordinate[0]][coordinate[1]]) < height:
        if coordinate not in basinList:
            basinList.append(coordinate)
            newCoords = findadjactentCoords(heightMap,coordinate)
            for coord in newCoords:
                findBasin(heightMap,height,coord,basinList)
    return basinList

def productOfList(integerList,number):
    """Given a list of integers and a number, multiply the number of largest integers together"""
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
    
    heightMap = readFileData(filename)

    allLowPointValues = []
 
    # Part 1 - find the low points in the height Map, increment each one by "1" and return the sum
    """
    for s in range(len(heightMap)):
        sLength = len(heightMap)
        stringLowPoints = find_string_low_points(heightMap[s])
        for pos in stringLowPoints:
            if s == 0:
                if stringLowPoints[pos] < heightMap[s+1][pos]:
                    allLowPointValues.append(stringLowPoints[pos])
            elif s == sLength-1:
                if stringLowPoints[pos] < heightMap[s-1][pos]:
                    allLowPointValues.append(stringLowPoints[pos])
            else:
                if stringLowPoints[pos] < heightMap[s-1][pos] and stringLowPoints[pos] < heightMap[s+1][pos]:
                    allLowPointValues.append(stringLowPoints[pos])
    """
    for i, value in enumerate(heightMap):
        sLength = len(heightMap)
        stringLowPoints = find_string_low_points(value)
        for pos in stringLowPoints:
            if i == 0:
                if stringLowPoints[pos] < heightMap[i+1][pos]:
                    allLowPointValues.append(stringLowPoints[pos])
            elif i == sLength-1:
                if stringLowPoints[pos] < heightMap[i-1][pos]:
                    allLowPointValues.append(stringLowPoints[pos])
            else:
                if stringLowPoints[pos] < heightMap[i-1][pos] and stringLowPoints[pos] < heightMap[i+1][pos]:
                    allLowPointValues.append(stringLowPoints[pos])
    print(sum(incrementListValues(allLowPointValues,1)))


    # Part 2 - Finding the three largest basins in the map and multiply them together    
    allBasinCoords = []
    basinLenghts = []
    for y in range(len(heightMap)):
        for x in range(len(heightMap[0])):
            tempBasinList = []
            coordinate = [y,x]
            if coordinate not in allBasinCoords:
                basin = findBasin(heightMap,9,coordinate,tempBasinList)
                allBasinCoords.extend(basin)
                basinSize = (len(basin))
                if basinSize > 0:
                    basinLenghts.append(basinSize)
    
    answer = productOfList(basinLenghts,3)
    print(f"Part 2 answer {answer}")
