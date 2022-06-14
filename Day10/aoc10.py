# Advent of Code Day 10

import argparse
import statistics

def readFileData(filename):
    """Function to read in data from an input file and return the list containing the file data"""
    fileData = []
    with open(filename) as file:
        for line in file:
            fileData.append(line.rstrip('\n'))
    return fileData

def scoreAutocomplete(autocmpleteList):
    delimiterPointsComplete = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }
    score = 0
    for char in autocmpleteList:
        score *= 5
        score += delimiterPointsComplete[char]
    return score

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "inputTest.txt"
    
    navSubSystem = readFileData(filename)
    
    delimiterDict = {
        ')': '(',
        '}': '{',
        ']': '[',
        '>': '<'
    }

    # Part 1
    delimiterPoints = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    errorScore = 0
    for line in navSubSystem:
        chunkDelimiters = []
        for char in line:
            if char in delimiterDict.values():
                chunkDelimiters.append(char)
            elif char in delimiterDict:
                lastOpenChar = chunkDelimiters.pop()
                if lastOpenChar == delimiterDict[char]:
                    pass
                else:
                    # print(f"Expected match for '{lastOpenChar}' but got '{char}'")
                    errorScore += delimiterPoints[char]
            else:
                print("Unidentified delimier")
    print(f"Part 1 final score {errorScore}")

    # Part 2
    autocompletedScores = []
    for line in navSubSystem:
        completedChunkScore = 0
        chunkDelimiters = []
        for char in line:
            if char in delimiterDict.values():
                chunkDelimiters.append(char)
            elif char in delimiterDict:
                lastOpenChar = chunkDelimiters.pop()
                if lastOpenChar == delimiterDict[char]:
                    pass
                else:
                    chunkDelimiters = []
                    break
            else:
                print("Unidentified delimier")
        chunkDelimiters.reverse()
        completedChunkScore = scoreAutocomplete(chunkDelimiters)
        if completedChunkScore == 0:
            pass
        else:
            autocompletedScores.append(completedChunkScore)
    print(f"Part 2 final score {statistics.median(autocompletedScores)}")
