from tkinter import Tk, Button, BOTTOM, TOP, StringVar, BooleanVar, X, BOTH, RIGHT, ttk, messagebox, filedialog
from source.gui.customizer.Entrances.overview import entrance_customizer_page
from source.gui.customizer.Items.overview import item_customizer_page
from Main import __version__ as ESVersion
import os
import yaml


def guiMain(args=None):
    mainWindow = Tk()
    self = mainWindow

    mainWindow.wm_title("Door Shuffle %s" % ESVersion)
    # mainWindow.protocol("WM_DELETE_WINDOW", guiExit)  # intercept when user clicks the X

    def load_yaml(self):
        file = filedialog.askopenfilename(
            filetypes=[("Yaml Files", (".yaml", ".yml")), ("All Files", "*")], initialdir=os.path.join(".")
        )
        with open(file, mode="r") as fh:
            yaml_data = yaml.safe_load(fh)
        self.pages["underworld_items"].content.load_yaml(
            self.pages["underworld_items"].content, yaml_data["placements"][1]
        )
        all_entrances = {**yaml_data["entrances"][1]["entrances"], **yaml_data["entrances"][1]["two-way"]}
        self.pages["entrances"].content.load_yaml(self.pages["entrances"].content, all_entrances)


    self.notebook = ttk.Notebook(self)

    # make array for pages
    self.pages = {}

    # make array for frames
    self.frames = {}

    self.pages["entrances"] = ttk.Frame(self.notebook)
    self.pages["underworld_items"] = ttk.Frame(self.notebook)
    self.notebook.add(self.pages["entrances"], text="Entrances")
    self.notebook.add(self.pages["underworld_items"], text="Items (Underworld)")
    self.notebook.pack()

    self.pages["entrances"].content = entrance_customizer_page(self, self.pages["entrances"])
    self.pages["entrances"].content.pack(side=TOP, fill=BOTH, expand=True)

    self.pages["underworld_items"].content = item_customizer_page(self, self.pages["underworld_items"])
    self.pages["underworld_items"].content.pack(side=TOP, fill=BOTH, expand=True)

    load_data_button = ttk.Button(self, text="Load Customizer Data", command=lambda: load_yaml(self))
    load_data_button.pack()

    mainWindow.mainloop()


if __name__ == "__main__":
    guiMain()
