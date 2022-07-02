# Advent of Code Day 4 part 1 - Giant Squid

def markSheet(number,sheet):
    """This function searches the numbers in the sheet and if the number is found marks it with an 'X'"""
    for i in range(0,len(sheet[0])):
        for j in range(0,len(sheet[0])):
            if sheet[i][j] == number:
                sheet[i][j] = "X"

def checkSheet(sheet):
    """This function checks to see if any rows or any columns are all marked in the sheet"""
    for i in range(0,len(sheet[0])):
        countX = 0
        for j in range(0,len(sheet[0])):
            if sheet[i][j] == "X":
                countX += 1
        if countX == len(sheet[0]):
            return True
    for j in range(0,len(sheet[0])):
        countX = 0
        for i in range(0,len(sheet[0])):
            if sheet[i][j] == "X":
                countX += 1
        if countX == len(sheet[0]):
            return True
    return False

def sumSheet(sheet):
    """This function adds up the numbers in the sheet that are not marked"""
    sum = 0
    for i in range(0,len(sheet[0])):
        for j in range(0,len(sheet[0])):
            if sheet[i][j] == "X":
                continue
            sum += int(sheet[i][j])
    return sum

def printSheet(sheet):
    TAB = '\t'
    for row in sheet:
        print(f"{TAB.join(map(str,row))}")


sheetCount = 0
bingoSheets = []
sheetName = []

filename = input("Enter the file containing the list Bingo Number Sheets: ")
with open(filename) as file_object:
    # this builds a list of sheets but requires the input file to start with a 'newline' and end with two newlines
    for line in file_object:
        if line == "\n":
            if len(sheetName) > 0:
                sheetName = [line.split() for line in sheetName]
                bingoSheets.append(sheetName)
            sheetCount += 1
            sheetName = []
        else:
            sheetName.append(line)

filename = input("Enter the bingo file containing the numbers called: ")
with open(filename) as file_object:
    numberList = file_object.readlines()
# this creates a list of the bingo numbers called and requires them to be comma separated with no spaces
numberList = numberList[0].split(",")

for number in numberList:
    for sheet in bingoSheets:
        markSheet(number, sheet)
        if checkSheet(sheet) == True:
            break
    if checkSheet(sheet) == True:
        break

printSheet(sheet)
result = sumSheet(sheet)
print(f"Result found, sum is {result} and product is {int(number)*int(result)}")