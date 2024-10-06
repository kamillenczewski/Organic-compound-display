from tkinter import Label
from typing import Callable
from tkinter import Tk

from constants import tag_to_image, WHITE_SQUARE
from matrix_utils import TagsMatrix

def create_array(width, height, default_item_generator: Callable[[], object]) -> list[list[object]]:
    return [[default_item_generator() for _ in range(width)] for _ in range(height)]

def transpose(array: list[list[object]], width, height, default_item_generator: Callable[[], object]) -> list[list[object]]:
    new_matrix = create_array(height, width, default_item_generator)

    for y in range(width):
        for x in range(height):
            new_matrix[y][x] = array[x][y]

    return new_matrix

class LabelsMatrix:
    def __init__(self, master, width, height) -> None:
        self.master = master

        self.width = width
        self.height = height

        self.labels = self.create_default_labels()

    def create_default_labels(self) -> list[list[Label]]:
        return create_array(self.width, self.height, lambda: Label(master=self.master, image=tag_to_image(WHITE_SQUARE)))

    def set_image(self, x, y, image):
        self.labels[y][x].config(image=image)

    def __getitem__(self, y) -> list[Label]:
        return self.labels[y]

class LabelsMatrixBuilder:
    def __init__(self, master, tags_matrix: TagsMatrix) -> None:
        self.master = master

        self.tags_matrix = tags_matrix

        self.width = tags_matrix.get_width()
        self.height = tags_matrix.get_height()

        self.labels_matrix = LabelsMatrix(self.master, self.width, self.height)

    def grid_labels(self):
        for x in range(self.width):
            for y in range(self.height):
                self.labels_matrix[y][x].grid(column=y, row=x)
    
    def inject_tags_matrix(self):
        for x in range(self.height):
            for y in range(self.width):
                tag = self.tags_matrix.get(x, y)
                image = tag_to_image(tag)
                self.labels_matrix.set_image(y, x, image)

    def generate_default_label(self):
        return Label(master=self.master, image=tag_to_image(WHITE_SQUARE))

    def build(self):
        self.labels_matrix.labels = transpose(self.labels_matrix.labels, self.width, self.height, self.generate_default_label)
        self.width, self.height = self.height, self.width
        self.grid_labels()
        self.inject_tags_matrix()

        return self.labels_matrix