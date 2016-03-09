import datetime
import math
import os
import random

import utils
from point import Point

module_logger = utils.get_logger(__name__)

POSSIBLE_MUTATIONS = range(9)
MOVE_POINT, CHANGE_COLOR, CHANGE_OPACITY, MOVE, SCALE, ROTATE, CHANGE_LEVEL, REMOVE_TRIANGLE, ADD_TRIANGLE = POSSIBLE_MUTATIONS
TWO_PI = math.pi * 2
MINIMUM_NUM_TRIANGLES = 10


#######################################################################
def clamp(low, num, high):
    return max(low, min(num, high))


#######################################################################
class Evolver(object):
    ###################################################################
    def __init__(self, source_image, output_folder, num_triangles, save_frequency, color_type, save_index=0, auto_save_frequency=None):
        self.source_image = source_image
        self.best = None
        self.output_folder = output_folder
        self.size = Point(self.source_image.size[0], self.source_image.size[1])
        self.num_triangles = num_triangles
        self.save_frequency = save_frequency
        self.auto_save_frequency = auto_save_frequency or datetime.timedelta(seconds=10)  # save every 5 seconds
        self.last_saved_time = datetime.datetime(1970, 1, 1)
        self.last_auto_saved_time = self.last_saved_time
        self.save_index = save_index
        self.previous_fitness = 0
        self.initial_fitness = 0
        self.color_type = color_type
        self.generation_count = 0
        self.min_fitness = self.size.x * self.size.y * 128
        if self.color_type == utils.RGB:
            self.min_fitness *= 3

    ###################################################################
    def checkpoint(self):
        if (datetime.datetime.now() - self.last_saved_time) >= self.save_frequency:
            self.best.save_file(os.path.join(self.output_folder, "intermediate_%03d.txt" % self.save_index))
            self.best.save_image(os.path.join(self.output_folder, "intermediate_%03d.png" % self.save_index))
            self.save_index += 1
            self.last_saved_time = datetime.datetime.now()

            fitness = self.best.get_fitness(self.source_image)
            diff = self.previous_fitness - fitness
            diff_from_initial = self.initial_fitness - fitness
            module_logger.info("evolution count: %s", self.generation_count)
            module_logger.info("best: %s", len(self.best.triangles))
            match = 100.0 * (self.min_fitness - fitness) / self.min_fitness
            print "self.min_fitness:", self.min_fitness
            print "fitness:", fitness
            # 2110464
            # 149493076
            module_logger.info("fitness diff: %s %s %s: %s (%0.1f%% match)", diff, diff_from_initial, 100.0 * diff_from_initial / fitness, fitness, match)
            self.previous_fitness = fitness
        if (datetime.datetime.now() - self.last_auto_saved_time) >= self.auto_save_frequency:
            self.best.save_file(os.path.join(self.output_folder, "auto_save.txt"))
            self.last_auto_saved_time = datetime.datetime.now()

    ###################################################################
    def randomly_move_triangle(self, tri, variance):
        dx = random.randint(-variance, variance)
        dy = random.randint(-variance, variance)
        tri.move(dx, dy)

    ###################################################################
    def randomly_move_point(self, tri, variance):
        index = random.randint(0, 2)
        dx = random.randint(-variance, variance)
        dy = random.randint(-variance, variance)
        tri.move_point(index, dx, dy)

    ###################################################################
    def randomly_change_color(self, triangle):
        variance = 50
        if self.color_type == utils.RGB:
            index = random.randint(0, 2)
            c = list(triangle.color)
            c[index] += random.randint(-variance, variance)
            c[index] = clamp(0, c[index], 255)
            triangle.color = tuple(c)
        else:
            value = triangle.color + random.randint(-variance, variance)
            triangle.color += clamp(0, value, 255)

    ###################################################################
    def randomly_change_opacity(self, triangle):
        variance = 50
        value = triangle.opacity + random.randint(-variance, variance)
        triangle.opacity = clamp(0, value, 255)

    ###################################################################
    def mutate(self, mutation, triangle):
        variance = max(self.size.x, self.size.y)
        if mutation == MOVE:
            self.randomly_move_triangle(triangle, variance)
        elif mutation == SCALE:
            triangle.scale(random.uniform(0, 2))
        elif mutation == ROTATE:
            triangle.rotate(random.uniform(0, TWO_PI))
        elif mutation == MOVE_POINT:
            self.randomly_move_point(triangle, variance)
        elif mutation == CHANGE_COLOR:
            self.randomly_change_color(triangle)
        elif mutation == CHANGE_OPACITY:
            self.randomly_change_opacity(triangle)

    ###################################################################
    def evolve(self, start_sketch):
        self.best = start_sketch
        self.previous_fitness = self.best.get_fitness(self.source_image)
        self.initial_fitness = self.previous_fitness
        while True:
            self.checkpoint()
            if self.best.get_fitness(self.source_image) == 0:
                break
            new_sketch = self.best.clone()
            if len(new_sketch.triangles) == 0:
                mutation = ADD_TRIANGLE
            else:
                index = random.randint(0, len(new_sketch.triangles) - 1)
                triangle = new_sketch.triangles[index]
                mutation = random.choice(POSSIBLE_MUTATIONS)
            if mutation == REMOVE_TRIANGLE:
                if len(new_sketch.triangles) > MINIMUM_NUM_TRIANGLES:
                    del new_sketch.triangles[index]
            if mutation == ADD_TRIANGLE:
                if len(new_sketch.triangles) < self.num_triangles:
                    triangle = utils.create_random_triangles(self.size, 1, self.color_type)[0]
                    new_sketch.triangles.append(triangle)
            if mutation == CHANGE_LEVEL:
                new_index = random.randint(0, len(new_sketch.triangles) - 1)
                del new_sketch.triangles[index]
                new_sketch.triangles.insert(new_index, triangle)
            else:
                self.mutate(mutation, triangle)

            if new_sketch.get_fitness(self.source_image) <= self.best.get_fitness(self.source_image):
                self.best = new_sketch
            self.generation_count += 1
