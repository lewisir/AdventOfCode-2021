"""Advent of Code Day 13 - Transparent Origami"""

import argparse
import doctest

def read_file_data(filename):
    """
    Function to read in data from an input file and return the processed file data

    The return_data is a list
    The first entry is a dictionary containing each of the points
    The second entry is a list of the fold instructions

    For input file containing:
     1,10
     2,14
     8,10
     9,0

     fold along y=7
     fold along x=5

    The return_data is:
     [{'1,10': 1, '2,14': 1, '8,10': 1, '9,0': 1}, ['fold along y=7', 'fold along x=5']]
    """
    paper = {}
    instructions = []
    with open(filename) as file:
        for line in file:
            if line[:4] == 'fold':
                instructions.append(line.rstrip('\n'))
            elif len(line) > 1 :
                paper[line.rstrip('\n')] = 1
    return_data = [paper,instructions]
    return return_data

def print_array(array):
    """Pretty printing for an array"""
    TAB = '\t'
    SPACE = ' '
    for row in array:
        print(f"{SPACE.join(map(str,row))}")

def create_array(height,width,value='.'):
    """
    Create a 2D array

    Parameters:
     height - int
     width - int
     value (default '.')

    Return
     list

    Calling create_array(4,2) will create:
    [['.', '.'], ['.', '.'], ['.', '.'], ['.', '.']]

    >>> print(create_array(3,2))
    [['.', '.'], ['.', '.'], ['.', '.']]
    """
    new_array = []
    row = value*(width)
    for _ in range(height):
        new_array.append(row)
    new_array = [list(x) for x in new_array]
    return new_array

def print_paper(paper):
    """
    Take a Dictionary that has 2 dimensional coordinates as its keys and create and print an Array to represent the map/graph
    """
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
    printable_paper = create_array(max_y+1,max_x+1)        # Why did I need to make this +1 ???
    for dot in paper:
        x_value = int(dot.split(',')[0])
        y_value = int(dot.split(',')[1])
        # print(f"dot is {dot}")
        printable_paper[y_value][x_value] = '#'
    print_array(printable_paper)

def fold(paper,direction,line):
    """Given the paper, a direction (x=left and y=up) and a line, produce a new paper with the mapping of the dots"""
    new_paper = {}
    for dot in paper:
        x_value = int(dot.split(',')[0])
        y_value = int(dot.split(',')[1])
        if direction == 'y' and y_value > line:
            new_paper[str(x_value)+','+str(y_value - 2 * (y_value - line))] = 1
        elif direction == 'x' and x_value > line:
            new_paper[str(x_value - 2 * (x_value - line))+','+str(y_value)] = 1
        else:
            new_paper[str(x_value)+','+str(y_value)] = 1
    return new_paper

def process_instructions(instruction_string):
    position = instruction_string.find('=')
    instruction_list = [instruction_string[position-1:position],int(instruction_string[position+1:])]
    return instruction_list

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day13/inputTest.txt"

    doctest.testmod()

    output = read_file_data(filename)
    transparent_paper = output[0]
    fold_instructions = output[1]
    first_instruction = process_instructions(fold_instructions[0])
    firstFold = fold(transparent_paper,first_instruction[0],first_instruction[1])
    print(f"Part I - number of dots {len(firstFold)}")

    for instruction in fold_instructions:
        foldDirection = process_instructions(instruction)[0]
        foldLine = process_instructions(instruction)[1]
        transparent_paper = fold(transparent_paper,foldDirection,foldLine)
    print(f"Part II - ")
    print_paper(transparent_paper)
