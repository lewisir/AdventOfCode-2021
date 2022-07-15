"""
Advent of Code Day 14 - Extended Polymerization
"""
import argparse
import doctest

def read_file_data(filename):
    """
    Function to read in data from an input file and return the processed file data

    For an input like this:
        NNCB

        CB -> H
        NN -> C
        NC -> B

    The return_data contains:
        [{'CB': 'H', 'NN': 'C', 'NC': 'B'}, ['NNCB']]
    """
    pair_insertions = {}
    polymer_template = ''
    with open(filename) as file:
        for line in file:
            if line[3:5] == '->':
                pair_insertions[line[:2]] = line.rstrip('\n')[-1:]
            elif len(line) > 1 :
                polymer_template = [line.rstrip('\n')]
    return_data = [pair_insertions,polymer_template]
    return return_data

def polymerise_pair(element_pair, steps, pair_insertions):
    """
    Given an element pair and a number of steps,
     iterate the element pair to determine the count of new pairs

    >>> pair_insertions =  {'CN': 'C', 'NN': 'C', 'NC': 'B'}
    >>> print(polymerise_pair('NN', 1, pair_insertions))
    [{'NC': 1, 'CN': 1}]
    >>> print(polymerise_pair('NN', 2, pair_insertions))
    [{'NB': 1, 'BC': 1, 'CC': 1, 'CN': 1}]
    """
    step = 0
    pair_count = [{element_pair: 1}]
    while step < steps:
        step += 1
        temp_dict = {}
        for pair in pair_count[-1]:
            new_element = pair_insertions[pair]
            new_pair1 = pair[0]+new_element
            new_pair2 = new_element+pair[1]
            if new_pair1 in temp_dict:
                temp_dict[new_pair1] += pair_count[-1][pair]
            else:
                temp_dict[new_pair1] = pair_count[-1][pair]
            if new_pair2 in temp_dict:
                temp_dict[new_pair2] += pair_count[-1][pair]
            else:
                temp_dict[new_pair2] = pair_count[-1][pair]
        del pair_count[0]
        pair_count.append(temp_dict)
    return pair_count

def count_final_inserts(polymer_dict):
    """
    Function to count the number of times elements appear in the keys of the dictionary
    Each element is multiplied by the value stored against the key in which it appears

    Given a polymer_dict like this:
    >>> polymer_dict = {'NB': 1, 'BB': 2, 'BC': 1, 'CN': 2, 'NC': 1, 'CC': 1}
    >>> print(count_final_inserts(polymer_dict))
    {'N': 4, 'B': 6, 'C': 6}
    """
    element_count_dict = {}
    for pair in polymer_dict:
        element1 = pair[0]
        element2 = pair[1]
        if element1 in element_count_dict:
            element_count_dict[element1] += polymer_dict[pair]
        else:
            element_count_dict[element1] = polymer_dict[pair]
        if element2 in element_count_dict:
            element_count_dict[element2] += polymer_dict[pair]
        else:
            element_count_dict[element2] = polymer_dict[pair]
    return element_count_dict

def adjust_elelment_count(element_count_dict, starting_pair):
    """
    Adjust the element counts to accomdate the fact that each element is counted twice,
     except for the elements at the ends of the polymer
    The ends of the polymer are provided by the starting_pair
    Subtract from the count the starting_pair,
     divide all values by 2 and then add on the staring_pair

    >>> element_count_dict = {'N': 6, 'B': 10, 'C': 12}
    >>> print(adjust_elelment_count(element_count_dict, 'NN'))
    {'N': 4, 'B': 5, 'C': 6}
    """
    # Can I check starting_pair is a two character string only?
    starting_elelemt1 = starting_pair[0]
    starting_elelemt2 = starting_pair[1]
    element_count_dict[starting_elelemt1] -= 1
    element_count_dict[starting_elelemt2] -= 1
    for element, count in element_count_dict.items():
        element_count_dict[element] = count//2
    element_count_dict[starting_elelemt1] += 1
    element_count_dict[starting_elelemt2] += 1
    return element_count_dict

def combine_dictionaries(dict1, dict2):
    """
    Function will take two dictionaores that contains integers values
    Combine the two dictionaries to return a singe dictionary that adds the
     integers where keys are the same
    >>> dict1 = {'A': 12, 'B': 3, 'C': 9}
    >>> dict2 = {'A': 4, 'C': 7, 'D': 4}
    >>> print(combine_dictionaries(dict1, dict2))
    {'A': 16, 'B': 3, 'C': 16, 'D': 4}
    """
    return_dict = {}
    for key, value in dict1.items():
        return_dict[key] = value
    for key, value in dict2.items():
        if key in return_dict:
            return_dict[key] += value
        else:
            return_dict[key] = value
    return return_dict

def polymersie_polymer(polymer, steps, pair_insertions):
    """
    Given a polymer string, iterate through each pair in the polymer
    to ploymerise it and return a dictionaty of the element counts
    """
    total_pairs_count = {}
    end_elements = polymer[0]+polymer[-1]
    for x in range(len(polymer)-1):
        pair = polymer[x:x+2]
        temp_pairs_count = polymerise_pair(pair, steps, pair_insertions)[-1]
        total_pairs_count = combine_dictionaries(total_pairs_count, temp_pairs_count)
    total_element_counts = adjust_elelment_count(count_final_inserts(total_pairs_count),end_elements)
    return total_element_counts

def max_value(input_dict):
    """
    For a dictionary containing number values, return the greatest number value

    >>> input_dict = {'A': 1, 'B': 12, 'C': 3, 'D': 9}
    >>> max_value(input_dict)
    12
    """
    max_value = 0
    for x in input_dict.values():
        if x > max_value:
            max_value = x
    return max_value

def min_value(input_dict):
    """
    For a dictionary containing number values, return the least number value

    >>> input_dict = {'A': 1, 'B': 12, 'C': 3, 'D': 9}
    >>> min_value(input_dict)
    1
    """
    min_value = float('inf')
    for x in input_dict.values():
        if x < min_value:
            min_value = x
    return min_value
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    parser.add_argument("--steps", help="Number of steps to iterate over")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day14/inputTest.txt"
    if args.steps:
        steps = int(args.steps)
    else:
        steps = 10

    doctest.testmod()

    output = read_file_data(filename)
    pair_insertions = output[0]
    starting_polymer = output[1][0]

    end_polymer = polymersie_polymer(starting_polymer, steps, pair_insertions)
    element_difference = max_value(end_polymer) - min_value(end_polymer)
    print(f"The element difference after {steps} steps is {element_difference}")
