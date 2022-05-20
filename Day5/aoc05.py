# Advent of Code Day 5

# Vents are provided in the input file as line segments like "3,4 -> 3,9"
# Need to determine at how many ports there's more than one line segment

# A function to plot a line on a map, given the map and a line

def createVentMap(size):
    # Create a map of a given size
    ventMap = []
    line = "."*size
    for i in range(0,size):
        ventMap.append(line)
    ventMap = [list(x) for x in ventMap]
    return ventMap

def printSheet(sheet):
    # Nice print of a two dimesional array
    TAB = '\t'
    SPACE = ' '
    for row in sheet:
        print(f"{SPACE.join(map(str,row))}")

def addLineSegment(ventMap, x_start, y_start, x_end, y_end):  # this works for horizontal and vertical lines only
    # make sure start value is smaller than end value
    if x_start > x_end:
        x_start, x_end = x_end, x_start
    if y_start > y_end:
        y_start, y_end = y_end, y_start
    for y in range(y_start, y_end+1):
        for x in range(x_start, x_end+1):
            if ventMap[y][x] == ".":
                ventMap[y][x] = 1
            else:
                ventMap[y][x] += 1
    return ventMap

def addLineSegmentII(ventMap, x_start, y_start, x_end, y_end):
    # New function to add horizontal, vertical or 45 degree diagonal lines
    draw = True
    x_step = 0
    y_step = 0
    x, y = x_start, y_start
    if x_start > x_end:
        x_step = -1
    elif x_start < x_end:
        x_step = 1
    if y_start > y_end:
        y_step = -1
    elif y_start < y_end:
        y_step = 1
    while draw == True:
        if ventMap[y][x] == ".":
            ventMap[y][x] = 1
        else:
            ventMap[y][x] += 1
        if x == x_end and y == y_end:
            draw = False
        x += x_step
        y += y_step
    return ventMap

def countOverlappingVents(ventMap):
    count = 0
    for y in range(len(ventMap)):
        for x in range(len(ventMap[0])):
            if ventMap[y][x] == ".":
                pass
            elif ventMap[y][x] > 1:
                count +=1
    return count

if __name__ == "__main__":
    lineSegments = []
    filename = input("Enter the file containing the vent data: ")
    with open(filename) as file_object:
        for line in file_object:
            lineSegments = file_object.readlines()
    # For some reason the input file needs to start with a blank line in order to pick up the first line ????????
    lineSegments = [line.strip() for line in lineSegments]
    lineSegments = [line.split(' -> ') for line in lineSegments]
    lineSegments = [[endPoint.split(',') for endPoint in line] for line in lineSegments]
    lineSegments = [[[int(coOrdinate) for coOrdinate in endPoint] for endPoint in line] for line in lineSegments]

    # find the maximum coordinate value and create a vent map that's big enough
    maxCoord = 0 
    for line in lineSegments:
        for endPoint in line:
            for coOrdinate in endPoint:
                if coOrdinate > maxCoord:
                    maxCoord = coOrdinate
    # print(maxCoord)
    ventMap = createVentMap(maxCoord+1)

    # add line segments to the map if they are horizontal or vertical
    for line in lineSegments:
        x_start = line[0][0]
        x_end = line[1][0]
        y_start = line[0][1]
        y_end = line[1][1]
        #print(f"coordinate are {x_start},{y_start} and {x_end},{y_end}")
        # This checks if the lines are horizontal or vertical before adding them to the map
        if x_start == x_end or y_start == y_end:
            addLineSegmentII(ventMap,x_start,y_start,x_end,y_end)
        # This checks if the line is 45 degress before adding them to the map
        if abs(x_start-x_end) == abs(y_start-y_end):
            addLineSegmentII(ventMap,x_start,y_start,x_end,y_end)
        #printSheet(ventMap)
    
    print(f"Number of overlapping vents is {countOverlappingVents(ventMap)}")
