# Advent of Code Day 7 - The Treachery of Whales

import statistics

def triangularCalc (x):
    return (x+1)*x/2

if __name__ == "__main__":
    
    filename = input("Enter the file containing the horizontl positions: ")
    with open(filename) as file_object:
        numberList = file_object.readlines()

    numbers = numberList[0]
    hrzntlPositions = numbers.split(',')
    hrzntlPositions = [int(x) for x in hrzntlPositions]
    # I'm sure there's a neater way to get the data in from the file !!!

    #hrzntlPositions = [16,1,2,0,4,2,7,1,2,14]  # This is the test data that can be substituted in

    # To find the optimum position X that minimises the differnece between each element and X
    # find the median in the range of numbers

    # Calcuate the sum of differences between each element and the median (Part 1)
    positionSum = 0
    optimumPosition = statistics.median(hrzntlPositions)
    for position in hrzntlPositions:
        positionSum += abs(position - optimumPosition)
    print(f"Median is {int(optimumPosition)} and sum is {int(positionSum)}")


    # Find the optimum value by minimising the sum of the triangular numbers
    # for each value in the range of numbers calculate the sum of triangular numbers and store this
    # find the minimum sum
    hrzntlPositions.sort()
    minH = hrzntlPositions[0]
    maxH = hrzntlPositions[-1]
    sumList = []
    for x in range(minH,maxH+1):
        sumX = 0
        for position in hrzntlPositions:
            sumX += triangularCalc(abs(position-x))
        sumList.append(sumX)
    
    sumList.sort()
    print(f"Weighted fule cost is {sumList[0]}")