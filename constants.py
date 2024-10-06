from tkinter import PhotoImage, Tk
from os.path import join as combine_path
from pathlib import Path

# !!! TEMPORARY !!!
# I need to understand how to remove it from here.
a = Tk()

#-------------------------------------------------#
# Constants here are tags which can be named like
# you want because they are only needed for
# flaging data and code dubuging.

C = 'C'
CH = 'CH'
CH2 = 'CH2'
CH3 = 'CH3'
CH4 = 'CH4'

CL = 'Cl' # chlor
BR = 'Br' # brom

HORIZONTAL_SINGLE_BOND = '-'
HORIZONTAL_DOUBLE_BOND = '--'
HORIZONTAL_TRIPLE_BOND = '--'

VERTICAL_SINGLE_BOND = 'I'
VERTICAL_DOUBLE_BOND = 'II'

WHITE_SQUARE = ' '

#-------------------------------------------------#

IMAGES_PATH = combine_path(Path(__file__).parent.resolve(), 'images')


# every image should be contained in images directory
# so only image_name is needed
def get_image(image_name):
    return PhotoImage(file=combine_path(IMAGES_PATH, image_name))


C_IMAGE = get_image('C.png')
CH_IMAGE = get_image('CH.png')
CH2_IMAGE = get_image('CH2.png')
CH3_IMAGE = get_image('CH3.png')
CH4_IMAGE = get_image('CH4.png')

BR_IMAGE = get_image('Br.png')
CL_IMAGE = get_image('Cl.png')

HORIZONTAL_SINGLE_BOND_IMAGE = get_image('horizontal_single_bond.png')
HORIZONTAL_DOUBLE_BOND_IMAGE = get_image('horizontal_double_bond.png')
HORIZONTAL_TRIPLE_BOND_IMAGE = get_image('horizontal_triple_bond.png')

VERTICAL_SINGLE_BOND_IMAGE = get_image('vertical_single_bond.png')
VERTICAL_DOUBLE_BOND_IMAGE = get_image('vertical_double_bond.png')

WHITE_SQUARE_IMAGE = get_image('white_square.png')

IMAGES = {
    C: C_IMAGE,
    CH: CH_IMAGE,
    CH2: CH2_IMAGE,
    CH3: CH3_IMAGE,
    CH4: CH4_IMAGE,

    BR: BR_IMAGE,
    CL: CL_IMAGE,

    HORIZONTAL_SINGLE_BOND: HORIZONTAL_SINGLE_BOND_IMAGE,
    HORIZONTAL_DOUBLE_BOND: HORIZONTAL_DOUBLE_BOND_IMAGE,
    HORIZONTAL_TRIPLE_BOND: HORIZONTAL_TRIPLE_BOND_IMAGE,

    VERTICAL_SINGLE_BOND: VERTICAL_SINGLE_BOND_IMAGE,
    VERTICAL_DOUBLE_BOND: VERTICAL_DOUBLE_BOND_IMAGE,

    WHITE_SQUARE: WHITE_SQUARE_IMAGE
}

def tag_to_image(tag):
    return IMAGES[tag]


ALKANE_PREFIXES = ['met', 'et', 'prop', 'but', 'pent', 'heks', 'hept', 'okt', 'non', 'dek']
ALKANE_SUFFIXES = ['an', 'en', 'yn']

DASH = '-'

METHYL_GROUPS = ['metylo', 'etylo', 'propylo', 'butylo', 'pentylo', 'heksylo', 'heptylo', 'oktylo', 'nonylo']
ELEMENT_GROUPS = ['bromo', 'chloro']

NUMBER_PREFIXES = ['di', 'tri', 'tetra', 'penta']
NUMBERS_AND_NUMBER_PREFIXES = {1: '', 2: 'di', 3: 'tri', 4: 'tetra', 5: 'penta'}