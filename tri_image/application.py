import argparse
import sys
import datetime
import glob
import os
import logging

from PIL import Image

import utils
from evolver import Evolver
from seeder import Seeder, RandomSeeder
from sketch import Sketch

module_logger = logging.getLogger(__name__)


####################################################################
def get_evolver_and_sketch(source_image, output_folder, num_triangles, save_frequency, color_type, start_from=None, continue_run=False, randomized=False):
    im = Image.open(source_image)
    im = im.convert(mode=color_type)
    assert not (start_from and continue_run), "you should only use start_from or continue_run, not both"
    sketch = None
    e = None
    if continue_run:
        # find the latest file in the folder
        file_names = glob.glob(os.path.join(output_folder, "intermediate_???.txt"))
        best = -1
        for filename in file_names:
            num = int(filename[-7:-4])
            if num > best:
                best = num
        if best >= 0:
            filename = os.path.join(output_folder, "intermediate_%03d.txt" % best)
            module_logger.info("Restarting evolution based on found file 'intermediate_%03d.txt'", best)
            sketch = Sketch.read(filename)
            e = Evolver(im, output_folder, num_triangles, save_frequency, color_type=color_type, save_index=best+1)

    # Preferred is to load from the auto-save, but in case it died while saving the above will still work
    filename = os.path.join(output_folder, "auto_save.txt")
    if os.path.exists(filename):
        sketch = Sketch.read(filename)

    if sketch is None:
        utils.clean_dir(output_folder)
        if start_from:
            sketch = Sketch.read(start_from)
        else:
            if randomized:
                seeder = RandomSeeder(im, output_folder, num_triangles, color_type)
            else:
                seeder = Seeder(im, output_folder, num_triangles, color_type)
            sketch = seeder.run()
        e = Evolver(im, output_folder, num_triangles, save_frequency, color_type=color_type)
    return e, sketch


########################################################################
def initialize_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


########################################################################
def parse_options():
    initialize_logging()

    parser = argparse.ArgumentParser(description="Run a toy evolution program to draw pictures using triangles")
    parser.add_argument("source_image", type=str, help="Path to target image for the evolution to generate")
    parser.add_argument("output_folder", type=str, help="Path to folder where the images and data files will be stored")
    parser.add_argument("--num-triangles", type=int, default=50, help="Number of triangles to use to create the image.  Minimum of 10, default of 50")
    parser.add_argument("--save-frequency", type=int, default=60, help="Number of seconds between auto-saves, default is 60 seconds")
    parser.add_argument("--randomized", action="store_true", default=False, help="Start with random triangles, instead of kick-starting the system using Seeder. Default False")
    parser.add_argument("--gray-scale", action="store_true", default=False, help="Create gray scale results")
    args = parser.parse_args()
    if args.num_triangles < 10:
        print "--num-triangles must be at least 10!"
        sys.exit()
    if args.gray_scale:
        color_type = utils.GRAY_SCALE
    else:
        color_type = utils.RGB

    application_options = dict(
        source_image=args.source_image,
        output_folder=args.output_folder,
        num_triangles=args.num_triangles,
        save_frequency=datetime.timedelta(seconds=args.save_frequency),
        continue_run=True,
        randomized=args.randomized,
        color_type=color_type)

    return application_options


#######################################################################
if __name__ == "__main__":
    options = parse_options()
    evolver, starting_sketch = get_evolver_and_sketch(**options)
    module_logger.info("start evolution...")
    evolver.evolve(starting_sketch)
