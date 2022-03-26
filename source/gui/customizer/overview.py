from cgitb import text
from enum import Enum
from tkinter import ttk, Frame, N, E, W, NW, LEFT, X, VERTICAL, Y, Canvas, Button
from PIL import ImageTk, Image
import source.gui.widgets as widgets
import json
import os

import source.classes.constants as CONST

# TODO: Refactor locations list into dict with names from actual randomizer
# TODO: Fix coordinates between worlds

# TODO: Do I add underworld? This will be needed for decoupled shuffles
worlds_data = {
    "light_world": {
        "locations": [
            {"x": 279.5, "y": 353.5, "name": "Links House"},
            {"x": 37.5, "y": 407.5, "name": "Desert Palace Entrance (South)"},
            {"x": 17.5, "y": 407.0, "name": "Desert Palace Entrance (West)"},
            {"x": 37.5, "y": 393.0, "name": "Desert Palace Entrance (North)"},
            {"x": 57.5, "y": 407.5, "name": "Desert Palace Entrance (East)"},
            {"x": 491.0, "y": 200.0, "name": "Eastern Palace"},
            {"x": 286.5, "y": 17.0, "name": "Tower of Hera"},
            {"x": 255.5, "y": 224.5, "name": "Hyrule Castle Entrance (South)"},
            {"x": 229.5, "y": 198.5, "name": "Hyrule Castle Entrance (West)"},
            {"x": 282.0, "y": 199.0, "name": "Hyrule Castle Entrance (East)"},
            {"x": 255.5, "y": 205.0, "name": "Agahnims Tower"},
            {
                "x": 281.5,
                "y": 220.0,
                "name": "Hyrule Castle Secret Entrance Stairs",
            },
            {"x": 24.0, "y": 218.5, "name": "Kakariko Well Cave"},
            {"x": 161.5, "y": 284.0, "name": "Bat Cave Cave"},
            {"x": 86.0, "y": 215.0, "name": "Elder House (East)"},
            {"x": 77.5, "y": 215.0, "name": "Elder House (West)"},
            {"x": 342.0, "y": 140.5, "name": "North Fairy Cave"},
            {"x": 93.5, "y": 77.5, "name": "Lost Woods Hideout Stump"},
            {"x": 169.5, "y": 16.5, "name": "Lumberjack Tree Cave"},
            {"x": 71.5, "y": 368.0, "name": "Two Brothers House (East)"},
            {"x": 55.5, "y": 368.0, "name": "Two Brothers House (West)"},
            {"x": 235.5, "y": 136.5, "name": "Sanctuary"},
            {"x": 181.5, "y": 90.0, "name": "Old Man Cave (West)"},
            {"x": 207.5, "y": 96.0, "name": "Old Man Cave (East)"},
            {"x": 229.5, "y": 120.0, "name": "Old Man House (Bottom)"},
            {"x": 273.5, "y": 82.5, "name": "Old Man House (Top)"},
            {"x": 201.5, "y": 70.0, "name": "Death Mountain Return Cave (East)"},
            {"x": 183.5, "y": 78.0, "name": "Death Mountain Return Cave (West)"},
            {"x": 249.5, "y": 52.0, "name": "Spectacle Rock Cave Peak"},
            {"x": 249.5, "y": 74.0, "name": "Spectacle Rock Cave"},
            {"x": 233.5, "y": 70.0, "name": "Spectacle Rock Cave (Bottom)"},
            {"x": 441.5, "y": 110.5, "name": "Paradox Cave (Bottom)"},
            {"x": 438.0, "y": 74.5, "name": "Paradox Cave (Middle)"},
            {"x": 439.5, "y": 32.5, "name": "Paradox Cave (Top)"},
            {"x": 419.5, "y": 70.0, "name": "Fairy Ascension Cave (Bottom)"},
            {"x": 419.5, "y": 58.5, "name": "Fairy Ascension Cave (Top)"},
            {"x": 407.5, "y": 46.0, "name": "Spiral Cave"},
            {"x": 410.0, "y": 66.5, "name": "Spiral Cave (Bottom)"},
            {"x": 460.5, "y": 69.5, "name": "Waterfall of Wishing"},
            {"x": 240.0, "y": 480.0, "name": "Dam"},
            {"x": 65.5, "y": 214.5, "name": "Blinds Hideout"},
            {"x": 304.5, "y": 213.0, "name": "Hyrule Castle Secret Entrance Drop"},
            {"x": 241.5, "y": 334.0, "name": "Bonk Fairy (Light)"},
            {"x": 421.5, "y": 330.5, "name": "Lake Hylia Fairy"},
            {"x": 305.5, "y": 399.0, "name": "Light Hype Fairy"},
            {"x": 141.5, "y": 456.5, "name": "Desert Fairy"},
            {"x": 307.5, "y": 151.5, "name": "Kings Grave"},
            {"x": 81.5, "y": 289.5, "name": "Tavern North"},
            {"x": 49.5, "y": 277.0, "name": "Chicken House"},
            {"x": 101.5, "y": 422.0, "name": "Aginahs Cave"},
            {"x": 414.5, "y": 232.5, "name": "Sahasrahlas Hut"},
            {"x": 371.5, "y": 393.0, "name": "Cave Shop (Lake Hylia)"},
            {"x": 405.5, "y": 436.5, "name": "Capacity Upgrade"},
            {"x": 11.5, "y": 218.0, "name": "Kakariko Well Drop"},
            {"x": 155.5, "y": 273.0, "name": "Blacksmiths Hut"},
            {"x": 165.5, "y": 288.0, "name": "Bat Cave Drop"},
            {"x": 79.5, "y": 275.5, "name": "Sick Kids House"},
            {"x": 328.5, "y": 159.0, "name": "North Fairy Cave Drop"},
            {"x": 94.5, "y": 8.0, "name": "Lost Woods Gamble"},
            {"x": 95.5, "y": 166.0, "name": "Fortune Teller (Light)"},
            {"x": 105.5, "y": 247.5, "name": "Snitch Lady (East)"},
            {"x": 25.5, "y": 239.5, "name": "Snitch Lady (West)"},
            {"x": 103.5, "y": 273.5, "name": "Bush Covered House"},
            {"x": 81.5, "y": 305.5, "name": "Tavern (Front)"},
            {"x": 13.5, "y": 305.0, "name": "Light World Bomb Hut"},
            {"x": 56.0, "y": 299.5, "name": "Kakariko Shop"},
            {"x": 96.5, "y": 67.0, "name": "Lost Woods Hideout Drop"},
            {"x": 153.5, "y": 38.0, "name": "Lumberjack Tree Tree"},
            {"x": 136.0, "y": 423.0, "name": "Cave 45"},
            {"x": 292.0, "y": 141.0, "name": "Graveyard Cave"},
            {"x": 89.5, "y": 398.5, "name": "Checkerboard Cave"},
            {"x": 333.5, "y": 481.0, "name": "Mini Moldorm Cave"},
            {"x": 501.5, "y": 358.5, "name": "Long Fairy Cave"},
            {"x": 467.5, "y": 395.0, "name": "Good Bee Cave"},
            {"x": 462.0, "y": 402.5, "name": "20 Rupee Cave"},
            {"x": 159.5, "y": 490.5, "name": "50 Rupee Cave"},
            {"x": 457.5, "y": 395.0, "name": "Ice Rod Cave"},
            {"x": 199.5, "y": 150.0, "name": "Bonk Rock Cave"},
            {"x": 79.5, "y": 338.0, "name": "Library"},
            {"x": 409.5, "y": 172.0, "name": "Potion Shop"},
            {"x": 265.5, "y": 150.0, "name": "Sanctuary Grave"},
            {"x": 431.5, "y": 74.5, "name": "Hookshot Fairy"},
            {"x": 431.5, "y": 46.5, "name": "Mimic Cave"},
            {"x": 171.5, "y": 31.5, "name": "Lumberjack House"},
            {"x": 332.0, "y": 411.5, "name": "Lake Hylia Fortune Teller"},
            {"x": 109.5, "y": 359.5, "name": "Kakariko Gamble Game"},
        ],
        "map_image": None,
        "canvas_image": None,
    },
    "dark_world": {
        "locations": [
            {"x": 63.5, "y": 248.5, "name": "Thieves Town"},
            {"x": 93.5, "y": 76.0, "name": "Skull Woods First Section Door"},
            {
                "x": 74.0,
                "y": 75.0,
                "name": "Skull Woods Second Section Door (East)",
            },
            {
                "x": 29.5,
                "y": 67.0,
                "name": "Skull Woods Second Section Door (West)",
            },
            {"x": 19.5, "y": 26.0, "name": "Skull Woods Final Section"},
            {"x": 407.5, "y": 442.0, "name": "Ice Palace"},
            {"x": 37.5, "y": 412.0, "name": "Misery Mire"},
            {"x": 491.0, "y": 202.0, "name": "Palace of Darkness"},
            {"x": 240.0, "y": 480.0, "name": "Swamp Palace"},
            {"x": 481.5, "y": 41.5, "name": "Turtle Rock"},
            {"x": 408.0, "y": 47.0, "name": "Dark Death Mountain Ledge (West)"},
            {"x": 432.0, "y": 47.0, "name": "Dark Death Mountain Ledge (East)"},
            {"x": 419.5, "y": 59.5, "name": "Turtle Rock Isolated Ledge Entrance"},
            {"x": 181.5, "y": 90.5, "name": "Bumper Cave (Bottom)"},
            {"x": 183.5, "y": 79.0, "name": "Bumper Cave (Top)"},
            {"x": 440.0, "y": 32.5, "name": "Superbunny Cave (Top)"},
            {"x": 431.5, "y": 74.5, "name": "Superbunny Cave (Bottom)"},
            {"x": 425.5, "y": 34.5, "name": "Hookshot Cave"},
            {"x": 409.5, "y": 8.0, "name": "Hookshot Cave Back Entrance"},
            {"x": 287.5, "y": 10.0, "name": "Ganons Tower"},
            {"x": 221.5, "y": 249.5, "name": "Pyramid Entrance"},
            {"x": 79.5, "y": 90.5, "name": "Skull Woods First Section Hole (West)"},
            {
                "x": 100.0,
                "y": 86.5,
                "name": "Skull Woods First Section Hole (East)",
            },
            {
                "x": 96.5,
                "y": 66.5,
                "name": "Skull Woods First Section Hole (North)",
            },
            {"x": 61.5, "y": 46.0, "name": "Skull Woods Second Section Hole"},
            {"x": 254.5, "y": 209.0, "name": "Pyramid Hole"},
            {"x": 239.5, "y": 249.5, "name": "Pyramid Fairy"},
            {"x": 502.0, "y": 359.0, "name": "East Dark World Hint"},
            {"x": 434.5, "y": 257.5, "name": "Palace of Darkness Hint"},
            {"x": 422.0, "y": 331.0, "name": "Dark Lake Hylia Fairy"},
            {"x": 458.0, "y": 395.0, "name": "Dark Lake Hylia Ledge Fairy"},
            {"x": 461.5, "y": 402.5, "name": "Dark Lake Hylia Ledge Spike Cave"},
            {"x": 467.5, "y": 395.0, "name": "Dark Lake Hylia Ledge Hint"},
            {"x": 305.5, "y": 399.0, "name": "Hype Cave"},
            {"x": 241.5, "y": 334.5, "name": "Bonk Fairy (Dark)"},
            {"x": 55.5, "y": 299.5, "name": "Brewery"},
            {"x": 106.0, "y": 247.5, "name": "C-Shaped House"},
            {"x": 25.5, "y": 239.0, "name": "Chest Game"},
            {"x": 161.5, "y": 310.0, "name": "Dark World Hammer Peg Cave"},
            {"x": 169.5, "y": 236.0, "name": "Red Shield Shop"},
            {"x": 235.5, "y": 141.0, "name": "Dark Sanctuary Hint"},
            {"x": 96.0, "y": 166.0, "name": "Fortune Teller (Dark)"},
            {"x": 103.5, "y": 273.0, "name": "Dark World Shop"},
            {"x": 171.5, "y": 29.5, "name": "Dark World Lumberjack Shop"},
            {"x": 411.5, "y": 173.0, "name": "Dark World Potion Shop"},
            {"x": 109.5, "y": 359.5, "name": "Archery Game"},
            {"x": 19.5, "y": 411.0, "name": "Mire Shed"},
        ],
        "map_image": None,
        "canvas_image": None,
    },
}


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


def customizer_page(top, parent):
    def change_world(self):
        # This should probably be an enum
        if self.current_world == "light_world":
            self.old_world = self.current_world
            self.current_world = "dark_world"
        else:
            self.current_world = "light_world"
            self.old_world = "dark_world"

        img = worlds_data[self.current_world]["map_image"]

        # Display only the current world, create if needed
        if worlds_data[self.current_world]["canvas_image"]:
            canvas.itemconfigure(
                worlds_data[self.current_world]["canvas_image"], state="normal"
            )
            canvas.itemconfigure(
                worlds_data[self.old_world]["canvas_image"], state="hidden"
            )
        else:
            worlds_data[self.current_world]["canvas_image"] = (
                canvas.create_image(20, 20, anchor=NW, image=img),
            )

        # Hide the old world's locations
        for loc in worlds_data[self.old_world]["locations"]:
            if "button" in loc:
                location_oval = loc["button"]
                canvas.itemconfigure((location_oval,), state="hidden")

        # Create or show the current world's locations
        for loc in worlds_data[self.current_world]["locations"]:
            if "target" in loc:
                fill_col = "blue"
            else:
                fill_col = "#0f0"
            if "button" not in loc:
                # TODO: Change the border to a variable, no magic numbers
                location_oval = canvas.create_oval(
                    loc["x"] + 15,
                    loc["y"] + 15,
                    loc["x"] + 25,
                    loc["y"] + 25,
                    fill=fill_col,
                )
                loc["button"] = location_oval
            else:
                location_oval = loc["button"]
                canvas.itemconfigure((location_oval,), state="normal")
            canvas.tag_bind(
                location_oval,
                "<Button-1>",
                lambda event: select_location(self, event),
            )

    def select_location(self, event):
        item = canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [
            worlds_data[self.current_world]["canvas_image"],
            worlds_data[self.old_world]["canvas_image"],
        ]:
            return

        # TODO: Check for dropdowns, maybe grey out incompatible targets for a source?

        # TODO: Store relation between target and source to display as a line
        # TODO: Use aformentioned relation to remove links with right click
        if self.select_state == SelectState.NoneSelected:
            canvas.itemconfigure(item, fill="orange")
            self.select_state = SelectState.SourceSelected
            self.source_location = item
        elif self.select_state == SelectState.SourceSelected:
            canvas.itemconfigure(self.source_location, fill="blue")
            canvas.itemconfigure(item, fill="blue")
            self.select_state = SelectState.NoneSelected

    # Custom Item Pool
    self = ttk.Frame(parent)
    self.current_world = "dark_world"
    self.select_state = SelectState.NoneSelected
    canvas = Canvas(self, width=552, height=552)
    canvas.pack()
    worlds_data["light_world"]["map_image"] = ImageTk.PhotoImage(
        Image.open("source\gui\customizer\lightworld512.png")
    )
    worlds_data["dark_world"]["map_image"] = ImageTk.PhotoImage(
        Image.open("source\gui\customizer\darkworld512.png")
    )

    change_world(self)
    # Create a button below the image to change the world
    world_button = ttk.Button(
        self, text="Change World", command=lambda: change_world(self)
    )
    world_button.pack()

    # TODO: Add a new button to show all links - How to show both worlds?
    # TODO: Add a new button to store this info somwhere as JSON for the generation

    return self
