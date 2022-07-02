# Advent of Code Day 3 - Binary Diagnostic

def evaluateBinValue(binaryList, commonFlag):
    # with a list of binary numbers as input, take each bit position in turn and determine the most or least common value as controlled by the commonFlag
    # assume all input values are of the same length
    binValue = ''
    for i in range(0,len(binaryList[0])-1):
        count = 0
        for inputBinValue in binaryList:
            if inputBinValue[i] == "1":
                count += 1
            elif inputBinValue[i] == "0":
                count -= 1
        if count >= 0 and commonFlag == "most":   # Greater than or equal to used to handle part 2
            bitValue = "1"
        elif count < 0 and commonFlag == "most":
            bitValue = "0"
        elif count >= 0 and commonFlag == "least":   # Greater than or equal to used to handle part 2
            bitValue = "0"
        elif count < 0 and commonFlag == "least":
            bitValue = "1"
        else:
            print("binValue is undefined (equal 1's and 0's)")   # no longer needed as I catch == 0 above
        binValue = binValue + bitValue
    # The binValue is a binary string with the most or least common value in each bit position
    return binValue

# take a list of binary strings, and position and a bit value and reduce the list to contain those values that match the bit value in the bit position
def reduceList(list, position, bitVal):
    tempList = []
    for value in list:
        if value[position] == bitVal:
            tempList.append(value)
    return tempList



# Read in the file to binaryList
filename = input("Enter the file containing the list of numbers. ")
with open(filename) as file_object:
    binaryList = file_object.readlines()

print("gamma = " + evaluateBinValue(binaryList,"most") + " which is " + str(int(evaluateBinValue(binaryList,"most"),2)))
print("epsilon = " + evaluateBinValue(binaryList,"least") + " which is " + str(int(evaluateBinValue(binaryList,"least"),2)))
powerConsumption = int(evaluateBinValue(binaryList,"most"),2) * int(evaluateBinValue(binaryList,"least"),2)
print(powerConsumption)

listO2 = binaryList
binMask = evaluateBinValue(binaryList,"most")
for j in range(0,len(binMask)):
    if len(listO2) == 1:
        break
    binMask = evaluateBinValue(listO2,"most")
    listO2 = reduceList(listO2,j,binMask[j])
print("Oxygen Generator Rating " + listO2[0] + " which is " + str(int(listO2[0],2)))

listCo2 = binaryList
binMask = evaluateBinValue(binaryList,"least")
for j in range(0,len(binMask)):
    if len(listCo2) == 1:
        break
    binMask = evaluateBinValue(listCo2,"least")
    listCo2 = reduceList(listCo2,j,binMask[j])
print("CO2 Scrubber Rating " + listCo2[0] + " which is " + str(int(listCo2[0],2)))

print("Life Support Rating is " + str(int(listO2[0],2)*int(listCo2[0],2)))
