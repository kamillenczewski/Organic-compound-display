from random import randint, choice
from constants import (
    METHYL_GROUPS, ELEMENT_GROUPS, NUMBERS_AND_NUMBER_PREFIXES, 
    ALKANE_PREFIXES, ALKANE_SUFFIXES
)

MAX_COAL_AMOUNT = 10
MAX_PREFIX_NUMBER = 5

def generate_coal_amount():
    return randint(1, MAX_COAL_AMOUNT)

def generate_methyl_group():
    return choice(METHYL_GROUPS[:4])

def generate_element_group():
    return choice(ELEMENT_GROUPS)

def generate_group():
    match(randint(0, 1)):
        case 0: return generate_methyl_group()
        case 1: return generate_element_group()

def generate_groups(amount):
    groups = []

    while len(groups) != amount:
        group = generate_group()

        if groups.count(group) < MAX_PREFIX_NUMBER:
            groups.append(group)

    return groups

DICT000 = None

def count_same_groups(groups):
    _dict = {}

    for group in groups:
        if group in _dict:
            _dict[group] += 1
        else:
            _dict[group] = 1

    global DICT000
    DICT000 = _dict

    return _dict

def link_groups_and_group_indices(groups, group_indices, group_amounts):
    _dict = {}

    group_indices_copy = group_indices.copy()

    for group, amount in zip(groups, group_amounts):
        _dict[group] = []

        for _ in range(amount):
            random_index = choice(group_indices_copy)
            group_indices_copy.remove(random_index)
            _dict[group].append(random_index)

    return _dict

def numbers_to_number_prefixes(numbers): 
    return [NUMBERS_AND_NUMBER_PREFIXES[number] for number in numbers]

# A chunk looks like: 1,2,3-trichloro
# indices + number prefix + group
def create_group_chunk(group, group_indices, number_prefix):
    indices_with_commas = ','.join(group_indices)
    return indices_with_commas + '-' + number_prefix + group

def create_group_chunks(groups_and_group_indices, number_prefixes):
    chunks = []

    for (group, group_indices), number_prefix in zip(groups_and_group_indices.items(), number_prefixes):
        # converting integers to strings
        group_indices = [str(index) for index in group_indices]

        chunk = create_group_chunk(group, group_indices, number_prefix)

        chunks.append(chunk)

    return chunks

def create_groups_string(groups_and_group_indices, number_prefixes):
    chunks = create_group_chunks(groups_and_group_indices, number_prefixes)
    stringified_chunks = '-'.join(chunks)

    return stringified_chunks

def bond_level_to_alkane_suffix(bond_level):
    return ALKANE_SUFFIXES[bond_level - 1]

class CompoundNameGenerator:
    # Only this function should be called outisde the class !!!
    def generate_compound_name(self):
        self.init()

        group_indices_amount = randint(0, self.coal_amount)

        compound_name = ''

        if group_indices_amount != 0:
            # pre generation --> init
            group_indices = self.generate_group_indices(group_indices_amount)

            groups = generate_groups(group_indices_amount)     

            counted_groups = count_same_groups(groups)   

            groups = list(counted_groups.keys())
            group_amounts = list(counted_groups.values())

            number_prefixes = numbers_to_number_prefixes(group_amounts)
            groups_and_group_indices = link_groups_and_group_indices(groups, group_indices, group_amounts)
            
            groups_string = create_groups_string(groups_and_group_indices, number_prefixes)
            
            compound_name += groups_string

        # pre generation --> init
        main_alkane_prefix = self.get_main_alkane_prefix()

        compound_name += main_alkane_prefix

        # pre generation --> init
        bond_level_and_bond_index = self.generate_bond_level_and_index()

        if bond_level_and_bond_index != None:
            bond_level, bond_index = bond_level_and_bond_index

            main_alkane_suffix = bond_level_to_alkane_suffix(bond_level)

            compound_name += f'-{bond_index}-' + main_alkane_suffix
        else:
            compound_name += 'an'

        # if randint(0, 1):
        #     OH_group_indices = self.generate_group_indices(2)
        #     OH_group_indices = [str(index) for index in OH_group_indices]
        #     string_indices = ','.join(OH_group_indices)

        #     compound_name += '-' + string_indices + '-' + 'diol'

        return compound_name

    def init(self):
        self.coal_amount = generate_coal_amount()

        self.FIRST_INDEX = 1
        self.LAST_INDEX = self.coal_amount

        self.EXTREME_COAL_MAX_FILL = 3
        self.MIDDLE_COAL_MAX_FILL = 2

        self.MAX_FILL_LEVEL = self.create_max_fill_level()

        self.fill_level = self.create_default_fill_level()

    def create_max_fill_level(self):
        level = {}

        for coal_index in range(1, self.coal_amount + 1):
            if coal_index == self.FIRST_INDEX or coal_index == self.LAST_INDEX:
                level[coal_index] = self.EXTREME_COAL_MAX_FILL
            else:
                level[coal_index] = self.MIDDLE_COAL_MAX_FILL

        return level

    def create_default_fill_level(self):
        return {coal_index: 0 for coal_index in range(1, self.coal_amount + 1)}

    def is_coal_full(self, coal_index):
        if coal_index == self.FIRST_INDEX or coal_index == self.LAST_INDEX:
            return self.fill_level[coal_index] == self.EXTREME_COAL_MAX_FILL
        else:
            return self.fill_level[coal_index] == self.MIDDLE_COAL_MAX_FILL

    def increase_fill_level(self, coal_index):
        if not self.is_coal_full(coal_index):
            self.fill_level[coal_index] += 1

    def get_possible_coal_indices_to_create_bond(self, bond_level):
        if bond_level not in [2, 3]:
            raise ValueError('You can create bond only with level 2 or 3!')

        needed_space = bond_level - 1

        inverted_fill_level = self.get_inverted_fill_level()

        indices = []

        for coal_index in list(inverted_fill_level.keys())[:-1]:
            current_amount = inverted_fill_level[coal_index]
            next_amount = inverted_fill_level[coal_index + 1]
        
            if current_amount - needed_space >= 0 and next_amount - needed_space >= 0:
                indices.append(coal_index)

        return indices

    def generate_bond_level_and_index(self):        
        bond_level = randint(2, 3)
        possible_indices = self.get_possible_coal_indices_to_create_bond(bond_level)

        if possible_indices:
            random_index = choice(possible_indices)
            self.increase_fill_level(random_index)
            return bond_level, random_index
        else:
            return None


    def get_possible_coal_indices(self):
        inverted_fill_level = self.get_inverted_fill_level()

        indices = []

        for coal_index, amount in inverted_fill_level.items():
            indices.extend(amount * [coal_index])

        return indices

    def get_inverted_fill_level(self):
        return {coal_index: max_amount - current_amount for coal_index, (max_amount, current_amount) in enumerate(list(zip(self.MAX_FILL_LEVEL.values(), self.fill_level.values())), start=1)}


    def generate_group_index(self, possible_coal_indices):
        index = choice(possible_coal_indices)
        self.increase_fill_level(index)
        return index

    def generate_group_indices(self, amount):
        possible_coal_indices = self.get_possible_coal_indices()
        return [self.generate_group_index(possible_coal_indices) for _ in range(amount)]

    def get_main_alkane_prefix(self):
        return ALKANE_PREFIXES[self.coal_amount - 1]



if __name__ == '__main__':
    generator = CompoundNameGenerator()

    for _ in range(100):
        print(generator.generate_compound_name())