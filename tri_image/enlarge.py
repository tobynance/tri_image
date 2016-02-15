import sys, os
from PIL import Image
import sketch
import point
#######################################################################
def main():
    dat_filename = sys.argv[1]
    enlarge = int(sys.argv[2])
    out_filename = sys.argv[3]

    s = sketch.Sketch.read(dat_filename)
    s.size = point.Point(s.size.x * enlarge, s.size.y * enlarge)
    for tri in s.triangles:
        for i in range(len(tri.coordinates)):
            tri.coordinates[i] *= enlarge
    s.saveImage(out_filename)

#######################################################################
main()
