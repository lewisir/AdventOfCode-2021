# Advent of Code Day 13 - Transparent Origami

import argparse

def readFileData(filename):
    """Function to read in data from an input file and return the processed file data"""
    paper = {}
    instructions = []
    with open(filename) as file:
        for line in file:
            if line[:4] == 'fold':
                instructions.append(line.rstrip('\n'))
            elif len(line) > 1 :
                paper[line.rstrip('\n')] = 1
    returnData = [paper,instructions]
    return returnData

def printArray(array):
    """Pretty printing for an array"""
    TAB = '\t'
    SPACE = ' '
    for row in array:
        print(f"{SPACE.join(map(str,row))}")

def createArray(height,width,value='.'):
    newArray = []
    row = value*(width+1)
    for _ in range(height+1):
        newArray.append(row)
    newArray = [list(x) for x in newArray]
    return newArray

def printPaper(paper):
    """Take a Disctionary that has 2 dimensional coordinates as its keys and create and print an Array to represent the map/graph"""
    max_x, max_y = 0, 0
    # print(f"Paper is {paper}")
    for dot in paper:
        # print(f" evaluating the x_value returns {dot.split(',')[0]} where dot is {dot}")
        x_value = int(dot.split(',')[0])
        y_value = int(dot.split(',')[1])
        if x_value > max_x:
            max_x = x_value
        if y_value > max_y:
            max_y = y_value
    # print(f"max x and y is {max_x} and {max_y}")
    printablePaper = createArray(max_y,max_x)
    for dot in paper:
        x_value = int(dot.split(',')[0])
        y_value = int(dot.split(',')[1])
        # print(f"dot is {dot}")
        printablePaper[y_value][x_value] = '#'
    printArray(printablePaper)

def fold(paper,direction,line):
    """Given the paper, a direction (x=left and y=up) and a line, produce a new paper with the mapping of the dots"""
    newPaper = {}
    for dot in paper:
        x_value = int(dot.split(',')[0])
        y_value = int(dot.split(',')[1])
        if direction == 'y' and y_value > line:
            newPaper[str(x_value)+','+str(y_value - 2 * (y_value - line))] = 1
        elif direction == 'x' and x_value > line:
            newPaper[str(x_value - 2 * (x_value - line))+','+str(y_value)] = 1
        else:
            newPaper[str(x_value)+','+str(y_value)] = 1
    return newPaper

def processInstructions(instructionString):
    position = instructionString.find('=')
    instructList = [instructionString[position-1:position],int(instructionString[position+1:])]
    return instructList

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "inputTest.txt"
    
    ouput = readFileData(filename)
    transparentPaper = ouput[0]
    foldInstructions = ouput[1]
    firstInstruct = processInstructions(foldInstructions[0])
    firstFold = fold(transparentPaper,firstInstruct[0],firstInstruct[1])
    print(f"Part I - number of dots {len(firstFold)}")

    for instruction in foldInstructions:
        foldDirection = processInstructions(instruction)[0]
        foldLine = processInstructions(instruction)[1]
        transparentPaper = fold(transparentPaper,foldDirection,foldLine)
    print(f"Part II - ")
    printPaper(transparentPaper)