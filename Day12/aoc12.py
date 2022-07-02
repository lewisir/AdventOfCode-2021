# Advent of Code Day 12 - Passage Pathing

import argparse

def readFileData(filename):
    """Function to read in data from an input file and return the processed file data"""
    fileData = []
    with open(filename) as file:
        for line in file:
            fileData.append(line.rstrip('\n'))
        fileData = [x.split('-') for x in fileData]
    return fileData

def createCaveGraph(caveConnections):
    """
    Takes a list of connections and creates a disctionary with keys that are the nodes (caves) and the values are a list of connected nodes (caves)
    It also ensures 'start' is never a destination and 'end' is never a source
    It duplicates entries to ensure bi-driectional connections between nodes (caves)
    """
    caveGraph = {}
    for connection in caveConnections:
        cave1 = connection[0]
        cave2 = connection[1]
        if cave1 == 'end' or cave2 == 'start': # make sure start is at the start and end is at the end
            cave1, cave2 = cave2, cave1
        if cave1 not in caveGraph.keys(): # create en an edge in the graph
            caveGraph[cave1] = [cave2]
        else:
            caveGraph[cave1].append(cave2)
        if cave1 == 'start' or cave2 == 'end': # duplicate the reverse entry if it doesn't contain start or end
            pass
        elif cave2 not in caveGraph.keys():
            caveGraph[cave2] = [cave1]
        else:
            caveGraph[cave2].append(cave1)
            pass
    return caveGraph

def printArray(array):
    """Pretty printing for an array"""
    TAB = '\t'
    SPACE = ' '
    for row in array:
        print(f"{SPACE.join(map(str,row))}")

def printGraph(caveGraph):
    """Pretty printing for a graph"""
    for cave in caveGraph:
        print(f"{cave}\t{caveGraph[cave]}")  

def testCavePath(path,node,smCvLmt):
    """Funciton to test whether the path so far could have the node added to it and not break the small cave visit limit"""
    pathList = path.split(',')
    maxSmCaveCount = 0
    for cave in pathList:
        if cave.islower():
            smCaveCount = pathList.count(cave)
        if smCaveCount > maxSmCaveCount:
            maxSmCaveCount = smCaveCount
    #print(f"with path ({path}) and node ({node}) and limit {smCvLmt} ",end='')
    if node.isupper() or node == 'start' or node == 'end':   # Big Caves, 'start' and 'end' are always OK to add. This leaves small caves to check
        #print(f"True isupper(), 'start' or 'end'")
        return True
    elif node not in pathList:              # Small caves that have never been visited are always OK to add
        #print(f"True new small cave for path")
        return True
    elif pathList.count(node) >= smCvLmt:   # If the small cave already appears enough times to reach the limit then you can't add it again
        #print(f"False count(node) >= limit")
        return False
    elif maxSmCaveCount >= smCvLmt:         # If any small cave has reached the limit, we don't visit any other small caves more than once
        #print(f"False maxSmCaveCount {maxSmCaveCount} is >= limit")
        return False
    else:
        #print(f"True - default")
        return True

def generatePaths(caveGraph,source,destination,allPaths,pathSoFar='',recursionLevel=0):
    """Function to search paths and add completed paths to the allPaths list."""
    recursionLevel += 1
    # recursionLevel is a way to display the print statements for debug and identify in which pass of the recursion each is occuring
    #print(f"  " * recursionLevel + f" {recursionLevel} genPaths called with source {source} and current path {pathSoFar}")
    if pathSoFar != '':
        pathSoFar = pathSoFar + ',' + source
    else:
        pathSoFar = source
    for node in caveGraph[source]:
        #print(f"  " * recursionLevel + f"   {recursionLevel} Checking node {node}")
        if node == destination:
            allPaths.append(pathSoFar + ',' + node)
            #print(f"  " * recursionLevel + f"   {recursionLevel}    found end and new path {allPaths[-1]} has been added")
        elif node != 'start' and node in pathSoFar and node.islower():
            pass
        else:
            generatePaths(caveGraph,node,destination,allPaths,pathSoFar,recursionLevel)

def genPaths2(caveGraph,source,destination,allPaths,pathSoFar='',smCvLmt=1,recursionLevel=0):
    """Function to search paths and add completed paths to the allPaths list. This includes a small cave limit allowing one small cave to be visited twice in a path"""
    recursionLevel += 1
    # recursionLevel is a way to display the print statements for debug and identify in which pass of the recursion each is occuring
    #print(f"  " * recursionLevel + f" {recursionLevel} genPaths called with source {source} and current path {pathSoFar}")
    if pathSoFar != '':
        pathSoFar = pathSoFar + ',' + source
    else:
        pathSoFar = source
    for node in caveGraph[source]:
        #print(f"  " * recursionLevel + f"   {recursionLevel} Checking node {node}")
        if node == destination:
            allPaths.append(pathSoFar + ',' + node)
            #print(f"  " * recursionLevel + f"   {recursionLevel}    found end and new path {allPaths[-1]} has been added")
        elif testCavePath(pathSoFar,node,smCvLmt):
            genPaths2(caveGraph,node,destination,allPaths,pathSoFar,smCvLmt,recursionLevel)

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "inputTest.txt"
    
    caveConnections = readFileData(filename)
    caveGraph = createCaveGraph(caveConnections)

    # printGraph(caveGraph)
    # Part 1
    myPaths = []
    generatePaths(caveGraph,'start','end',myPaths)
    #print(myPaths)
    print(f"Part 1. Number of Paths is {len(myPaths)}")
    myPaths = []
    genPaths2(caveGraph,'start','end',myPaths,'',2)
    #print(myPaths)
    print(f"Part 2. Number of Paths is {len(myPaths)}")

    