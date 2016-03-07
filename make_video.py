import glob
import os

from PIL import Image, ImageDraw, ImageFont


########################################################################
def get_image_size(filename):
    im = Image.open(filename)
    return im.size


########################################################################
def make_combined_image(index, left_folder, right_folder, combined_folder):

    left_path = os.path.join(left_folder, "intermediate_{:03d}.png".format(index))


########################################################################
def generate_combined_folder(left_folder, right_folder, combined_folder):
    if not os.path.exists(combined_folder):
        os.mkdir(combined_folder)
    left_files = glob.glob1(left_folder, "intermediate_*.png")
    right_files = glob.glob1(right_folder, "intermediate_*.png")
    combined_files = glob.glob1(combined_folder, "combined_*.png")

    left_highest = max([int(x.split("_")[-1].split(".")[0]) for x in left_files] or [0])
    right_highest = max([int(x.split("_")[-1].split(".")[0]) for x in right_files] or [0])
    combined_highest = max([int(x.split("_")[-1].split(".")[0]) for x in combined_files] or [0])
    print "left_highest:", left_highest
    print "right_highest:", right_highest
    print "combined_highest:", combined_highest

    start_at = combined_highest
    stop_at = min(left_highest, right_highest) + 1

    size = get_image_size(os.path.join(left_folder, left_files[0]))
    middle = size[0]
    combined_size = size[0] * 2, size[1]
    font = ImageFont.truetype("/var/draft2digital/libD2D/src/libEpub/bookGeneration/pdf/fonts/D2D-GaramondPremrPro.ttf", 30)
    x = combined_size[0] - 80
    y = combined_size[1] - 50
    left_im = None
    right_im = None
    for i in range(start_at, stop_at):
        left_path = os.path.join(left_folder, "intermediate_{:03d}.png".format(i))
        if os.path.exists(left_path):
            left_im = Image.open(left_path)
        else:
            print "WARNING: path {} is missing!".format(left_path)
        right_path = os.path.join(right_folder, "intermediate_{:03d}.png".format(i))
        if os.path.exists(right_path):
            right_im = Image.open(right_path)
        else:
            print "WARNING: path {} is missing!".format(right_path)

        combined_im = Image.new("RGB", combined_size)
        if left_im:
            combined_im.paste(left_im, box=(0, 0))
        if right_im:
            combined_im.paste(right_im, box=(middle, 0))

        draw = ImageDraw.Draw(combined_im)
        hours, minutes = divmod(i, 60)
        text = "{:02d}:{:02d}".format(hours, minutes)
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        out_filename = os.path.join(combined_folder, "combined_{:04d}.png".format(i))
        print "{} of {}".format(i, stop_at)
        combined_im.save(out_filename)


########################################################################
def main():
    generate_combined_folder("/home/tnance/projects/tri_image/evolved_results/mona_lisa_500_randomized",
                             "/home/tnance/projects/tri_image/evolved_results/mona_lisa_500",
                             "/home/tnance/projects/tri_image/evolved_results/mona_lisa_combined")

    # generate_combined_folder("/home/tnance/projects/tri_image/evolved_results/picasso_500_randomized",
    #                          "/home/tnance/projects/tri_image/evolved_results/picasso_500",
    #                          "/home/tnance/projects/tri_image/evolved_results/picasso_combined")


########################################################################
if __name__ == "__main__":
    main()
