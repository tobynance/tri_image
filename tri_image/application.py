import datetime
import glob
import os

from PIL import Image

import utils
from evolver import Evolver
from seeder import Seeder
from sketch import Sketch


########################################################################
class Application(object):
    ####################################################################
    def __init__(self):
        self.evolver = None

    ####################################################################
    def run(self, source_image, output_folder, num_triangles, save_frequency, start_from=None, continue_run=False):
        im = Image.open(source_image)
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
                print filename
                sketch = Sketch.read(filename)
                e = Evolver(im, output_folder, num_triangles, save_frequency, save_index=best+1)

        if sketch is None:
            utils.clean_dir(output_folder)
            if start_from:
                sketch = Sketch.read(start_from)
            else:
                seeder = Seeder(im, output_folder, num_triangles)
                sketch = seeder.run()
            sketch.save_image(os.path.join(output_folder, "test_seeded.png"))
            sketch.save_file(os.path.join(output_folder, "test_seeded.txt"))
            e = Evolver(im, output_folder, num_triangles, save_frequency)
        if e is None:
            print "Not able to create Evolver - bailing."
            return
        self.evolver = e
        print "start evolution..."
        better = e.evolve(sketch)
        better.save_image(os.path.join(output_folder, "test_evolve.png"))
        better.save_file(os.path.join(output_folder, "test_evolve.txt"))


#######################################################################
if __name__ == "__main__":
    a = Application()
    # a.run("monalisa.bmp", "mona_200", 200, datetime.timedelta(seconds=60),
    #       start_from="/data/projects/kris/triangular_image/tested_version/data/output/mona.txt")
    # a.run("monet.png", "monet_2000", 2000, datetime.timedelta(seconds=60), continueRun=True)
    # a.run("rembrandt_med.jpg", "rembrandt_meditation_1000", 1000, datetime.timedelta(seconds=60), continueRun=True)
    a.run("sky_less_big.png", "sky_less_big_2000", 2000, datetime.timedelta(seconds=180), continue_run=True)
