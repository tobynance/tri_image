import sys, datetime
from PyQt4 import QtGui, QtCore
from ImageQt import ImageQt
from PIL import Image
import application

### allow a user to interactively run the evolver, and allow them to start where
### they left off, and pause, etc.
### This will let me see the best output so far.  I probably need to create a
### configuration file based off of the user's input, so that they don't have to
### reenter the information.
### I should probably also eliminate the 'only run this long' timer.
#######################################################################
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(800, 600)
        self.setWindowTitle("triImage")
        fileMenu = self.menuBar().addMenu("File")
        testAction = QtGui.QAction("testAction", self)
        closeAction = QtGui.QAction("closeAction", self)
        self.connect(testAction, QtCore.SIGNAL("triggered()"), self.newRun)
        fileMenu.addAction(testAction)
        fileMenu.addAction(closeAction)
        self.image = ImageWindow(self)
        self.setCentralWidget(self.image)
        self.app = RunApplication(self)
        self.app.start()
        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)
        self.timer.start(1000)
    
    ###################################################################
    def newRun(self):
        print "newRun"

    ###################################################################
    def update(self):
        evolver = self.app.app.evolver
        if evolver:
            sketch = evolver.best
            if sketch:
                image = sketch.getImage()
                self.image.setImage(image)

#######################################################################
class ImageWindow(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.image = QtGui.QLabel(self)
        self.image.resize(800, 600)
    
    ###################################################################
    def setImage(self, im):
        image = ImageQt(im)
        self.image.setPixmap(QtGui.QPixmap.fromImage(image))

#######################################################################
class RunApplication(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.app = application.Application()
        self.input_image_name = None
        self.output_folder = None
        self.num_triangles = 0
        self.save_rate = None

    ###################################################################
    def setup(input_image_name, output_folder, num_triangles, save_rate):
        self.input_image_name = input_image_name
        self.output_folder = output_folder
        self.num_triangles = num_triangles
        self.save_rate = save_rate

    ###################################################################
    def run(self):
        #self.app.run("mona-lisa-painting.jpg", "gui_mona_500", 500, datetime.timedelta(seconds=180), continueRun=True)
        #self.app.run("mona-lisa-painting.jpg", "gui_mona_variable", 500, datetime.timedelta(seconds=180), continueRun=True)
        #self.app.run("marx_cubist.jpg", "gui_marx_cubist_500", 500, datetime.timedelta(seconds=180), continueRun=True)
        #self.app.run("cubism_art.jpg", "gui_cubism_art_500", 500, datetime.timedelta(seconds=180), continueRun=True)
        #self.app.run("parascan_cubism.jpg", "gui_parascan_cubism_500", 100, datetime.timedelta(seconds=180), continueRun=True)
        #self.app.run(self.input_image_name, self.output_folder, self.num_triangles, self.save_rate, continueRun=True)
        self.app.run("mona-lisa-painting.jpg", "gui_mona_1000", 1000, datetime.timedelta(seconds=180), continueRun=True)

#######################################################################
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()

