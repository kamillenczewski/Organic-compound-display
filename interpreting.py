from matrix_utils import CoalChainBuilder, GroupsInserter, CoalChainIterator
from constants import ALKANE_PREFIXES, DASH, METHYL_GROUPS, ELEMENT_GROUPS, NUMBER_PREFIXES, NUMBERS_AND_NUMBER_PREFIXES

def split_by_dash(name):
    return name.split(DASH)

# It returns index of string with alkane prefix, this prefix
# And boolean value saying if suffix exists in this string
def find_string_with_alkane_prefix_in_the_end(strings: list[str]):
    for index, string in enumerate(strings):
        for prefix in ALKANE_PREFIXES:
            if string.endswith(prefix):
                return index, prefix, len(string) != len(prefix)
            
    return -1, None

def remove_number_prefixes(strings: list[str]):
    for index, string in enumerate(strings):
        for prefix in NUMBER_PREFIXES:
            if string.startswith(prefix):
                strings[index] = string.removeprefix(prefix)
                break

def disjoin_methyl_group_and_alkane(strings: list[str], alkane_index, alkane_prefix):
    methyl_group = strings[alkane_index].removesuffix(alkane_prefix)
    strings[alkane_index] = methyl_group
    strings.insert(alkane_index + 1, alkane_prefix)

def alkane_prefix_to_coal_amount(prefix):
    return ALKANE_PREFIXES.index(prefix) + 1

def strings_coal_indices_to_lists_of_ints(strings: list[str]):
    for i, string in enumerate(strings):
        # Split string, containing indices, by ',' to chars
        chars = string.split(',')

        # Convert to list of integers
        for j, char in enumerate(chars):
            if char.isdigit():
                chars[j] = int(char)
            else:
                raise ValueError(f"Character '{char}' can't be converted to integer!")
            
        strings[i] = chars

def get_coal_indexed_groups(coal_indices: list[list[int]], methyl_groups: list[str], coal_amount):
    coal_indexed_groups = [[] for _ in range(coal_amount)]
    
    for indices, group in zip(coal_indices, methyl_groups):
        for index in indices:
            # Coal indices can be integers between 1 and (coal_number)
            # But we want to convert it to programming standard indexing
            # So we make decrease by 1 to make first index be 0
            index -= 1

            if not 0 <= index < coal_amount:
                raise ValueError(f'Index of group should be in interval: [0,{coal_amount})')

            coal_indexed_groups[index].append(group)

    return coal_indexed_groups

def validate_amount_of_groups_in_each_coal(coal_indexed_methyl_groups, coal_amount):
    # According to the appearance of organic compounds
    # Coal elements in the middle of chain can hold 2 other groups
    # But coal elements in the left or right side can hold 3 groups
    #      H    H    H
    #      |    |    |
    # H -- C -- C -- C -- H
    #      |    |    | 
    #      H    H    H  

    if coal_amount == 0:
        raise ValueError('Compound have to have at least one coal!')

    # Compound which has 1 coal is a specific one
    # It can hold as many as 4 other groups
    #      H
    #      |
    # H -- C -- H
    #      |
    #      H 
    if coal_amount == 1:
        if len(coal_indexed_methyl_groups[0]) > 4:
            raise ValueError('Coal in this type of compound can hold maximally 4 groups!')

    if coal_amount == 2:
        if len(coal_indexed_methyl_groups[0]) > 3 or len(coal_indexed_methyl_groups[1]) > 3:
            raise ValueError('Coal elements in this type of compound can hold maximally 3 groups!')

    if coal_amount >= 3:
        if len(coal_indexed_methyl_groups[0]) > 3:
            raise ValueError('Left coal can hold maximally 3 groups!')

        if len(coal_indexed_methyl_groups[-1]) > 3:
            raise ValueError('Right coal can hold maximally 3 groups!')
        
        for i in range(1, coal_amount - 1):
            if len(coal_indexed_methyl_groups[i]) > 2:
                raise ValueError('Coal elements in the middle can hold maximally 2 groups!')

def is_alphabetically_ordered(methyl_groups):
    for i in range(len(methyl_groups) - 1):
        if methyl_groups[i] > methyl_groups[i + 1]:
            return False

    return True

def sort_alphabetically(coal_indices, methyl_groups):
    # We want to sort two lists ('methyl_groups', 'coal_indices') simultaneously
    # So we create a list of indices which will going to be sorted with 
    # alphabetical order of words of 'methyl_groups'

    indices = list(range(len(methyl_groups)))

    indices = sorted(indices, key=lambda index: methyl_groups[index])

    new_coal_indices = [None] * len(methyl_groups)
    new_methyl_groups = [None] * len(methyl_groups)

    for i, index in enumerate(indices):
        new_coal_indices[i] = coal_indices[index]
        new_methyl_groups[i] = methyl_groups[index]

    return new_coal_indices, new_methyl_groups

def disjoin_alkane_with_an_suffix(strings: list[str]):
    for i, string in enumerate(strings):
        if string.endswith('an'):
            strings[i] = string.removesuffix('an')
            strings.insert(i + 1, '1')
            strings.insert(i + 2, 'an')
            break

def get_hydrogen_amount_list(coal_indexed_groups: list[list[str]], coal_amount):
    # Creating default list of hydrogens
    if coal_amount == 1:
        hydrogens = [4]
    else:
        hydrogens = [2 for _ in range(coal_amount)]
        hydrogens[0] = 3
        hydrogens[-1] = 3

    for i, groups in enumerate(coal_indexed_groups):
        hydrogens[i] -= len(groups)

    return hydrogens

def validate_groups(groups: list[str]):
    for group in groups:
        if group not in METHYL_GROUPS and group not in ELEMENT_GROUPS:
            raise ValueError(f'Group with name: {group} is incorrect!')

def ensure_alphabetical_order(coal_indices, groups):
    coal_indices_and_groups = (len(coal_indices) + len(groups)) * [0]

    # It checks if alphabetical order of groups is satisfied
    # and, if not ,it shows message with corrected version.
    if not is_alphabetically_ordered(groups):
        coal_indices, groups = sort_alphabetically(coal_indices, groups)

        # We totally don't care what this variable meant before
        # I wanted to just use it because I has proper name
        coal_indices_and_groups[::2] = coal_indices
        coal_indices_and_groups[1::2] = groups

        # Adding number prefix before every group which has more than 1 occuring
        for i in range(1, len(coal_indices_and_groups), 2):
            indices_string_length = len(coal_indices_and_groups[i - 1])

            if indices_string_length == 1:
                continue

            # Assuming we handle only digits as indices we pick up relationship
            # between length of string indices that (length + 1) / 2 = number prefix (di, tri...)
            # For instance, we have: '1,1,3' so the length of this is 5 and if we add 1 
            # and divide by 2 we get (5 + 1) / 2 = 6 / 2 = 3 which is number of indices in this string
            indices_amount = (indices_string_length + 1) // 2

            number_prefix = NUMBERS_AND_NUMBER_PREFIXES[indices_amount]

            coal_indices_and_groups[i] = number_prefix + coal_indices_and_groups[i]

        corrected_compound_name = '-'.join(coal_indices_and_groups) + '-'.join(strings[index:])

        print(f"\n You meant: {corrected_compound_name} \n")

def try_find_string_with_an_suffix(strings):
    for index, string in enumerate(strings):
        if string.endswith('an'):
            strings[index] = string.removesuffix('an')
            strings.insert(index + 1, 'an')
            return index, string

def find_string_ending_with_alkane_prefix(strings):
    for string in strings:
        for alkane_prefix in ALKANE_PREFIXES:
            index = string.endswith(alkane_prefix)

            if index == -1:
                continue

            last_methyl_group = string[:index]
            main_alkane_index = index
            main_alkane_prefix = alkane_prefix

            return last_methyl_group, main_alkane_index, main_alkane_prefix

def interpret_compound_name(name: str):
    name = name.replace(' ', '')

    strings = split_by_dash(name)

    remove_number_prefixes(strings)

    main_alkane_index = -1
    main_alkane_prefix = None
    last_methyl_group = None

    main_alkane = try_find_string_with_an_suffix(strings)

    if main_alkane != None:
        strings[index] = string.removesuffix('an')
        strings.insert(index + 1, 'an')

    for index, string in enumerate(strings):
        if string.endswith('an'):
            strings[index] = string.removesuffix('an')
            strings.insert(index + 1, 'an')

    find_string_ending_with_alkane_prefix(strings)

    if main_alkane_index == -1:
        raise ValueError('There is no string which has an alkane prefix in the end!')




    # Remove one string contaning:
    # - methyl group
    # - main_alkane_prefix
    strings.pop(main_alkane_index)

    # Inserting strings which were removed
    # but as separate objects.
    strings.insert(main_alkane_index, main_alkane_prefix)
    strings.insert(main_alkane_index, last_methyl_group)

    # Increment main alkane indexby 1 because 
    # in this position last methyl group appeared.
    main_alkane_index += 1



    coal_amount = alkane_prefix_to_coal_amount(alkane_prefix)

    coal_indices_and_groups = strings[:main_alkane_index]
    coal_indices = coal_indices_and_groups[::2]
    groups = coal_indices_and_groups[1::2] 

    if len(coal_indices) != len(groups):
        raise ValueError("Size of 'coal_indices' and 'methyl_groups' should be the same!")

    validate_groups(groups)

    # ensure_alphabetical_order(coal_indices, groups)

    # Changing indices which are strings to lists of integers
    strings_coal_indices_to_lists_of_ints(coal_indices)

    coal_indexed_groups = get_coal_indexed_groups(coal_indices, groups, coal_amount) 

    validate_amount_of_groups_in_each_coal(coal_indexed_groups, coal_amount)
    
    hydrogen_amount_list =  get_hydrogen_amount_list(coal_indexed_groups, coal_amount)

    #  CoalChainBuilder, GroupsInserter

    matrix, coal_chain_x_coordinates, coal_chain_y_coordinate  = CoalChainBuilder(hydrogen_amount_list).build()
    coal_chain_iterator = CoalChainIterator(matrix, coal_chain_x_coordinates, coal_chain_y_coordinate)

    GroupsInserter(coal_chain_iterator, coal_indexed_groups, coal_chain_x_coordinates, coal_chain_y_coordinate).execute()

    return matrix

def main():
    name = """1,2,3-tribromo-1,4-dichloro-2,3-metyloheksan"""
    matrix = interpret_compound_name(name)
    matrix.print()

if __name__ == '__main__':
    main()