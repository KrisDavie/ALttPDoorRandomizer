from enum import Enum
from tkinter import Toplevel, ttk, NW, Canvas
from PIL import ImageTk, Image, ImageOps
import source.gui.customizer.item_sprite_data as item_sprite_data
from source.gui.customizer.worlds_data import worlds_data
from pathlib import Path


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


BORDER_SIZE = 20

item_sheet_path = Path("resources") / "app" / "gui" / "plandomizer" / "Item_Sheet.png"


def item_customizer_page(top, parent, tab_world):
    def load_yaml(self, yaml_data):
        for loc_name, placed_item in yaml_data.items():
            if loc_name not in worlds_data[tab_world]["locations"]:
                continue
            item = worlds_data[tab_world]["locations"][loc_name]["button"]
            if placed_item.startswith("Crystal"):
                crystal_num = int(placed_item[-1])
                if crystal_num in [5, 6]:
                    placed_item = "Red Crystal"
                else:
                    placed_item = "Crystal"
            if loc_name not in self.placed_items:
                self.placed_items[loc_name] = {"name": placed_item, "sprite": None}
            place_item(self, item, placed_item, loc_name)

    def display_world_locations(self, world):
        objects = self.canvas.find_all()
        for name, loc in worlds_data[world]["locations"].items():
            if "target" in loc:
                fill_col = "blue"
            else:
                fill_col = "#0f0"
            if "button" not in loc or loc["button"] not in objects:
                location_oval = self.canvas.create_oval(
                    loc["x"] + BORDER_SIZE - 5,
                    loc["y"] + BORDER_SIZE - 5,
                    loc["x"] + BORDER_SIZE + 5,
                    loc["y"] + BORDER_SIZE + 5,
                    fill=fill_col,
                )
                worlds_data[world]["locations"][name]["button"] = location_oval
            else:
                location_oval = loc["button"]
                self.canvas.itemconfigure((location_oval,), state="normal")
            self.canvas.tag_bind(
                location_oval,
                "<Button-1>",
                lambda event: select_location(self, event),
            )

    def get_loc_by_button(self, button):
        for name, loc in worlds_data[tab_world]["locations"].items():
            if loc["button"] == button[0]:
                return name
        for name, data in self.placed_items.items():
            if data["image"] == button[0]:
                return name

    def place_item(self, item, placed_item, loc_name):
        self.canvas.itemconfigure(item, state="hidden")

        # Place a new sprite
        sprite_y, sprite_x = item_sprite_data.item_table[placed_item]
        self.placed_items[loc_name]["sprite"] = ImageTk.PhotoImage(
            ImageOps.expand(
                Image.open(item_sheet_path).crop(
                    (sprite_x * 16, sprite_y * 16, sprite_x * 16 + 16, sprite_y * 16 + 16)
                ),
                1,
                "#fff",
            )
        )
        self.placed_items[loc_name]["image"] = self.canvas.create_image(
            worlds_data[tab_world]["locations"][loc_name]["x"] + BORDER_SIZE,
            worlds_data[tab_world]["locations"][loc_name]["y"] + BORDER_SIZE,
            image=self.placed_items[loc_name]["sprite"],
        )
        self.canvas.tag_bind(
            self.placed_items[loc_name]["image"],
            "<Button-3>",
            lambda event: remove_item(self, event),
        )

    def select_location(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in worlds_data[tab_world]["canvas_image"]:
            return
        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)
        self.currently_selected = loc_name
        self.canvas.itemconfigure(item, fill="orange", state="disabled")

        # Show the sprite sheet
        show_sprites(self, event, prize=True if "Prize" in loc_name else False)

        # Hide the circle
        if loc_name not in self.placed_items:
            self.canvas.itemconfigure(item, fill="#0f0", state="normal")
            return
        placed_item = self.placed_items[loc_name]["name"]
        place_item(self, item, placed_item, loc_name)

    def remove_item(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return
        loc_name = get_loc_by_button(self, item)
        self.canvas.itemconfigure(item, state="hidden")
        loc_ref = worlds_data[tab_world]["locations"][loc_name]["button"]
        self.canvas.itemconfigure((loc_ref,), state="normal", fill="#0f0")
        del self.placed_items[loc_name]["image"]
        del self.placed_items[loc_name]["sprite"]
        self.placed_items[loc_name]["image"] = None
        self.placed_items[loc_name]["sprite"] = None
        del self.placed_items[loc_name]

    def return_placements(placed_items):
        final_placements = {}
        cystals_placed = 0
        red_crystals_placed = 0
        for loc_name, item_data in placed_items.items():
            if item_data["name"] == "Crystal":
                cystals_placed += 1
                final_placements[loc_name] = f"Crystal {cystals_placed}"
            elif item_data["name"] == "Red Crystal":
                red_crystals_placed += 1
                final_placements[loc_name] = f"Crystal {red_crystals_placed + 5}"
            else:
                final_placements[loc_name] = item_data["name"]

        return final_placements

    # TODO: Refactor this out, will be reused in other places
    def show_sprites(self, parent_event, prize=False):
        prize_names = [
            "Green Pendant",
            "Red Pendant",
            "Blue Pendant",
            "Crystal",
            "Red Crystal",
        ]

        def select_sprite(parent, self, event):
            item = self.canvas.find_closest(event.x, event.y)
            if item in [w["canvas_image"] for w in worlds_data.values()]:
                return
            item_name = get_sprite_by_button(self, item)

            parent.placed_items[parent.currently_selected] = {"name": item_name, "sprite": None}
            self.destroy()

        def get_sprite_by_button(self, button):
            for name, loc in self.items.items():
                if loc == button[0]:
                    return name

        sprite_window = Toplevel(self)
        w = top.winfo_x()
        h = top.winfo_y()
        x = max(0, min(w + parent_event.x - 544, self.winfo_screenwidth() - 544))
        y = max(0, min(h + parent_event.y - 288, self.winfo_screenheight() - 288))
        sprite_window.geometry(f"{544 + (BORDER_SIZE * 2)}x{288 + (BORDER_SIZE * 2)}+{int(x)}+{int(y)}")
        sprite_window.title("Sprites Window")
        sprite_window.focus_set()
        sprite_window.grab_set()

        sprite_window.canvas = Canvas(
            sprite_window, width=544 + (BORDER_SIZE * 2), height=288 + (BORDER_SIZE * 2), background="black"
        )
        sprite_window.canvas.pack()
        sprite_window.spritesheet = ImageTk.PhotoImage(Image.open(item_sheet_path).resize((544, 288)))
        sprite_window.image = sprite_window.canvas.create_image(
            0 + BORDER_SIZE, 0 + BORDER_SIZE, anchor=NW, image=sprite_window.spritesheet
        )
        sprite_window.items = {}
        for item, coords in item_sprite_data.item_table.items():
            if (prize and item not in prize_names) or (not prize and item in prize_names):
                disabled = True
            else:
                disabled = False

            y, x = coords
            item_selector = sprite_window.canvas.create_rectangle(
                x * 32 + BORDER_SIZE,
                y * 32 + BORDER_SIZE,
                x * 32 + 33 + BORDER_SIZE,
                y * 32 + 33 + BORDER_SIZE,
                outline="",
                fill="#888" if disabled else "",
                stipple="gray12" if disabled else "",
                state="disabled" if disabled else "normal",
            )
            sprite_window.items[item] = item_selector
            sprite_window.canvas.tag_bind(
                item_selector,
                "<Button-1>",
                lambda event: select_sprite(self, sprite_window, event),
            )
        sprite_window.wait_window(sprite_window)
        sprite_window.grab_release()

    # Custom Item Pool
    self = ttk.Frame(parent)
    self.cwidth = 1024
    self.cheight = 512
    self.select_state = SelectState.NoneSelected
    self.placed_items = {}
    self.canvas = Canvas(self, width=self.cwidth + (BORDER_SIZE * 2), height=self.cheight + (BORDER_SIZE * 2))
    self.canvas.pack()

    # Load in the world images
    worlds_data[tab_world]["map_image"] = ImageTk.PhotoImage(Image.open(worlds_data[tab_world]["map_file"]))
    worlds_data[tab_world]["canvas_image"] = (
        self.canvas.create_image(BORDER_SIZE, BORDER_SIZE, anchor=NW, image=worlds_data[tab_world]["map_image"]),
    )

    # Display locations (and map?)
    for name, loc in worlds_data[tab_world]["locations"].items():
        worlds_data[tab_world]["locations"][name]["x"] *= 2
        worlds_data[tab_world]["locations"][name]["y"] *= 2

    display_world_locations(self, tab_world)

    self.load_yaml = load_yaml
    self.return_placements = return_placements

    # TODO: Add a new button to store this info somwhere as JSON for the generation
    return self
