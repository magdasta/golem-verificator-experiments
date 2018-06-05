# Usage: python add_random_objects.py path_to_source_images output_path number_of_objects

from PIL.ImageDraw import Draw
import random
from sys import argv

import helpers


class Shape:
    def __init__(self, kind, color, bounding_box=None, start_angle=None, end_angle=None, vertices=None):
        self.kind = kind
        self.color = color
        self.bounding_box = bounding_box
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.vertices = vertices

    def scale_float_coords_to_image_size(coords, image_to_draw_on):
        width, height = image_to_draw_on.size
        scaled = []
        for i in range(len(coords)):
            if i % 2 == 0:
                scaled.append(coords[i] * width)
            else:
                scaled.append(coords[i] * height)
        return scaled

    def draw(self, image_to_draw_on):
        drawing_context = Draw(image_to_draw_on)
        if self.bounding_box:
            coords = Shape.scale_float_coords_to_image_size(self.bounding_box, image_to_draw_on)
        else:
            coords = Shape.scale_float_coords_to_image_size(self.vertices, image_to_draw_on)

        if self.kind == "chord":
            drawing_context.chord(coords, self.start_angle, self.end_angle, fill=self.color)
        elif self.kind == "ellipse":
            drawing_context.ellipse(coords, fill=self.color)
        elif self.kind == "pieslice":
            drawing_context.pieslice(coords, self.start_angle, self.end_angle, fill=self.color)
        elif self.kind == "polygon":
            drawing_context.polygon(coords, fill=self.color)
        else:
            raise Exception("unsupported kind")


def get_random_color():
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)
    return r, g, b


def get_random_bounding_box():
    x1 = random.random()
    y1 = random.random()
    dx = (random.random() - 0.5) / 7
    dy = (random.random() - 0.5) / 7
    return x1, y1, x1 + dx, y1 + dy


def get_random_polygon_vertices():
    vertices = [random.random(), random.random()]
    number_of_vertices = random.randrange(4, 15)
    for i in range(2, number_of_vertices * 2):
        d_coord = (random.random() - 0.5) / 20
        coord = vertices[i - 2] + d_coord
        vertices.append(coord)
    return vertices


def get_random_angle():
    return random.randrange(360)


def needs_angles(kind):
    if kind == "chord" or kind == "pieslice":
        return True
    return False


def prepare_objects_data(number_of_shapes_to_add):
    shapes = []
    while number_of_shapes_to_add > 0:
        bounding_box = None
        start_angle = None
        end_angle = None
        vertices = None
        number_of_shapes_to_add -= 1
        kind = random.choice(["chord", "ellipse", "pieslice", "polygon"])
        color = get_random_color()
        if kind in ["chord", "pieslice"]:
            start_angle = get_random_angle()
            end_angle = get_random_angle()

        if kind == "polygon":
            vertices = get_random_polygon_vertices()
        else:
            bounding_box = get_random_bounding_box()

        shapes.append(Shape(kind, color, bounding_box, start_angle, end_angle, vertices))
    return shapes


def draw_objects(image, parameters):
    for shape in parameters.shapes_to_add:
        shape.draw(image)
    return image


def run():
    number_of_objects_string = argv[3]
    parameters = []
    parameters_set = helpers.Parameters()
    parameters_set.file_postfix = "_[randomObjects]_[numberOfObjects=" + number_of_objects_string + "]"
    parameters_set.shapes_to_add = prepare_objects_data(int(number_of_objects_string))

    parameters.append(parameters_set)

    helpers.simple_process_directory(argv[1], argv[2], draw_objects, parameters)


if __name__ == "__main__":
    run()
