# tri_image
Make images out of triangles

Original Blog post that inspired this:
http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/

Original Slashdot post about it:
http://developers.slashdot.org/story/08/12/09/0238252/evolution-of-mona-lisa-via-genetic-programming

As a convenience, I found running this useful:

```
pqiv --watch-directories --slideshow-interval=2 -s -t /path/to/image_folder
```

To get this working in a virtual environment on linux, I had to install the ubuntu package `python-pil.imagetk` then copy
`/usr/lib/python2.7/dist-packages/PIL/_imagingtk.so` to `.virtualenvs/tri_image/lib/python2.7/site-packages/PIL/_imagingtk.so`.

Example usage:

python gui.py ../input_images/mona_lisa.jpg ../evolved_results/mona_lisa_500 --num-triangles 500
