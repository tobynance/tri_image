import Tkinter

import datetime
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
        self.image.pack({"side": "left"})

    ####################################################################
    def update_image(self):
        self.after(1000, self.update_image)
        sketch = self.evolver.best
        if sketch:
            image = sketch.image
            if image:
                self.photo = ImageTk.PhotoImage(image)
                self.image["image"] = self.photo


########################################################################
if __name__ == "__main__":
    application.initialize_logging()
    options = application.parse_options()

    evolver, starting_sketch = application.get_evolver_and_sketch(**options)

    root = Tkinter.Tk()
    root.wm_title("tri_image")
    gui = GUIApplication(master=root, evolver=evolver, starting_sketch=starting_sketch)
    gui.mainloop()
