from tkinter import Tk, Button, BOTTOM, TOP, StringVar, BooleanVar, X, BOTH, RIGHT, ttk, messagebox
from source.gui.customizer.overview import customizer_page
from Main import __version__ as ESVersion


def guiMain(args=None):
    mainWindow = Tk()
    self = mainWindow

    mainWindow.wm_title("Door Shuffle %s" % ESVersion)
    # mainWindow.protocol("WM_DELETE_WINDOW", guiExit)  # intercept when user clicks the X

    self.notebook = ttk.Notebook(self)

    # make array for pages
    self.pages = {}

    # make array for frames
    self.frames = {}

    self.pages["customizer"] = ttk.Frame(self.notebook)
    self.notebook.add(self.pages["customizer"], text="Customizer")
    self.notebook.pack()

    self.pages["customizer"].content = customizer_page(self, self.pages["customizer"])
    self.pages["customizer"].content.pack(side=TOP, fill=BOTH, expand=True)

    mainWindow.mainloop()


if __name__ == "__main__":
    guiMain()
