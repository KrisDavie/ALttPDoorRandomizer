from pathlib import Path
from tkinter import Tk, TOP, BOTH, Toplevel, ttk, filedialog
from PIL import Image
from source.gui.customizer.Doors.overview import door_customizer_page
from source.gui.customizer.Entrances.overview import entrance_customizer_page
from source.gui.customizer.Items.overview import item_customizer_page
from source.gui.customizer.worlds_data import World, worlds_data

from Main import __version__ as ESVersion
import os
import yaml

# This should be made better
dungeon_worlds = {
    "Overworld": World.OverWorld,
    "Underworld": World.UnderWorld,
    "Hyrule_Castle": World.HyruleCastle,
    "Eastern_Palace": World.EasternPalace,
    "Desert_Palace": World.DesertPalace,
    "Tower_of_Hera": World.TowerOfHera,
    "Castle_Tower": World.CastleTower,
    "Palace_of_Darkness": World.PalaceOfDarkness,
    "Swamp_Palace": World.SwampPalace,
    "Skull_Woods": World.SkullWoods,
    "Thieves_Town": World.ThievesTown,
    "Ice_Palace": World.IcePalace,
    "Misery_Mire": World.MiseryMire,
    "Turtle_Rock": World.TurtleRock,
    "Ganons_Tower": World.GanonsTower,
}


def customizerGUI(top=None):
    if top is None:
        mainWindow = Tk()
    else:
        mainWindow = Toplevel(top)

    self = mainWindow

    mainWindow.wm_title("Door Shuffle %s" % ESVersion)

    def load_yaml(self):
        file = filedialog.askopenfilename(
            filetypes=[("Yaml Files", (".yaml", ".yml")), ("All Files", "*")], initialdir=os.path.join(".")
        )
        with open(file, mode="r") as fh:
            yaml_data = yaml.safe_load(fh)

        for dungeon in dungeon_worlds.keys():
            self.pages["items"].pages[dungeon].content.load_yaml(
                self.pages["items"].pages[dungeon].content, yaml_data["placements"][1]
            )
            if dungeon == "Overworld":
                continue
            self.pages["pots"].pages[dungeon].content.load_yaml(
                self.pages["pots"].pages[dungeon].content, yaml_data["placements"][1]
            )
            if dungeon == "Underworld":
                continue

            self.pages["doors"].pages[dungeon].content.load_yaml(
                self.pages["doors"].pages[dungeon].content, yaml_data["doors"][1]
            )

        all_entrances = {**yaml_data["entrances"][1]["entrances"], **yaml_data["entrances"][1]["two-way"]}
        self.pages["entrances"].content.load_yaml(self.pages["entrances"].content, all_entrances)

    def save_yaml(self, save=True):
        yaml_data = {}
        entrances, er_type = self.pages["entrances"].content.return_connections(
            self.pages["entrances"].content.defined_connections
        )
        if er_type:
            yaml_data["settings"] = {1: {"shuffle": er_type}}

        if len(entrances["entrances"]) + len(entrances["two-way"]) + len(entrances["exits"]) > 0:
            yaml_data["entrances"] = {1: entrances}

        # Save doors
        yaml_data["doors"] = {1: {"doors": {}, "lobbies": {}}}

        for item_world in self.pages["doors"].pages:
            doors_data, doors_type = (
                self.pages["doors"]
                .pages[item_world]
                .content.return_connections(
                    self.pages["doors"].pages[item_world].content.door_links,
                    self.pages["doors"].pages[item_world].content.lobby_doors,
                    self.pages["doors"].pages[item_world].content.special_doors,
                )[0]
            )
            yaml_data["doors"][1]["doors"].update(doors_data["doors"])
            yaml_data["doors"][1]["lobbies"].update(doors_data["lobbies"])

        if len(yaml_data["doors"][1]) == 0:
            del yaml_data["doors"]

        # Save items
        yaml_data["placements"] = {1: {}}

        for item_world in self.pages["items"].pages:
            for loc, item in (
                self.pages["items"]
                .pages[item_world]
                .content.return_placements(self.pages["items"].pages[item_world].content.placed_items)
                .items()
            ):

                yaml_data["placements"][1].update({loc: item})
        if len(yaml_data["placements"][1]) == 0:
            del yaml_data["placements"]

        # Save Pots
        if "placements" not in yaml_data:
            yaml_data["placements"] = {1: {}}

        for pot_world in self.pages["pots"].pages:
            for loc, item in (
                self.pages["pots"]
                .pages[pot_world]
                .content.return_placements(self.pages["pots"].pages[pot_world].content.placed_items)
                .items()
            ):

                yaml_data["placements"][1].update({loc: item})
        if len(yaml_data["placements"][1]) == 0:
            del yaml_data["placements"]

        if not save:
            if len(yaml_data) == 0:
                return None
            else:
                return yaml_data
        file = filedialog.asksaveasfilename(
            filetypes=[("Yaml Files", (".yaml", ".yml")), ("All Files", "*")], initialdir=os.path.join(".")
        )
        with open(file, mode="w") as fh:
            yaml.dump(yaml_data, fh)

    self.notebook = ttk.Notebook(self)

    # make array for pages
    self.pages = {}

    # make array for frames
    self.frames = {}

    self.pages["entrances"] = ttk.Frame(self.notebook)
    self.pages["items"] = ttk.Frame(self.notebook)
    self.pages["pots"] = ttk.Frame(self.notebook)
    self.pages["doors"] = ttk.Frame(self.notebook)
    self.notebook.add(self.pages["entrances"], text="Entrances")
    self.notebook.add(self.pages["items"], text="Items")
    self.notebook.add(self.pages["pots"], text="Pots")
    self.notebook.add(self.pages["doors"], text="Doors")
    self.notebook.pack()

    self.pages["items"].notebook = ttk.Notebook(self.pages["items"])
    self.pages["items"].pages = {}

    self.pages["pots"].notebook = ttk.Notebook(self.pages["pots"])
    self.pages["pots"].pages = {}

    self.pages["doors"].notebook = ttk.Notebook(self.pages["doors"])
    self.pages["doors"].pages = {}

    self.pages["entrances"].content = entrance_customizer_page(self, self.pages["entrances"])
    self.pages["entrances"].content.pack(side=TOP, fill=BOTH, expand=True)

    eg_map = Path("resources") / "app" / "gui" / "plandomizer" / "maps" / "egmap.png"
    eg_img = Image.open(eg_map)

    for dungeon, world in dungeon_worlds.items():
        self.pages["items"].pages[dungeon] = ttk.Frame(self.pages["items"].notebook)
        self.pages["items"].notebook.add(self.pages["items"].pages[dungeon], text=dungeon.replace("_", " "))
        self.pages["items"].pages[dungeon].content = item_customizer_page(
            self, self.pages["items"].pages[dungeon], world, tab_item_type="standard", eg_img=eg_img
        )
        self.pages["items"].pages[dungeon].content.pack(side=TOP, fill=BOTH, expand=True)

        if dungeon == "Overworld":
            continue

        self.pages["pots"].pages[dungeon] = ttk.Frame(self.pages["pots"].notebook)
        self.pages["pots"].notebook.add(self.pages["pots"].pages[dungeon], text=dungeon.replace("_", " "))
        self.pages["pots"].pages[dungeon].content = item_customizer_page(
            self, self.pages["pots"].pages[dungeon], world, tab_item_type="pot", eg_img=eg_img
        )
        self.pages["pots"].pages[dungeon].content.pack(side=TOP, fill=BOTH, expand=True)

        if dungeon == "Underworld":
            continue

        self.pages["doors"].pages[dungeon] = ttk.Frame(self.pages["doors"].notebook)
        self.pages["doors"].notebook.add(self.pages["doors"].pages[dungeon], text=dungeon.replace("_", " "))
        self.pages["doors"].pages[dungeon].content = door_customizer_page(
            self, self.pages["doors"].pages[dungeon], world, eg_img=eg_img
        )
        self.pages["doors"].pages[dungeon].content.pack(side=TOP, fill=BOTH, expand=True)

    self.pages["items"].notebook.pack()
    self.pages["pots"].notebook.pack()
    self.pages["doors"].notebook.pack()
    save_data_button = ttk.Button(self, text="Save Customizer Data", command=lambda: save_yaml(self))
    save_data_button.pack()
    load_data_button = ttk.Button(self, text="Load Customizer Data", command=lambda: load_yaml(self))
    load_data_button.pack()

    def close_window():
        if top:
            self.withdraw()
            yaml_data = save_yaml(self, save=False)
            top.widgets["plandomizer"].window = self
            top.widgets["plandomizer"].storageVar.set(yaml_data)
            top.widgets["customizer"].storageVar.set(yaml_data)
        else:
            self.destroy()

    mainWindow.protocol("WM_DELETE_WINDOW", close_window)

    mainWindow.mainloop()


if __name__ == "__main__":
    customizerGUI()
