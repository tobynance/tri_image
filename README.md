# tri_image
Make images out of triangles

Original Blog post that inspired this:
http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/

Original Slashdot post about it:
http://developers.slashdot.org/story/08/12/09/0238252/evolution-of-mona-lisa-via-genetic-programming

To get the GUI version working in a virtual environment named `tri_image` on Linux (Linux Mint), I had to install the
ubuntu package `python-pil.imagetk` then copy
`/usr/lib/python2.7/dist-packages/PIL/_imagingtk.so` to `~/.virtualenvs/tri_image/lib/python2.7/site-packages/PIL/_imagingtk.so`.

Example usage:

```
# For GUI version (you can actively watch the evolution)
python gui.py ../input_images/mona_lisa.jpg ../evolved_results/mona_lisa_500 --num-triangles 500

# For non-GUI version
python application.py ../input_images/mona_lisa.jpg ../evolved_results/mona_lisa_500 --num-triangles 500

```

To make a video of the results:

```
# 10 frames per second, taken from the images in the folder picasso_500
ffmpeg -r 10  -i picasso_500/intermediate_%03d.png picasso.mp4
```

To make a complicated video with variable speed and side-by-side comparisons:
run `make_video.py`, then copy the 1st hundred images into a folder named *1*, then images 100-499 into a folder named *2*,
and the rest into a folder named *3*.
Then, run:

```
ffmpeg -r 10 -i 1/combined_%04d.png picasso_1.mp4
ffmpeg -r 20 -start_number 100 -i 2/combined_%04d.png picasso_2.mp
ffmpeg -r 30 -start_number 500 -i 3/combined_%04d.png picasso_3.mp4
mencoder picasso_1.mp4 picasso_2.mp4 picasso_3.mp4 -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=1800 -o picasso.avi
```
