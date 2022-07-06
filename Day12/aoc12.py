# Advent of Code Day 12 - Passage Pathing

import argparse
import doctest

def readFileData(filename):
    """
    Function to read in data from an input file and return the processed file data

    For a file containing:
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end

    The returned fileData shall be:
    [['start', 'A'], ['start', 'b'], ['A', 'c'], ['A', 'b'], ['b', 'd'], ['A', 'end'], ['b', 'end']]

    """
    fileData = []
    with open(filename) as file:
        for line in file:
            fileData.append(line.rstrip('\n'))
        fileData = [x.split('-') for x in fileData]
    return fileData

def createCaveGraph(caveConnections):
    """
    Takes a list of connections and creates a dictionary
    The keys that are the nodes (caves) and the values are a list of connected nodes (caves)
    It also ensures 'start' is never a destination and 'end' is never a source
    It duplicates entries to ensure bi-driectional connections between nodes (caves)

    For this list of connections:
    [['start', 'A'], ['start', 'b'], ['A', 'c'], ['A', 'b'], ['b', 'd'], ['A', 'end'], ['b', 'end']]

    The following dictionary is returned:
    {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}

    >>> caveConnections = [['start', 'A'], ['b', 'start'], ['A', 'c'], ['A', 'b'], ['b', 'd'], ['A', 'end'], ['b', 'end']]
    >>> print(createCaveGraph(caveConnections))
    {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    """
    caveGraph = {}
    for connection in caveConnections:
        cave1 = connection[0]
        cave2 = connection[1]
        if cave1 == 'end' or cave2 == 'start':  # make sure start is at the start and end is at the end
            cave1, cave2 = cave2, cave1
        if cave1 not in caveGraph.keys():       # create en an edge in the graph
            caveGraph[cave1] = [cave2]
        else:
            caveGraph[cave1].append(cave2)
        if cave1 == 'start' or cave2 == 'end':  # duplicate the reverse entry if it doesn't contain start or end
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

def generatePaths(caveGraph,source,destination,allPaths,pathSoFar='',recursionLevel=0):
    """
    A recursive function to search paths and add completed paths to the allPaths list.

    parameters:
     caveGraph: A dictionary of the cave connections
     source: A string containing the starting location (typically 'start')
     destination: A string containing the end location (typically 'end')
     allPaths: A list containing all of the paths discovered (each path is a string of caves)
     pathSoFar: A string containg the current caves in the path (comma seaparetd caves)
     recustionLevel: An integer to help debugging the recusrive function
    
    For the caveGraph
    {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    using 'start' and 'end' as the source and destintion
    
    The following paths are found:
    ['start,A,c,A,b,A,end', 'start,A,c,A,b,end', 'start,A,c,A,end', 'start,A,b,A,c,A,end',
     'start,A,b,A,end', 'start,A,b,end', 'start,A,end', 'start,b,A,c,A,end', 'start,b,A,end', 'start,b,end']

    >>> caveGraph = {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    >>> allPaths = []
    >>> generatePaths(caveGraph,'start','end',allPaths)
    >>> print(allPaths)
    ['start,A,c,A,b,A,end', 'start,A,c,A,b,end', 'start,A,c,A,end', 'start,A,b,A,c,A,end', 'start,A,b,A,end', 'start,A,b,end', 'start,A,end', 'start,b,A,c,A,end', 'start,b,A,end', 'start,b,end']
    """
    recursionLevel += 1
    if pathSoFar != '':
        pathSoFar = pathSoFar + ',' + source
    else:
        pathSoFar = source
    for node in caveGraph[source]:
        if node == destination:
            allPaths.append(pathSoFar + ',' + node)
        elif node != 'start' and node in pathSoFar and node.islower():
            pass
        else:
            generatePaths(caveGraph,node,destination,allPaths,pathSoFar,recursionLevel)

def testCavePath(path,node,smCvLmt):
    """
    Funciton to test whether the path so far could have the cave added to it and not break the small cave visit limit

    Parameters
     path: A string of comma sepaarted nodes/caves
     node: A string which is a cave
     smCvLmt: An integer controlling the number of times a single small cave can be visited
    
    Returns
        Boolean

    The most times a singel cave appears in the path is recorded in teh maxSmCaveCount
    If any small cave has reached the smCvLmt we only add a small cave if it's not already in the path
    
    >>> path = 'start,A,b,C,d'
    >>> testCavePath(path,'A',2)
    True
    >>> testCavePath(path,'e',2)
    True
    >>> testCavePath(path,'b',2)
    True
    >>> testCavePath(path,'end',2)
    True
    >>> path = 'start,A,b,C,d,b'
    >>> testCavePath(path,'b',2)
    False
    >>> testCavePath(path,'d',2)
    False
    >>> testCavePath(path,'F',2)
    True
    """
    pathList = path.split(',')
    maxSmCaveCount = 0
    for cave in pathList:
        if cave.islower():
            smCaveCount = pathList.count(cave)
        if smCaveCount > maxSmCaveCount:
            maxSmCaveCount = smCaveCount
    if node.isupper() or node == 'start' or node == 'end':   # Big Caves and 'start' and 'end' are always OK to add
        return True
    elif node not in pathList:       # Small caves that have never been visited are always OK to add
        return True
    elif maxSmCaveCount >= smCvLmt:  # If any small cave has reached the limit, we don't visit any other small caves more than once
        return False
    else:
        return True

def genPaths2(caveGraph,source,destination,allPaths,pathSoFar='',smCvLmt=1,recursionLevel=0):
    """
    A recursive function to search paths and add completed paths to the allPaths list.
    This includes a small cave limit allowing one small cave to be visited twice in a path

    parameters:
     caveGraph: A dictionary of the cave connections
     source: A string containing the starting location (typically 'start')
     destination: A string containing the end location (typically 'end')
     allPaths: A list containing all of the paths discovered (each path is a string of caves)
     pathSoFar: A string containg the current caves in the path (comma seaparetd caves)
     smCvLmt: An integer controlling the number of times a single small cave can be visited
     recustionLevel: An integer to help debugging the recusrive function
    
    For the caveGraph
    {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    using 'start' and 'end' as the source and destintion
    
    The following paths are found:
    ['start,A,c,A,c,A,b,A,end', 'start,A,c,A,c,A,b,end', 'start,A,c,A,c,A,end', 'start,A,c,A,b,A,c,A,end',
     'start,A,c,A,b,A,b,A,end', 'start,A,c,A,b,A,b,end', 'start,A,c,A,b,A,end', 'start,A,c,A,b,d,b,A,end',
     'start,A,c,A,b,d,b,end', 'start,A,c,A,b,end', 'start,A,c,A,end', 'start,A,b,A,c,A,c,A,end', 
     'start,A,b,A,c,A,b,A,end', 'start,A,b,A,c,A,b,end', 'start,A,b,A,c,A,end', 'start,A,b,A,b,A,c,A,end', 
     'start,A,b,A,b,A,end', 'start,A,b,A,b,end', 'start,A,b,A,end', 'start,A,b,d,b,A,c,A,end', 
     'start,A,b,d,b,A,end', 'start,A,b,d,b,end', 'start,A,b,end', 'start,A,end', 'start,b,A,c,A,c,A,end', 
     'start,b,A,c,A,b,A,end', 'start,b,A,c,A,b,end', 'start,b,A,c,A,end', 'start,b,A,b,A,c,A,end', 
     'start,b,A,b,A,end', 'start,b,A,b,end', 'start,b,A,end', 'start,b,d,b,A,c,A,end', 'start,b,d,b,A,end', 
     'start,b,d,b,end', 'start,b,end']

    >>> caveGraph = {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    >>> allPaths = []
    >>> genPaths2(caveGraph,'start','end',allPaths,'',2)
    >>> print(allPaths)
    ['start,A,c,A,c,A,b,A,end', 'start,A,c,A,c,A,b,end', 'start,A,c,A,c,A,end', 'start,A,c,A,b,A,c,A,end', 'start,A,c,A,b,A,b,A,end', 'start,A,c,A,b,A,b,end', 'start,A,c,A,b,A,end', 'start,A,c,A,b,d,b,A,end', 'start,A,c,A,b,d,b,end', 'start,A,c,A,b,end', 'start,A,c,A,end', 'start,A,b,A,c,A,c,A,end', 'start,A,b,A,c,A,b,A,end', 'start,A,b,A,c,A,b,end', 'start,A,b,A,c,A,end', 'start,A,b,A,b,A,c,A,end', 'start,A,b,A,b,A,end', 'start,A,b,A,b,end', 'start,A,b,A,end', 'start,A,b,d,b,A,c,A,end', 'start,A,b,d,b,A,end', 'start,A,b,d,b,end', 'start,A,b,end', 'start,A,end', 'start,b,A,c,A,c,A,end', 'start,b,A,c,A,b,A,end', 'start,b,A,c,A,b,end', 'start,b,A,c,A,end', 'start,b,A,b,A,c,A,end', 'start,b,A,b,A,end', 'start,b,A,b,end', 'start,b,A,end', 'start,b,d,b,A,c,A,end', 'start,b,d,b,A,end', 'start,b,d,b,end', 'start,b,end']
    """
    recursionLevel += 1
    if pathSoFar != '':
        pathSoFar = pathSoFar + ',' + source
    else:
        pathSoFar = source
    for node in caveGraph[source]:
        if node == destination:
            allPaths.append(pathSoFar + ',' + node)
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
    
    doctest.testmod()

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

    