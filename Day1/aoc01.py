# Advent of Code Day 1

# Given an input file, which is a list of numbers, and a window size, count the number of times the number window is greater than the preceeding window

def count_increases(list, window_size):
    # Make sure the list is a list of integers and not strings
    # Is there a smarter way to check that the list contains numbers and error if it doesn't?
    int_list = [int(x) for x in list]
    count = 0
    # Run over all the numbers in the list up to the last value which depends on the window size
    for i in range(0,len(int_list)-window_size):
        # Calcualte the values of the two adjacent windows using a list slice
        window1 = sum(int_list[i:i+window_size])
        window2 = sum(int_list[i+1:i+1+window_size])
        if window2 > window1:
            count+=1
    return count

# Read in the file to numberList
# Is there a smarter way to handle exceptions if the file does not exist?
filename = input("Enter the file containing the list of numbers. ")
with open(filename) as file_object:
    numberList = file_object.readlines()


# Count increases with a window size of 1
print("Number of times the list increases with window size 1: " + str(count_increases(numberList,1)))
# Count increases with a window size of 2
print("Number of times the list increases with window size 2: " + str(count_increases(numberList,2)))
# Count increases with a window size of 3
print("Number of times the list increases with window size 3: " + str(count_increases(numberList,3)))
# Count increases with a window size of 4
print("Number of times the list increases with window size 4: " + str(count_increases(numberList,4)))
# How can I automate tests of differnet input files and differnet window sizes? -- just pytest!