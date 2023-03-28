from pathlib import Path
import pickle
from tkinter import Tk, TOP, BOTH, Toplevel, ttk, filedialog
from PIL import Image
from SpoilerToYaml import parse_dr_spoiler
from source.gui.customizer.Doors.overview import door_customizer_page
from source.gui.customizer.Entrances.overview import entrance_customizer_page
from source.gui.customizer.Items.overview import item_customizer_page
from source.gui.customizer.worlds_data import dungeon_worlds
from source.gui.customizer.doors_data import eg_tile_multiuse

from Main import __version__ as ESVersion
import os
import yaml

# This should be made better


def customizerGUI(top=None):
    if top is None:
        mainWindow = Tk()
    else:
        mainWindow = Toplevel(top)

    self = mainWindow

    mainWindow.wm_title("Door Shuffle %s" % ESVersion)

    def _save_vanilla(self):
        data = {}
        # Tile map, tile_size, map_dims
        for dungeon in dungeon_worlds.keys():
            if dungeon in ["Overworld", "Underworld"]:
                continue
            data[dungeon] = {
                'tiles': {k: {'map_tile': v['map_tile']} for k, v in self.pages["doors"].pages[dungeon].content.tiles.items() if 'map_tile' in v },
                "tile_size": self.pages["doors"].pages[dungeon].content.tile_size,
                "map_dims": self.pages["doors"].pages[dungeon].content.map_dims,
                'x_offset': self.pages["doors"].pages[dungeon].content.x_offset,
                'y_offset': self.pages["doors"].pages[dungeon].content.y_offset,
            }
        with open("vanilla_layout.pickle", "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def load_yaml(self):
        file = filedialog.askopenfilename(
            filetypes=[("Yaml Files", (".yaml", ".yml")), ("All Files", "*")], initialdir=os.path.join(".")
        )
        with open(file, mode="r") as fh:
            try:
                yaml_data = yaml.safe_load(fh)
            except:
                print("Error loading yaml file. Attempting to load DR spoiler log.")
                try:
                    fh.seek(0)
                    yaml_data = parse_dr_spoiler(fh)
                except Exception as e:
                    print(f"Error loading DR spoiler log. {e}")
                    return

        for dungeon in dungeon_worlds.keys():
            self.pages["items"].pages[dungeon].content.load_yaml(
                self.pages["items"].pages[dungeon].content,
                yaml_data["placements"][1] if "placements" in yaml_data else {},
            )
            if dungeon == "Overworld":
                continue
            self.pages["pots"].pages[dungeon].content.load_yaml(
                self.pages["pots"].pages[dungeon].content,
                yaml_data["placements"][1] if "placements" in yaml_data else {},
            )
            if dungeon == "Underworld":
                continue

            if "doors" in yaml_data:
                self.pages["doors"].pages[dungeon].content.load_yaml(
                    self.pages["doors"].pages[dungeon].content, yaml_data["doors"][1]
                )

        if "entrances" in yaml_data:
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
                )
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

    def hide_dont_close(self):
        self.eg_tile_window.grab_release()
        self.eg_tile_window.withdraw()

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

    self.eg_tile_window = Toplevel(self)
    self.eg_tile_window.wm_title("EG Tiles")
    self.eg_tile_window.title("EG Map Window")
    self.eg_tile_window.protocol("WM_DELETE_WINDOW", lambda: hide_dont_close(self))
    self.eg_tile_window.notebook = ttk.Notebook(self.eg_tile_window)
    self.eg_tile_window.pages = {}
    with open(Path("resources/app/gui/plandomizer/vanilla_layout.pickle"), "rb") as f:
        vanilla_layout = pickle.load(f)

    self.eg_tile_multiuse = eg_tile_multiuse.copy()
    self.disabled_eg_tiles = {}
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

        self.eg_tile_window.pages[dungeon] = ttk.Frame(self.eg_tile_window.notebook)
        self.eg_tile_window.notebook.add(self.eg_tile_window.pages[dungeon], text=dungeon.replace("_", " "))
        self.eg_tile_window.pages[dungeon].content = door_customizer_page(
            self, self.eg_tile_window.pages[dungeon], world, 
            eg_img=eg_img, 
            eg_selection_mode=True, 
            vanilla_data=vanilla_layout[dungeon],
            plando_window=self.pages["doors"].notebook)
        self.eg_tile_window.pages[dungeon].content.pack(side=TOP, fill=BOTH, expand=True)

    self.pages["items"].notebook.pack()
    self.pages["pots"].notebook.pack()
    self.pages["doors"].notebook.pack()
    self.eg_tile_window.notebook.pack()
    save_data_button = ttk.Button(self, text="Save Customizer Data", command=lambda: save_yaml(self))
    save_data_button.pack()
    load_data_button = ttk.Button(self, text="Load Customizer Data", command=lambda: load_yaml(self))
    load_data_button.pack()
    self.eg_tile_window.withdraw()

    # save_vanilla_button = ttk.Button(self, text="Save Vanilla Data", command=lambda: _save_vanilla(self))
    # save_vanilla_button.pack()

    def close_window():
        if top:
            self.withdraw()
            yaml_data = save_yaml(self, save=False)
            top.widgets["plandomizer"].window = self
            top.widgets["plandomizer"].storageVar.set(yaml_data)
            top.widgets["customizer"].storageVar.set(yaml_data)
        else:
            self.eg_tile_window.destroy()
            self.destroy()

    mainWindow.protocol("WM_DELETE_WINDOW", close_window)

    if top is None:
        mainWindow.mainloop()


if __name__ == "__main__":
    customizerGUI()
