"""
Day 18 - Snailfish

What sort of new Hell is this?

A Snailfish Number (SN) is a pair [x,y]
x and y can be regular integers or can in fact themselves be pairs of numbers

To add two SNs together form a new pair;
  [1,2] + [[3,4],5]  =  [[1,2],[[3,4],5]]

SNs are then reduced by:
- If any pair is nested inside four pairs, the leftmost pair explodes
- If any regular number is 10 or greater, the leftmost number splits

Repeat the above operations until no pairs are nested four deep and no numbers are greater than 9
Always check the number for explosions before checking for splitting

To explode a pair:
The pair's left value is added to the first number to the left of the exploding pair (if any),
and the pair's right value is added to the first number to the right of the exploding pair (if any).
Exploding pairs will always consist of two regular numbers.
Then, the entire exploding pair is replaced with the regular number 0
For example:
[[[[[9,8],1],2],3],4] - here [9,8] is nested inside four pairs
[[[[[9,8],9],2],3],4] - nothing to the left of 9, there is 1 to the right of 8 which makes a 9
[[[[0,9],2],3],4]  - the original [9,8] pair is then replaced with '0'

To split a regular number:
Replace it with a pair; the left element is the number divided by two and rounded down,
while the right element is regular number divided by two and rounded up.
For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on
"""


from cgi import test


class NumberPair:
    """A class to model a pair of elements"""

    MAX_DEPTH = 4
    MAX_VALUE = 9
    EXPLODED = "X"

    def __init__(self, x_value=None, y_value=None):
        self.length = 1
        self.pair_list = [x_value, y_value]
        self.depth = 0
        self.magnitude = 0
        self.display_string = ""

    @property
    def x_value(self):
        """return the real time x value"""
        return self.pair_list[0]

    @property
    def y_value(self):
        """return the real time y value"""
        return self.pair_list[1]

    def build_number(self, pair_string, pointer=1, depth=1):
        """ "build the number from a string"""
        self.depth = depth
        index = 0
        while pointer < len(pair_string):
            char = pair_string[pointer]
            # self.debug_ouput(pair_string, pointer, self.depth)
            if char == "[":
                self.pair_list[index] = NumberPair()
                self.pair_list[index].build_number(
                    pair_string, pointer + 1, self.depth + 1
                )
                pointer += self.pair_list[index].length
                self.length += self.pair_list[index].length
            elif char == "]":
                index = 0
                pointer += 1
                self.length += 1
                break
            elif char == ",":
                index = 1
                pointer += 1
                self.length += 1
            elif char.isnumeric():
                result = self.get_number(pair_string, pointer)
                self.pair_list[index] = result[0]
                pointer = result[1]
                self.length += len(str(self.pair_list[index]))
            else:
                print("Unrecognised content in pair string")
                break

    def get_number(self, pair_string, pointer):
        """extract an integer from a string"""
        number = ""
        while pair_string[pointer].isnumeric():
            number += pair_string[pointer]
            pointer += 1
        return [int(number), pointer]

    def evaluate_magnitude(self):
        """
        The magnitude of a pair is 3 x its X element plus 2 x its y element.
        The magnitude of a regular number is just that number and is recursive (lower numbers first)
        [[1,2],[[3,4],5]] ->
        [[1,2],[[3*3 + 2*4],5]] ->
        [[1,2],[17,5]] ->
        [[3*1 + 2*2],[3*17 + 2*5]] ->
        [7,61] ->
        3*7 + 2*61 = 143
        """
        if isinstance(self.x_value, NumberPair):
            self.x_value.evaluate_magnitude()
            mag_x = self.x_value.magnitude
        else:
            mag_x = self.x_value
        if isinstance(self.y_value, NumberPair):
            self.y_value.evaluate_magnitude()
            mag_y = self.y_value.magnitude
        else:
            mag_y = self.y_value
        self.magnitude = 3 * mag_x + 2 * mag_y

    def build_display_string(self):
        """build a string to display the number"""
        self.display_string = ""
        for index, value in enumerate(self.pair_list):
            if index == 0 and isinstance(value, NumberPair):
                value.build_display_string()
                self.display_string += "[" + value.display_string
            elif index == 1 and isinstance(value, NumberPair):
                value.build_display_string()
                self.display_string += "," + value.display_string + "]"
            elif index == 0:
                self.display_string += "[" + str(value)
            else:
                self.display_string += "," + str(value) + "]"

    def reduce(self):
        """
        Run the process to reduce the number
        First explode until you can explode no more
        Then split, if you split anything go back and explode
        If you can't split anything then the number is reduced
        """
        reducing = True
        while reducing:
            self.explode()
            reducing = self.split()

    def explode(self):
        """Run through the number exploding everything"""
        exploding = True
        while exploding:
            add_x, add_y = self.find_explode()
            if isinstance(add_x, int):
                self.increment(add_y, False, True)
                add_y = None
                self.increment(add_x, False, False)
                add_x = None
                self.reset_exploded_pair()
            elif add_x == None:
                exploding = False

    def find_explode(self):
        add_x, add_y = None, None
        for index, value in enumerate(self.pair_list):
            if isinstance(value, NumberPair) and self.depth == self.MAX_DEPTH:
                add_x = value.x_value
                add_y = value.y_value
                self.pair_list[index] = self.EXPLODED
                return [add_x, add_y]
            elif isinstance(value, NumberPair):
                add_x, add_y = value.find_explode()
                if isinstance(add_x, int):
                    return [add_x, add_y]
        return [add_x, add_y]

    def increment(self, increment, increment_next=False, direction=True):
        if direction == False:
            self.pair_list.reverse()
        for index, value in enumerate(self.pair_list):
            if increment_next and isinstance(value, int):
                self.pair_list[index] += increment
                increment_next = False
            elif value == self.EXPLODED:
                increment_next = True
            elif isinstance(value, NumberPair):
                increment_next = value.increment(increment, increment_next, direction)
        if direction == False:
            self.pair_list.reverse()
        return increment_next

    def reset_exploded_pair(self):
        """Work through the number and change 'X' to 0"""
        for index, value in enumerate(self.pair_list):
            if value == self.EXPLODED:
                self.pair_list[index] = 0
            elif isinstance(value, NumberPair):
                value.reset_exploded_pair()

    def split(self, splitting=False):
        """split a number in to a new pair"""
        for index, value in enumerate(self.pair_list):
            if isinstance(value, int) and value > self.MAX_VALUE:
                self.pair_list[index] = NumberPair(
                    self.round_number(value, 2, "down"),
                    self.round_number(value, 2, "up"),
                )
                self.pair_list[index].depth = self.depth + 1
                splitting = True
                return splitting
            elif isinstance(value, NumberPair):
                splitting = value.split(splitting)
                if splitting:
                    return splitting
        return splitting

    def debug_ouput(self, pair_string, pointer, depth):
        """outputs information on string processing"""
        print(f"{pair_string}\n" + " " * pointer + "^")
        print(
            "- " * depth
            + f"Pointer is {pointer} length is {self.length} and pair is {self.pair_list}\n"
        )

    def round_number(self, number, divisor, round_control="up"):
        """function to round a number up or down"""
        remainder = number % divisor
        if remainder == 0 or round_control == "down":
            return number // divisor
        else:
            return (number // divisor) + 1


def main():
    """the main program"""

    file_data = []
    with open("Day18/inputDay18.txt", "r", encoding="utf-8") as file:
        for line in file:
            file_data.append(line.rstrip("\n"))

    sum_number = NumberPair()
    for index, value in enumerate(file_data):
        current_number = NumberPair()
        current_number.build_number(value)
        current_number.reduce()
        current_number.build_display_string()
        if index == 0:
            sum_number.build_number(value)
            sum_number.reduce()
            sum_number.build_display_string()
        else:
            sum_number.build_number(
                "["
                + sum_number.display_string
                + ","
                + current_number.display_string
                + "]"
            )
            sum_number.reduce()
            sum_number.build_display_string()

    sum_number.evaluate_magnitude()
    print(f"Part I answer {sum_number.magnitude}")

    max_magnitude = 0
    sum_number = NumberPair()
    for index1, value1 in enumerate(file_data):
        for index2, value2 in enumerate(file_data):
            if index1 != index2:
                sum_number.build_number("[" + value1 + "," + value2 + "]")
                sum_number.reduce()
                sum_number.evaluate_magnitude()
                magnitude = sum_number.magnitude
                if magnitude > max_magnitude:
                    max_magnitude = magnitude
    print(f"Part II answer {max_magnitude}")


if __name__ == "__main__":
    main()
