# Advent of Code Day 8

import argparse

def stringSubtract(string1,string2):
    """Function to remove the characters that are in string 2 from string 1 and return the resulting string"""
    returnString = ""
    for char1 in string1:
        match = False
        for char2 in string2:
            if char1 == char2:
                match = True
        if match == False:
            returnString += char1
    return returnString

def compareStrings(string1,string2):
    """Function to compare two strings and return the common characters that appear in both strings"""
    returnString = ""
    for char1 in string1:
        match = False
        for char2 in string2:
            if char1 == char2:
                returnString += char1
                break
    return returnString

def extractDisplays(displayList,length):
    """Function to return the strings from the list provided that match the length provided"""
    returnList = []
    for display in displayList:
        if len(display) == length:
            returnList.append(display)
    return returnList

def determineDigitMap(inputList):
    """Fuction takes in a list of the ten seven-segment displays and determines which charcters map to wich digits"""
    sevenCode = extractDisplays(inputList,3)[0]
    oneCode = extractDisplays(inputList,2)[0]
    fourCode = extractDisplays(inputList,4)[0]
    eightCode = extractDisplays(inputList,7)[0]
    fiveSegCodes = extractDisplays(inputList,5)
    sixSegCodes = extractDisplays(inputList,6)
    # Record the segment display as a dictionary which we can populate as we work out each signal wire
    segmentDisplay = {
        "Top":"",
        "TopLeft":"",
        "TopRight":"",
        "Middle":"",
        "BottomLeft":"",
        "BottomRight":"",
        "Bottom":""
    }
    # The top value is equal to display for (7) subtract display for (1)
    segmentDisplay["Top"] = stringSubtract(sevenCode,oneCode)
    # The common values between (2), (3) and (5) provide the Top, Middle and Bottom values
    tempString = compareStrings(fiveSegCodes[0],fiveSegCodes[1])
    topMiddleBottom = compareStrings(tempString,fiveSegCodes[2])
    # (4) subtract (1) provides middle and top left values
    middleTopLeft = stringSubtract(fourCode,oneCode)
    # Middle value is commone between (2)&(3)&(5) and (4)-(1)
    segmentDisplay["Middle"] = compareStrings(middleTopLeft,topMiddleBottom)
    # Bottom value is (2)&(3)&(5) - Top - Middle
    tempString = stringSubtract(topMiddleBottom,segmentDisplay["Middle"])
    segmentDisplay["Bottom"] = stringSubtract(tempString,segmentDisplay["Top"])
    # Top Left is (4)-(1) - Middle
    segmentDisplay["TopLeft"] = stringSubtract(middleTopLeft,segmentDisplay["Middle"])
    # Bottom Left is (8) - (7) - Middle - Bottom - TopLeft
    tempString = stringSubtract(eightCode,sevenCode)
    tempString = stringSubtract(tempString,segmentDisplay["Middle"])
    tempString = stringSubtract(tempString,segmentDisplay["Bottom"])
    segmentDisplay["BottomLeft"] = stringSubtract(tempString,segmentDisplay["TopLeft"])
    # Compare (1) with (0), (6) and (9), will return (1) apart from (6) where it returns bottom right only
    for code in sixSegCodes:
        tempString = compareStrings(oneCode,code)
        if len(tempString) == 1:
            segmentDisplay["BottomRight"] = tempString
    # Last value must be top right
    segmentDisplay["TopRight"] = stringSubtract(oneCode,segmentDisplay["BottomRight"])
    zeroCode = stringSubtract(eightCode,segmentDisplay["Middle"])
    sixCode = stringSubtract(eightCode,segmentDisplay["TopRight"])
    nineCode = stringSubtract(eightCode,segmentDisplay["BottomLeft"])
    fiveCode = stringSubtract(sixCode,segmentDisplay["BottomLeft"])
    twoCode = stringSubtract(eightCode,segmentDisplay["TopLeft"])
    threeCode = stringSubtract(twoCode,segmentDisplay["BottomLeft"])
    twoCode = stringSubtract(twoCode,segmentDisplay["BottomRight"])
    digitDict = {
        "0":''.join(sorted(zeroCode)),
        "1":''.join(sorted(oneCode)),
        "2":''.join(sorted(twoCode)),
        "3":''.join(sorted(threeCode)),
        "4":''.join(sorted(fourCode)),
        "5":''.join(sorted(fiveCode)),
        "6":''.join(sorted(sixCode)),
        "7":''.join(sorted(sevenCode)),
        "8":''.join(sorted(eightCode)),
        "9":''.join(sorted(nineCode))
    }
    return digitDict



if __name__ == "__main__":

    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "inputTest.txt"
    
    # Open the file and process the contents
    displayInputs = []
    with open(filename) as file:
        for line in file:
            displayInputs.append(line.rstrip('\n'))
            displayInputs[-1] = displayInputs[-1].split('|')
            displayInputs[-1][-1] = displayInputs[-1][-1].split()
            displayInputs[-1][-2] = displayInputs[-1][-2].split()
    
    # set a Tuple to to match for unique number of segments, these are the number of segments corresponding to numners 1 (2 segs), 4 (4 segs), 7 (3 segs) and 8 (7 segs)
    uniqueSegmentDigits = (2,3,4,7)

    # Work through the data to count the number of digits that are using a unique number of segments
    countDigits = 0
    for data in displayInputs:
        for digits in data[-1]:
            if len(digits) in uniqueSegmentDigits:
                countDigits += 1
    print(f"Part 1: Number of digits using a unique set of segments {countDigits}")
 
    # sort the test items and match each item to find what number it represents

    answerList = []
    for input in displayInputs:
        answerNum = ''
        numberMap = determineDigitMap(input[0])
        for number in input[1]:
            sortedNum = ''.join(sorted(number))
            for digit in numberMap:
                if numberMap[digit] == sortedNum:
                    answerNum += digit
        answerList.append(answerNum)
    
    intAnswList = [int(x) for x in answerList]
    print(f"Part 2: Sum of digits is {sum(intAnswList)}")