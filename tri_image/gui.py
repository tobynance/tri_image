import Tkinter

import datetime
import os

from PIL import ImageTk
import thread
import application


########################################################################
class GUIApplication(Tkinter.Frame):
    ####################################################################
    def __init__(self, master, evolver, starting_sketch):
        Tkinter.Frame.__init__(self, master)
        self.evolver = evolver
        self.photo = ImageTk.PhotoImage(starting_sketch.get_image())
        thread.start_new_thread(self.evolver.evolve, (starting_sketch,))
        self.create_widgets()
        self.pack()
        self.after(1000, self.update_image)

    ####################################################################
    def create_widgets(self):
        self.image = Tkinter.Label(self)
        self.image["image"] = self.photo
        self.image.pack({"side": "top"})
        self.stats = Tkinter.Frame(self)
        self.stats.pack({"side": "bottom"})
        self.generation_label = Tkinter.Label(self.stats, text="Generation:")
        self.generation_label.pack({"side": "left"})
        self.generation = Tkinter.Label(self.stats, text="0")
        self.generation.pack({"side": "left"})
        self.spacer = Tkinter.Label(self.stats, text="     ")  # a hack around not knowing how best to space out the sections of the stats
        self.spacer.pack({"side": "left"})
        self.num_triangles_label = Tkinter.Label(self.stats, text="# Triangles:")
        self.num_triangles = Tkinter.Label(self.stats, text="0")
        self.num_triangles.pack({"side": "right"})
        self.num_triangles_label.pack({"side": "right"})

    ####################################################################
    def update_image(self):
        self.after(1000, self.update_image)
        self.generation["text"] = str(self.evolver.generation_count)
        sketch = self.evolver.best
        if sketch:
            image = sketch.image
            if image:
                self.photo = ImageTk.PhotoImage(image)
                self.image["image"] = self.photo
                self.num_triangles["text"] = str(len(sketch.triangles))


########################################################################
if __name__ == "__main__":
    application.initialize_logging()
    options = application.parse_options()

    evolver, starting_sketch = application.get_evolver_and_sketch(**options)

    window_name = os.path.basename(options["output_folder"])

    root = Tkinter.Tk()
    root.wm_title(window_name)
    gui = GUIApplication(master=root, evolver=evolver, starting_sketch=starting_sketch)
    gui.mainloop()
