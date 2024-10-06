"""
C CH CH2 CH3 
H Br Cl 
metylo etylo
ol al on 
horizontal_single_bond, horizontal_double_bond, horizontal_triple_bond
vertical_single_bond, vertical_double_bond
"""

from constants import *

METHYL_GROUPS = ['metylo', 'etylo', 'propylo', 'butylo', 'pentylo', 'heksylo', 'heptylo', 'oktylo', 'nonylo']
ELEMENT_GROUPS = ['bromo', 'chloro']

def methyl_group_to_coal_amount(methyl_group):
    return METHYL_GROUPS.index(methyl_group) + 1

class TagsMatrix:
    def __init__(self, height, length, default_item):
        self.height = height
        self.length = length
        self.default_item = default_item
        self.items = self.create_items()

    def create_items(self):
        return [self.create_row() for _ in range(self.height)]

    def create_row(self):
        return [self.default_item for _ in range(self.length)]

    def set(self, x, y, item):
        if 0 <= x < self.length and 0 <= y < self.height:
            self.items[y][x] = item

    def get(self, x, y):
        if 0 <= x < self.length and 0 <= y < self.height:
            return self.items[y][x]

    def add_right_column(self):
        for row in self.items:
            row.append(self.default_item)
        
        self.length += 1

    def add_left_column(self):
        for row in self.items:
            row.insert(0, self.default_item)

        self.length += 1

    def add_upper_row(self):
        self.items.append(self.create_row())
        self.height += 1

    def add_lower_row(self):
        self.items.insert(0, self.create_row())
        self.height += 1

    def print(self):
        for row in self.items:
            string = ''.join(row)
            print(string)

    def get_width(self):
        return self.length

    def get_height(self):
        return self.height

class MatrixIterator:
    def __init__(self, matrix: TagsMatrix, start_x=0, start_y=0) -> None:
        self.matrix = matrix

        self.current_x = start_x
        self.current_y = start_y

    def move_to_coordinates(self, x, y):
        # diff_x (+) -> right
        # diff_x (-) -> left
        # diff_y (+) -> up
        # diff_y (-) -> down

        diff_x = x - self.current_x
        diff_y = y - self.current_y

        if diff_x > 0:
            for _ in range(abs(diff_x)):
                self.move_right()            
        elif diff_x < 0:
            for _ in range(abs(diff_x)):
                self.move_left()           

        if diff_y > 0:
            for _ in range(abs(diff_y)):
                self.move_up()         
        elif diff_y < 0:
            for _ in range(abs(diff_y)):
                self.move_down()  

    def move_right(self):
        if self.current_x + 1 >= self.matrix.length:
            self.matrix.add_right_column()

        self.current_x += 1

    def move_left(self):
        if self.current_x - 1 < 0:
            self.matrix.add_left_column()
        else:
            self.current_x -= 1

    def move_up(self):
        if self.current_y + 1 >= self.matrix.height:
            self.matrix.add_upper_row()
        
        self.current_y += 1

    def move_down(self):
        if self.current_y - 1 < 0:
            self.matrix.add_lower_row()
        else:
            self.current_y -= 1

    def set(self, item):
        self.matrix.set(self.current_x, self.current_y, item)

    def get(self):
        return self.matrix.get(self.current_x, self.current_y)

# Class which produces object of Matrix with coal chain
class CoalChainBuilder1:
    # Hydrogen amount list should be checked if it is corrected
    # Before passing it into this method
    def __init__(self, hydrogen_amounts_list: list[int]) -> None:
        self.matrix = TagsMatrix(1, 1, WHITE_SQUARE)

        self.matrix_iterator = MatrixIterator(self.matrix, 0, 0)

        self.hydrogen_amounts_list = hydrogen_amounts_list
       
        self.coal_x_coordinates = []

    # It returns:
    #   - Matrix with coal chain
    #   - List with x coordinates which correspond to next coal elements
    #   - Value of y coordinate of location of coal chain
    def build(self):
        for index, hydrogen_amount in enumerate(self.hydrogen_amounts_list):
            match(hydrogen_amount):
                case 0: self.set(C)
                case 1: self.set(CH)
                case 2: self.set(CH2)
                case 3: self.set(CH3)
                case 4: self.set(CH4)

            self.coal_x_coordinates.append(self.matrix_iterator.current_x)

            # We don't want to have bond in the last coal so 
            # If we are not in the last index, execute ...
            if index != len(self.hydrogen_amounts_list) - 1:
                # Building bonds
                self.move_right()
                self.set(HORIZONTAL_SINGLE_BOND)
                self.move_right()

        return self.matrix, self.coal_x_coordinates, self.matrix_iterator.current_y         

    def move_right(self):
        self.matrix_iterator.move_right()

    def set(self, item):
        self.matrix_iterator.set(item)


# Class which produces object of Matrix with coal chain
class CoalChainBuilder:
    # Hydrogen amount list should be checked if it is corrected
    # Before passing it into this method
    def __init__(self, hydrogen_amounts_list: list[int]) -> None:
        self.matrix = TagsMatrix(1, 1, WHITE_SQUARE)

        self.matrix_iterator = MatrixIterator(self.matrix, 0, 0)

        self.hydrogen_amounts_list = hydrogen_amounts_list
       
        self.coal_x_coordinates = []

    # It returns:
    #   - Matrix with coal chain
    #   - List with x coordinates which correspond to next coal elements
    #   - Value of y coordinate of location of coal chain
    def build(self):
        for index, hydrogen_amount in enumerate(self.hydrogen_amounts_list):
            match(hydrogen_amount):
                case 0: self.set(C)
                case 1: self.set(CH)
                case 2: self.set(CH2)
                case 3: self.set(CH3)
                case 4: self.set(CH4)

            self.coal_x_coordinates.append(self.matrix_iterator.current_x)

            # We don't want to have bond in the last coal so 
            # If we are not in the last index, execute ...
            if index != len(self.hydrogen_amounts_list) - 1:
                # Building bonds
                self.move_right()
                self.set(HORIZONTAL_SINGLE_BOND)
                self.move_right()

        return self.matrix, self.coal_x_coordinates, self.matrix_iterator.current_y         

    def move_right(self):
        self.matrix_iterator.move_right()

    def set(self, item):
        self.matrix_iterator.set(item)

class CoalChainIterator:
    def __init__(self, matrix, coal_chain_x_coordinates, coal_y) -> None:
        self.matrix = matrix
        self.matrix_iterator = MatrixIterator(matrix, coal_chain_x_coordinates[0], coal_y)

        self.coal_chain_y = coal_y
        self.coal_chain_x_coordinates = coal_chain_x_coordinates

        self.current_coal_index = 0

    def reset(self):
        self.current_coal_index = 0
        self.move_to_current_coal()

    def move_to_next_coal(self):
        self.move_to_coal_index(self.current_coal_index + 1)

    def move_to_coal_index(self, index):
        if self.is_index_valid(index):
            self.current_coal_index = index
            self.move_to_current_coal()

    def is_index_valid(self, index):
        return 0 <= index < len(self.coal_chain_x_coordinates)   

    def move_to_current_coal(self):
        self.matrix_iterator.move_to_coordinates(self.current_coal_x(), self.current_coal_y())   

    def current_coal_x(self):
        return self.coal_chain_x_coordinates[self.current_coal_index]
    
    def current_coal_y(self):
        return self.coal_chain_y

    def current_x(self):
        return self.matrix_iterator.current_x

    def current_y(self):
        return self.matrix_iterator.current_y

    def set(self, item):
        self.matrix_iterator.set(item)

    def get(self):
        return self.matrix_iterator.get()

    def move_right(self):
        self.matrix_iterator.move_right()

    def move_left(self):
        if self.matrix_iterator.current_x - 1 < 0:
            # Increasing all x coordinates by 1
            for i in range(len(self.coal_chain_x_coordinates)):
                self.coal_chain_x_coordinates[i] += 1

        self.matrix_iterator.move_left()

    def move_up(self):
        self.matrix_iterator.move_up()

    def move_down(self):
        if self.matrix_iterator.current_y - 1 < 0:
            self.coal_chain_y += 1

        self.matrix_iterator.move_down()

class GroupsInserter:
    def __init__(self,
                coal_chain_iterator: CoalChainIterator, 
                coal_indexed_groups: list[list[str]], 
                coal_chain_x_coordinates: list[int],
                coal_chain_y) -> None:
        self.coal_chain_iterator = coal_chain_iterator
        self.coal_indexed_groups = coal_indexed_groups
        self.coal_chain_x_coordinates = coal_chain_x_coordinates
        self.coal_chain_y = coal_chain_y

    # metylo -> 1 etylo -> 2 propylo -> 3
    def insert_methyl_group_up(self, coal_amount):
        for _ in range(coal_amount - 1):
            self.insert_basic_group_up(CH2)

        self.go_up()
        self.set(VERTICAL_SINGLE_BOND)
        self.go_up()
        self.set(CH3)

    def insert_methyl_group_down(self, coal_amount):
        for _ in range(coal_amount - 1):
            self.insert_basic_group_down(CH2)

        self.go_down()
        self.set(VERTICAL_SINGLE_BOND)
        self.go_down()
        self.set(CH3)

    def insert_basic_group_up(self, group):
        self.go_up()
        self.set(VERTICAL_SINGLE_BOND)
        self.go_up()
        self.set(group)

    def insert_basic_group_down(self, group):
        self.go_down()
        self.set(VERTICAL_SINGLE_BOND)
        self.go_down()
        self.set(group)

    def insert_basic_group_left(self, group):
        self.go_left()
        self.set(HORIZONTAL_SINGLE_BOND)
        self.go_left()
        self.set(group)

    def insert_basic_group_right(self, group):
        self.go_right()
        self.set(HORIZONTAL_SINGLE_BOND)
        self.go_right()
        self.set(group)

    def insert_basic_group(self, group, direction):
        match(direction):
            case 'up': self.insert_basic_group_up(group)
            case 'down': self.insert_basic_group_down(group)
            case 'left': self.insert_basic_group_left(group)
            case 'right': self.insert_basic_group_right(group)
            case _: raise ValueError(f'Direction: {direction} is incorrect!')

    def insert_methyl_group(self, coal_amount, direction):
        match(direction):
            case 'up': self.insert_methyl_group_up(coal_amount)
            case 'down': self.insert_methyl_group_down(coal_amount)
            case _: raise ValueError(f'Direction: {direction} is incorrect!')

    def execute(self):
        self.reset()

        coal_indexed_methyl_groups, coal_indexed_basic_groups = self.split_to_methyl_and_basic_groups()

        for index, methyl_groups_and_basic_groups in enumerate(zip(coal_indexed_methyl_groups, coal_indexed_basic_groups)):
            methyl_groups = methyl_groups_and_basic_groups[0]
            basic_groups = methyl_groups_and_basic_groups[1]

            # Setting possible directions
            # We know that first and last coal can hold 3 groups
            # But every coal in the middle can hold only 2 groups
            # -------------------------------------------------------#
            possible_directions = ['up', 'down']

            if index == 0:
                possible_directions.append('left')
            elif index == len(self.coal_indexed_groups) - 1:
                possible_directions.append('right')
            # -------------------------------------------------------#

            for group in basic_groups:
                # We assume that amount of groups was checked before
                # So do not have to care about an error here
                direction = possible_directions.pop(0)

                # provisional converting group name to symbol (tag)
                match(group):
                    case 'chloro': group = CL
                    case 'bromo': group = BR

                self.insert_basic_group(group, direction)

                self.move_to_current_coal()

            # We don't want to insert methyl groups in first or last coal
            # because it would make it different compound
            # For example if I got '1-metylopropan' it is obviously incorrect
            # Because we would say that it is 'butan' 
            if 0 < index < len(self.coal_indexed_groups) - 1:
                for group in methyl_groups:
                    # We assume that amount of groups was checked before
                    # So do not have to care about an error here
                    direction = possible_directions.pop(0)

                    coal_amount = methyl_group_to_coal_amount(group)

                    self.insert_methyl_group(coal_amount, direction)

                    self.move_to_current_coal()
                
            self.next_coal()

    def split_to_methyl_and_basic_groups(self):
        coal_indexed_methyl_groups = [[] for _ in range(len(self.coal_indexed_groups))]
        coal_indexed_basic_groups = [[] for _ in range(len(self.coal_indexed_groups))]

        for index, groups in enumerate(self.coal_indexed_groups):
            for group in groups:
                if group in METHYL_GROUPS:
                    coal_indexed_methyl_groups[index].append(group)
                elif group in ELEMENT_GROUPS:
                    coal_indexed_basic_groups[index].append(group)
                else:
                    raise ValueError(f'Group named {group} is incorrect!')
                
        return coal_indexed_methyl_groups, coal_indexed_basic_groups

    def move_to_current_coal(self):
        self.coal_chain_iterator.move_to_current_coal()

    def next_coal(self):
        self.coal_chain_iterator.move_to_next_coal()

    def go_up(self):
        self.coal_chain_iterator.move_up()

    def go_down(self):
        self.coal_chain_iterator.move_down()

    def go_right(self):
        self.coal_chain_iterator.move_right()

    def go_left(self):
        self.coal_chain_iterator.move_left()

    def set(self, item):
        self.coal_chain_iterator.set(item)

    def reset(self):
        self.coal_chain_iterator.reset()