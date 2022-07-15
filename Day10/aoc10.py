"""Advent of Code Day 10 - Syntax Scoring"""

import argparse
import statistics
import doctest

def read_file_data(filename):
    """
    Function to read in data from an input file and return the list containing the file data

    If the file contains the following:
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}

    The then returned file_data is:
    ["[({(<(())[]>[[{[]{<()<>>","[(()[<>])]({[<{<<[]>>(","{([(<{}[<>[]}>{[]{[(<()>","(((({<>}<{<{<>}{[]{[]{}"]
    """
    fileData = []
    with open(filename) as file:
        for line in file:
            fileData.append(line.rstrip('\n'))
    return fileData

def score_auto_complete(autocomplete_list):
    """
    Function takes a list of opening delimiters and calculates the points that this scores

    >>> score_auto_complete(['(','[','{','<'])
    194
    """
    delimiter_points_complete = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }
    score = 0
    for char in autocomplete_list:
        score *= 5
        score += delimiter_points_complete[char]
    return score

if __name__ == "__main__":
    # Handle command line argument for the input filename
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Filename for the data input")
    args = parser.parse_args()
    if args.file:
        filename = args.file
    else:
        filename = "Day10/inputTest.txt"

    nav_sub_system = read_file_data(filename)

    doctest.testmod()

    # delimiter_dict records the matching closing and opeing delimiter characters
    delimiter_dict = {
        ')': '(',
        '}': '{',
        ']': '[',
        '>': '<'
    }

    # Part 1
    """
    Take each input line, which is a line of opening and closing delimiter characters
    For example {([(<{}[<>[]}>{[]{[(<()>
    For each charcter check if it's an opening character and it to the chunk_delimiters list
    For example {([(<{ are the first continuous opening delimiters in the string above
    If it's a closing delimiter and it matches the last opening delimiter,
     remove the last opening delimiter from chunk_delimiters
    For example '}' is found when the chunk_delimiters contains {([(<{, it becomes {([(<
    If it doesn't then increment the error_score
    For example '}' is found when the chunk_delimiters contains {([(<[,
     this causes the error to increment by the points for '}'
    """
    delimiter_points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    error_score = 0
    for line in nav_sub_system:
        chunk_delimiters = []
        for char in line:
            if char in delimiter_dict.values():
                chunk_delimiters.append(char)
            elif char in delimiter_dict:
                last_open_delimiter = chunk_delimiters.pop()
                if last_open_delimiter == delimiter_dict[char]:
                    pass
                else:
                    # print(f"Expected match for '{last_open_delimiter}' but got '{char}'")
                    error_score += delimiter_points[char]
            else:
                print("Unidentified delimiter")
    print(f"Part 1 final score {error_score}")

    # Part 2 - correctly complete the incomplete strings with the right closing delimiters
    """
    Work through each string recording the opening delimiters in the chunk_delimiters list
    Remove the opening character if it matches a closing delimiter
    The remaining unmatched opening characters are passed to be scored
    All scores are recorded in teh autocomplete_scores list
    """
    autocomplete_scores = []
    for line in nav_sub_system:
        completed_chunk_score = 0
        chunk_delimiters = []
        for char in line:
            if char in delimiter_dict.values():
                chunk_delimiters.append(char)
            elif char in delimiter_dict:
                last_open_delimiter = chunk_delimiters.pop()
                # Check if this string is incorrect rather than incomplete
                if last_open_delimiter != delimiter_dict[char]:
                    chunk_delimiters = []
                    break
            else:
                print("Unidentified delimier")
        chunk_delimiters.reverse()
        completed_chunk_score = score_auto_complete(chunk_delimiters)
        if completed_chunk_score != 0:
            autocomplete_scores.append(completed_chunk_score)
    print(f"Part 2 final score {statistics.median(autocomplete_scores)}")
