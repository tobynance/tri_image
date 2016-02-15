import os, sys, datetime, glob
from PIL import Image
from seeder import Seeder
from evolver import Evolver
from sketch import Sketch
import utils
BASE_INPUT_FOLDER="../../data/input/"
BASE_OUTPUT_FOLDER="../../data/output/"

#######################################################################
class Application(object):
    def __init__(self):
        self.evolver = None

    ###################################################################
    def run(self, source_image, output_folder, num_triangles, save_frequency, start_from=None, continueRun=False):
        im = Image.open(os.path.join(BASE_INPUT_FOLDER, source_image))
        output_folder = os.path.join(BASE_OUTPUT_FOLDER, output_folder)
        assert(not (start_from and continueRun))
        ### NOTE: you should only use start_from or continueRun, not both
        sketch = None
        if continueRun:
            ### find the latest file in the folder
            filenames = glob.glob(os.path.join(output_folder, "intermediate_???.txt"))
            best = -1
            for filename in filenames:
                num = int(filename[-7:-4])
                if num > best:
                    best = num
            if best >= 0:
                filename = os.path.join(output_folder, "intermediate_%03d.txt" % best)
                print filename
                sketch = Sketch.read(filename)
                e = Evolver(im, output_folder, num_triangles, save_frequency, save_index=best+1)

        if sketch == None:
            utils.cleanDir(output_folder)
            if start_from:
                sketch = Sketch.read(start_from)
            else:
                seeder = Seeder(im, output_folder, num_triangles)
                sketch = seeder.run()
            sketch.saveImage(os.path.join(output_folder, "test_seeded.png"))
            sketch.saveFile(os.path.join(output_folder, "test_seeded.txt"))
            e = Evolver(im, output_folder, num_triangles, save_frequency)
        self.evolver = e
        print "start evolution..."
        better = e.evolve(sketch)
        better.saveImage(os.path.join(output_folder, "test_evolve.png"))
        better.saveFile(os.path.join(output_folder, "test_evolve.txt"))

#######################################################################
if __name__ == "__main__":
    a = Application()
    #a.run("monalisa.bmp", "mona_200", 200, datetime.timedelta(seconds=60),
    #      start_from="/data/projects/kris/triangular_image/tested_version/data/output/mona.txt")
    #a.run("monet.png", "monet_2000", 2000, datetime.timedelta(seconds=60), continueRun=True)
    #a.run("rembrandt_med.jpg", "rembrandt_meditation_1000", 1000, datetime.timedelta(seconds=60), continueRun=True)
    a.run("sky_less_big.png", "sky_less_big_2000", 2000, datetime.timedelta(seconds=180), continueRun=True)
