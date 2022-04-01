from enum import Enum
from tkinter import Toplevel, ttk, NW, Canvas, LAST
from PIL import ImageTk, Image, ImageOps
import source.gui.customizer.location_data as location_data
import source.gui.customizer.item_sprite_data as item_sprite_data
import yaml
import random

# TODO: Do I add underworld? This will be needed for decoupled shuffles


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


class World(Enum):
    LightWorld = 0
    DarkWorld = 1
    UnderWorld = 2


BORDER_SIZE = 20

hex_col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]


def item_customizer_page(top, parent):

    worlds_data = {
        World.UnderWorld: {
            "locations": location_data.underworld_coordinates,
            "map_image": None,
            "canvas_image": None,
        },
    }

    def display_world_locations(self, world):
        for name, loc in worlds_data[world]["locations"].items():
            if "target" in loc:
                fill_col = "blue"
            else:
                fill_col = "#0f0"
            if "button" not in loc:
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
        for name, loc in worlds_data[World.UnderWorld]["locations"].items():
            if loc["button"] == button[0]:
                return name
        for name, data in self.placed_items.items():
            if data["image"] == button[0]:
                return name

    def select_location(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return
        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)
        print("Selected location:", loc_name)
        self.currently_selected = loc_name
        self.canvas.itemconfigure(item, fill="orange")

        # Show the sprite sheet
        show_sprites(self)

        # Hide the circle
        placed_item = self.placed_items[loc_name]["name"]
        self.canvas.itemconfigure(item, state="hidden")

        # Place a new sprite
        sprite_y, sprite_x = item_sprite_data.item_table[placed_item]
        self.placed_items[loc_name]["sprite"] = ImageTk.PhotoImage(
            ImageOps.expand(
                Image.open("source\\gui\\customizer\\Item_Sheet.png").crop(
                    (sprite_x * 16, sprite_y * 16, sprite_x * 16 + 16, sprite_y * 16 + 16)
                ),
                1,
                "#fff",
            )
        )
        self.placed_items[loc_name]["image"] = self.canvas.create_image(
            worlds_data[World.UnderWorld]["locations"][loc_name]["x"] + BORDER_SIZE,
            worlds_data[World.UnderWorld]["locations"][loc_name]["y"] + BORDER_SIZE,
            image=self.placed_items[loc_name]["sprite"],
        )
        self.canvas.tag_bind(
            self.placed_items[loc_name]["image"],
            "<Button-3>",
            lambda event: remove_item(self, event),
        )

    def remove_item(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return
        loc_name = get_loc_by_button(self, item)
        self.canvas.itemconfigure(item, state="hidden")
        loc_ref = worlds_data[World.UnderWorld]["locations"][loc_name]["button"]
        self.canvas.itemconfigure((loc_ref,), state="normal", fill="#0f0")
        del self.placed_items[loc_name]["image"]
        del self.placed_items[loc_name]["sprite"]

    def print_all_items(placed_items):
        # TODO: Implement
        bp = {"placements": {1: {}}}
        for loc_name, item_data in placed_items.items():
            bp["placements"][1][loc_name] = item_data["name"]

        print(yaml.dump(bp))

    # TODO: Refactor this out, will be reused in other places
    def show_sprites(self):
        def select_sprite(parent, self, event):
            item = self.canvas.find_closest(event.x, event.y)
            if item in [w["canvas_image"] for w in worlds_data.values()]:
                return
            item_name = get_sprite_by_button(self, item)
            parent.placed_items[parent.currently_selected] = {"name": item_name, "sprite": None}
            print(f"Placed sprite: {item_name} at {parent.currently_selected}")
            self.destroy()

        def get_sprite_by_button(self, button):
            for name, loc in self.items.items():
                if loc == button[0]:
                    return name

        sprite_window = Toplevel(self)
        sprite_window.geometry(f"{288 + (BORDER_SIZE * 2)}x{256 + (BORDER_SIZE * 2)}")
        sprite_window.title("Sprites Window")
        sprite_window.focus_set()
        sprite_window.canvas = Canvas(
            sprite_window, width=288 + (BORDER_SIZE * 2), height=256 + (BORDER_SIZE * 2), background="black"
        )
        sprite_window.canvas.pack()
        sprite_window.spritesheet = ImageTk.PhotoImage(
            Image.open("source\\gui\\customizer\\Item_Sheet.png").resize((288, 256))
        )
        sprite_window.image = sprite_window.canvas.create_image(
            0 + BORDER_SIZE, 0 + BORDER_SIZE, anchor=NW, image=sprite_window.spritesheet
        )
        sprite_window.items = {}
        for item, coords in item_sprite_data.item_table.items():
            y, x = coords
            item_selector = sprite_window.canvas.create_rectangle(
                x * 32 + BORDER_SIZE,
                y * 32 + BORDER_SIZE,
                x * 32 + 33 + BORDER_SIZE,
                y * 32 + 33 + BORDER_SIZE,
                outline="",
            )
            sprite_window.items[item] = item_selector
            sprite_window.canvas.tag_bind(
                item_selector,
                "<Button-1>",
                lambda event: select_sprite(self, sprite_window, event),
            )
        sprite_window.wait_window(sprite_window)

    # Custom Item Pool
    self = ttk.Frame(parent)
    self.cwidth = 1024
    self.cheight = 512
    self.select_state = SelectState.NoneSelected
    self.placed_items = {}
    self.canvas = Canvas(self, width=self.cwidth + (BORDER_SIZE * 2), height=self.cheight + (BORDER_SIZE * 2))
    self.canvas.pack()

    # Load in the world images
    worlds_data[World.UnderWorld]["map_image"] = ImageTk.PhotoImage(
        Image.open("source\\gui\\customizer\\Items\\Underworld_Items_Trimmed_512.png")
    )
    worlds_data[World.UnderWorld]["canvas_image"] = (
        self.canvas.create_image(BORDER_SIZE, BORDER_SIZE, anchor=NW, image=worlds_data[World.UnderWorld]["map_image"]),
    )

    # Display locations (and map?)
    for name, loc in worlds_data[World.UnderWorld]["locations"].items():
        worlds_data[World.UnderWorld]["locations"][name]["x"] *= 2
        worlds_data[World.UnderWorld]["locations"][name]["y"] *= 2

    display_world_locations(self, World.UnderWorld)

    connections_button = ttk.Button(self, text="List Items", command=lambda: print_all_items(self.placed_items))
    connections_button.pack()

    # TODO: Add a new button to store this info somwhere as JSON for the generation
    return self
