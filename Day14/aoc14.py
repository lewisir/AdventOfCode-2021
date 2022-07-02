# Advent of Code Day 14 - Extended Polymerization

import argparse
import functools

def readFileData(filename):
    """Function to read in data from an input file and return the processed file data"""
    pairInsertions = {}
    polymerTemplate = ''
    with open(filename) as file:
        for line in file:
            if line[3:5] == '->':
                pairInsertions[line[:2]] = line.rstrip('\n')[-1:]
            elif len(line) > 1 :
                polymerTemplate = [line.rstrip('\n')]
    returnData = [pairInsertions,polymerTemplate]
    return returnData

def polymerise(pairInsertions,polymerInput):
    newPolymer = ''
    for x in range(len(polymerInput)-1):
        element1 = polymerInput[x:x+1]
        element2 = polymerInput[x+1:x+2]
        key = element1 + element2
        newElement = pairInsertions[key]
        newPolymer = newPolymer + element1 + newElement
    newPolymer = newPolymer + polymerInput[-1]
    return newPolymer

def countFrequency(string):
    frequencyDict = {}
    for char in string:
        if char in frequencyDict.keys():
            pass
        else:
            frequencyDict[char] = string.count(char)
    return frequencyDict

def maxValue(inputDict):
    maxValue = 0
    for x in inputDict.values():
        if x > maxValue:
            maxValue = x
    return maxValue

def minValue(inputDict):
    minValue = float('inf')
    for x in inputDict.values():
        if x < minValue:
            minValue = x
    return minValue

# @functools.lru_cache(maxsize=None)   #### This gives an "unhashable type: 'dict'" error
def countPolymerElements(pair,pairInsertions,elementCount,step,limit):
    element1, element2, newElement = pair[:1], pair[-1], pairInsertions[pair]
    if newElement in elementCount:
        elementCount[newElement] += 1
    else:
        elementCount[newElement] = 1
    newPair1 = "".join([element1,newElement])
    newPair2 = "".join([newElement,element2])
    step += 1
    # print(f"step {step} pair {pair} newElement {newElement} newPair1 {newPair1} newPair2 {newPair2}")
    if step <= limit:
        countPolymerElements(newPair1,pairInsertions,elementCount,step,limit)
        countPolymerElements(newPair2,pairInsertions,elementCount,step,limit)

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
    pairInsertions = ouput[0]
    polymerTemplate = ouput[1]
    polymer = polymerTemplate[0]
    print(f"starting polymer {polymerTemplate}")
    """
    for _ in range(10):
        polymer=polymerise(pairInsertions,polymer)
    
    maxNum = maxValue(countFrequency(polymer))
    minNum = minValue(countFrequency(polymer))

    # print(countFrequency(polymer))

    print(f"Part I : max value is {maxNum} min value is {minNum} and difference is {maxNum - minNum}")
    """
    polymer = polymerTemplate[0]
    elementCount = countFrequency(polymer)
    limit = 9
    step = 0
    for x in range(len(polymer)-1):
        pair = polymer[x:x+2]
        countPolymerElements(pair,pairInsertions,elementCount,step,limit)
    print(elementCount)
    maxNum = maxValue(elementCount)
    minNum = minValue(elementCount)
    print(f"Part II : max value is {maxNum} min value is {minNum} and difference is {maxNum - minNum}")
