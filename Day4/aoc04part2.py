# Advent of Code Day 4 part 2

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
            #print(f"Checking rows and i is {i} and j is {j} and sheet value is {sheet[i][j]} and count is {countX}")
        if countX == len(sheet[0]):
            #print(f"True, count {countX} is length sheet[0] {len(sheet[0])}")
            return True
    for j in range(0,len(sheet[0])):
        countX = 0
        for i in range(0,len(sheet[0])):
            if sheet[i][j] == "X":
                countX += 1
            #print(f"Checking rows and i is {i} and j is {j} and sheet value is {sheet[i][j]} and count is {countX}")
        if countX == len(sheet[0]):
            #print(f"True, count {countX} is length sheet[0] {len(sheet[0])}")
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

def losingList(number, bingoSheets):
    newBingoSheets = []
    for sheet in bingoSheets:
        markSheet(number, sheet)
        #printSheet(sheet)
        #print('\n')
        if checkSheet(sheet) == False:
            newBingoSheets.append(sheet)
    return newBingoSheets

if __name__ == "__main__":

    sheetCount = 0
    bingoSheets = []
    sheetName = []

    filename = input("Enter the file containing the list Bingo Number Sheets: ")
    with open(filename) as file_object:
        # this builds a list of sheets but requires the input file to start with a 'newline' and end with two 'newlines'
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
    resultWin = sumSheet(sheet)
    print(f"Result found, sum is {resultWin} and product is {int(number)*int(resultWin)}")

    tempBingoSheets = bingoSheets
    for number in numberList:
        #print('\n')
        #print(f"All the fours {number}")
        #print(f'number of bongo sheets {len(tempBingoSheets)}')
        if len(tempBingoSheets) == 1:
            markSheet(number, tempBingoSheets[0])
            if checkSheet(tempBingoSheets[0]) == True:
                break
        tempBingoSheets = losingList(number, tempBingoSheets)
    
    printSheet(tempBingoSheets[0])
    resultLose = sumSheet(tempBingoSheets[0])
    print(f"Losing result found, sum is {resultLose} and product is {int(number)*int(resultLose)}")

    #tempSheet = [['34','35','X'],['45','46','X'],['55','56','X']]