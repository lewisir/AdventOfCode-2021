"""Advent of Code Day 12 - Passage Pathing"""

import argparse
import doctest

def readfile_data(filename):
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

    The returned file_data shall be:
    [['start', 'A'], ['start', 'b'], ['A', 'c'], ['A', 'b'], ['b', 'd'], ['A', 'end'], ['b', 'end']]

    """
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip('\n'))
        file_data = [x.split('-') for x in file_data]
    return file_data

def create_cave_graph(cave_connections):
    """
    Takes a list of connections and creates a dictionary
    The keys that are the nodes (caves) and the values are a list of connected nodes (caves)
    It also ensures 'start' is never a destination and 'end' is never a source
    It duplicates entries to ensure bi-driectional connections between nodes (caves)

    For this list of connections:
    [['start', 'A'], ['start', 'b'], ['A', 'c'], ['A', 'b'], ['b', 'd'], ['A', 'end'], ['b', 'end']]

    The following dictionary is returned:
    {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}

    >>> cave_connections = [['start', 'A'], ['b', 'start'], ['A', 'c'], ['A', 'b'], ['b', 'd'], ['A', 'end'], ['b', 'end']]
    >>> print(create_cave_graph(cave_connections))
    {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    """
    cave_graph = {}
    for connection in cave_connections:
        cave1 = connection[0]
        cave2 = connection[1]
        if cave1 == 'end' or cave2 == 'start':  # make sure start is at the start and end is at the end
            cave1, cave2 = cave2, cave1
        if cave1 not in cave_graph.keys():       # create en an edge in the graph
            cave_graph[cave1] = [cave2]
        else:
            cave_graph[cave1].append(cave2)
        if cave1 == 'start' or cave2 == 'end':  # duplicate the reverse entry if it doesn't contain start or end
            pass
        elif cave2 not in cave_graph.keys():
            cave_graph[cave2] = [cave1]
        else:
            cave_graph[cave2].append(cave1)
            pass
    return cave_graph

def print_array(array):
    """Pretty printing for an array"""
    TAB = '\t'
    SPACE = ' '
    for row in array:
        print(f"{SPACE.join(map(str,row))}")

def print_graph(cave_graph):
    """Pretty printing for a graph"""
    for cave in cave_graph:
        print(f"{cave}\t{cave_graph[cave]}")  

def generate_paths(cave_graph,source,destination,all_paths,paths_so_far='',recurse_level=0):
    """
    A recursive function to search paths and add completed paths to the all_paths list.

    parameters:
     cave_graph: A dictionary of the cave connections
     source: A string containing the starting location (typically 'start')
     destination: A string containing the end location (typically 'end')
     all_paths: A list containing all of the paths discovered (each path is a string of caves)
     paths_so_far: A string containg the current caves in the path (comma seaparetd caves)
     recustionLevel: An integer to help debugging the recusrive function

    For the cave_graph
    {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    using 'start' and 'end' as the source and destintion

    The following paths are found:
    ['start,A,c,A,b,A,end', 'start,A,c,A,b,end', 'start,A,c,A,end', 'start,A,b,A,c,A,end',
     'start,A,b,A,end', 'start,A,b,end', 'start,A,end', 'start,b,A,c,A,end', 'start,b,A,end',
     'start,b,end']

    >>> cave_graph = {'start':['A','b'], 'A':['c','b','end'], 'c':['A'], 'b':['A','d','end'], 'd':['b']}
    >>> all_paths = []
    >>> generate_paths(cave_graph,'start','end',all_paths)
    >>> print(all_paths)
    ['start,A,c,A,b,A,end', 'start,A,c,A,b,end', 'start,A,c,A,end', 'start,A,b,A,c,A,end', 'start,A,b,A,end', 'start,A,b,end', 'start,A,end', 'start,b,A,c,A,end', 'start,b,A,end', 'start,b,end']
    """
    recurse_level += 1
    if paths_so_far != '':
        paths_so_far = paths_so_far + ',' + source
    else:
        paths_so_far = source
    for node in cave_graph[source]:
        if node == destination:
            all_paths.append(paths_so_far + ',' + node)
        elif node != 'start' and node in paths_so_far and node.islower():
            pass
        else:
            generate_paths(cave_graph,node,destination,all_paths,paths_so_far,recurse_level)

def test_path(path,node,small_cave_limit):
    """
    Funciton to test whether the path so far could have the cave added to it
     and not break the small cave visit limit

    Parameters
     path: A string of comma sepaarted nodes/caves
     node: A string which is a cave
     small_cave_limit: An integer controlling the number of times a single small cave can be visited

    Returns
        Boolean

    The most times a singel cave appears in the path is recorded in teh max_small_cave_count
    If any small cave has reached the small_cave_limit we only add a small cave if
     it's not already in the path

    >>> path = 'start,A,b,C,d'
    >>> test_path(path,'A',2)
    True
    >>> test_path(path,'e',2)
    True
    >>> test_path(path,'b',2)
    True
    >>> test_path(path,'end',2)
    True
    >>> path = 'start,A,b,C,d,b'
    >>> test_path(path,'b',2)
    False
    >>> test_path(path,'d',2)
    False
    >>> test_path(path,'F',2)
    True
    """
    path_list = path.split(',')
    max_small_cave_count = 0
    for cave in path_list:
        if cave.islower():
            small_cave_count = path_list.count(cave)
        if small_cave_count > max_small_cave_count:
            max_small_cave_count = small_cave_count
    if node.isupper() or node == 'start' or node == 'end':   # Big Caves and 'start' and 'end' are always OK to add
        return True
    elif node not in path_list:       # Small caves that have never been visited are always OK to add
        return True
    elif max_small_cave_count >= small_cave_limit:  # If any small cave has reached the limit, we don't visit any other small caves more than once
        return False
    else:
        return True

def gen_paths_02(cave_graph,source,destination,all_paths,paths_so_far='',small_cave_limit=1,recurse_level=0):
    """
    A recursive function to search paths and add completed paths to the all_paths list.
    This includes a small cave limit allowing one small cave to be visited twice in a path

    parameters:
     cave_graph: A dictionary of the cave connections
     source: A string containing the starting location (typically 'start')
     destination: A string containing the end location (typically 'end')
     all_paths: A list containing all of the paths discovered (each path is a string of caves)
     paths_so_far: A string containg the current caves in the path (comma seaparetd caves)
     small_cave_limit: An integer controlling the number of times a single small cave can be visited
     recustionLevel: An integer to help debugging the recusrive function

    For the cave_graph
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

    >>> cave_graph = {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['A', 'd', 'end'], 'd': ['b']}
    >>> all_paths = []
    >>> gen_paths_02(cave_graph,'start','end',all_paths,'',2)
    >>> print(all_paths)
    ['start,A,c,A,c,A,b,A,end', 'start,A,c,A,c,A,b,end', 'start,A,c,A,c,A,end', 'start,A,c,A,b,A,c,A,end', 'start,A,c,A,b,A,b,A,end', 'start,A,c,A,b,A,b,end', 'start,A,c,A,b,A,end', 'start,A,c,A,b,d,b,A,end', 'start,A,c,A,b,d,b,end', 'start,A,c,A,b,end', 'start,A,c,A,end', 'start,A,b,A,c,A,c,A,end', 'start,A,b,A,c,A,b,A,end', 'start,A,b,A,c,A,b,end', 'start,A,b,A,c,A,end', 'start,A,b,A,b,A,c,A,end', 'start,A,b,A,b,A,end', 'start,A,b,A,b,end', 'start,A,b,A,end', 'start,A,b,d,b,A,c,A,end', 'start,A,b,d,b,A,end', 'start,A,b,d,b,end', 'start,A,b,end', 'start,A,end', 'start,b,A,c,A,c,A,end', 'start,b,A,c,A,b,A,end', 'start,b,A,c,A,b,end', 'start,b,A,c,A,end', 'start,b,A,b,A,c,A,end', 'start,b,A,b,A,end', 'start,b,A,b,end', 'start,b,A,end', 'start,b,d,b,A,c,A,end', 'start,b,d,b,A,end', 'start,b,d,b,end', 'start,b,end']
    """
    recurse_level += 1
    if paths_so_far != '':
        paths_so_far = paths_so_far + ',' + source
    else:
        paths_so_far = source
    for node in cave_graph[source]:
        if node == destination:
            all_paths.append(paths_so_far + ',' + node)
        elif test_path(paths_so_far,node,small_cave_limit):
            gen_paths_02(cave_graph,node,destination,all_paths,paths_so_far,small_cave_limit,recurse_level)

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day12/inputTest.txt"

    doctest.testmod()

    cave_connections = readfile_data(filename)
    cave_graph = create_cave_graph(cave_connections)

    # print_graph(cave_graph)
    # Part 1
    myPaths = []
    generate_paths(cave_graph,'start','end',myPaths)
    #print(myPaths)
    print(f"Part 1. Number of Paths is {len(myPaths)}")
    myPaths = []
    gen_paths_02(cave_graph,'start','end',myPaths,'',2)
    #print(myPaths)
    print(f"Part 2. Number of Paths is {len(myPaths)}")
   