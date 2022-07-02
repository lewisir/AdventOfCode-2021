# Advent of Code Day 2 - Dive!

# Take a list of instructions (forward, up, down) and total the horizonal position and depth

def position_simple(instructionList):
    depth = 0
    hzntl_position = 0
    for instruction in instructionList:
        if instruction.split()[0] == "forward":
            hzntl_position += int(instruction.split()[1])
        elif instruction.split()[0] == "down":
            depth += int(instruction.split()[1])
        elif instruction.split()[0] == "up":
            depth -= int(instruction.split()[1])
        else:
            print("Unrecognised instruction")
    product = hzntl_position * depth
    return product


def position_complex(instructionList):
    depth = 0
    hzntl_position = 0
    aim = 0
    for instruction in instructionList:
        if instruction.split()[0] == "forward":
            hzntl_position += int(instruction.split()[1])
            depth += aim * int(instruction.split()[1])
        elif instruction.split()[0] == "down":
            aim += int(instruction.split()[1])
        elif instruction.split()[0] == "up":
            aim -= int(instruction.split()[1])
        else:
            print("Unrecognised instruction")
    product = hzntl_position * depth
    return product

# Read in the file to instricutionList
filename = input("Enter the file containing the list of numbers. ")
with open(filename) as file_object:
    instructionList = file_object.readlines()

# For each line in the file check whether forward, up or down is used and increment the position
# Initiate the depth and horizontal positions

print("Simple position product " + str(position_simple(instructionList)))

print("Complex position product " + str(position_complex(instructionList)))