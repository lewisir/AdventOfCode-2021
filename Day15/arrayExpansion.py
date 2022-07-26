from typing import List

class ArrayExpansion():
    """
    A class to duplicate and expand a 2D array of integers
    """

    def __init__(self,input_array:List[List[int]]) -> None:
        self.input_array = input_array

    @property
    def y_array_size(self):
        return len(self.input_array)

    @property
    def x_array_size(self):
        return len(self.input_array[0])

    def expand_array(self,y_multiple:int,x_multiple:int,modulation:int=1) -> List[List[int]]:
        """
        Take the input_array and duplciate it y_multiple times in the y direction
        and x_multiple times in the x direction.
        The modulation value controls how integers are increased each time the
        input_array is duplciated, and defaults to 1.

        if the input_array is:
            1 2 3
            4 5 6
            7 8 9

        and the expand_array is called with expand_array(2, 3, 1) the new array is:
            1 2 3  2 3 4 3 4 5
            4 5 6  5 6 7 6 7 8
            7 8 9  8 9 1 9 1 2

            2 3 4  3 4 5 4 5 6
            5 6 7  6 7 8 7 8 9
            8 9 1  9 1 2 1 2 3
        (spaces added to show the original array in the top left corner)
        """
        # Initialise the new 2D array
        output_array = [[0 for x in range(self.x_array_size*x_multiple)] for y in range(self.y_array_size*y_multiple)]
        # Update the array elements
        for y_pos, y_val in enumerate(output_array):
            for x_pos, x_val in enumerate(y_val):
                y_dup = y_pos // self.y_array_size
                x_dup = x_pos // self.x_array_size
                factor = y_dup + x_dup
                new_value = self.input_array[y_pos % self.y_array_size][x_pos % self.x_array_size] + modulation*factor
                if new_value > 9:
                    new_value -= 9
                output_array[y_pos][x_pos] = new_value
        return output_array
