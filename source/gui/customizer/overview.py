from cgitb import text
from enum import Enum
from tkinter import ttk, Frame, N, E, W, NW, LEFT, X, VERTICAL, Y, Canvas, Button
from turtle import color
from PIL import ImageTk, Image
import source.gui.widgets as widgets
import EntranceShuffle
import json
import os

import source.classes.constants as CONST

# TODO: Fix coordinates between worlds

# TODO: Do I add underworld? This will be needed for decoupled shuffles


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


class World(Enum):
    LightWorld = 0
    DarkWorld = 1


BORDER_SIZE = 20


def customizer_page(top, parent):

    boilerplate = {"meta": {"players": 1}}

    worlds_data = {
        World.LightWorld: {
            "locations": {
                "Links House": {"x": 279.5, "y": 353.5},
                "Desert Palace Entrance (South)": {"x": 37.5, "y": 407.5},
                "Desert Palace Entrance (West)": {"x": 17.5, "y": 407.0},
                "Desert Palace Entrance (North)": {"x": 37.5, "y": 393.0},
                "Desert Palace Entrance (East)": {"x": 57.5, "y": 407.5},
                "Eastern Palace": {"x": 491.0, "y": 200.0},
                "Tower of Hera": {"x": 286.5, "y": 17.0},
                "Hyrule Castle Entrance (South)": {"x": 255.5, "y": 224.5},
                "Hyrule Castle Entrance (West)": {"x": 229.5, "y": 198.5},
                "Hyrule Castle Entrance (East)": {"x": 282.0, "y": 199.0},
                "Agahnims Tower": {"x": 255.5, "y": 205.0},
                "Hyrule Castle Secret Entrance Stairs": {"x": 281.5, "y": 220.0},
                "Kakariko Well Cave": {"x": 24.0, "y": 218.5},
                "Bat Cave Cave": {"x": 161.5, "y": 284.0},
                "Elder House (East)": {"x": 86.0, "y": 215.0},
                "Elder House (West)": {"x": 77.5, "y": 215.0},
                "North Fairy Cave": {"x": 342.0, "y": 140.5},
                "Lost Woods Hideout Stump": {"x": 93.5, "y": 77.5},
                "Lumberjack Tree Cave": {"x": 169.5, "y": 16.5},
                "Two Brothers House (East)": {"x": 71.5, "y": 368.0},
                "Two Brothers House (West)": {"x": 55.5, "y": 368.0},
                "Sanctuary": {"x": 235.5, "y": 136.5},
                "Old Man Cave (West)": {"x": 181.5, "y": 90.0},
                "Old Man Cave (East)": {"x": 207.5, "y": 96.0},
                "Old Man House (Bottom)": {"x": 229.5, "y": 120.0},
                "Old Man House (Top)": {"x": 273.5, "y": 82.5},
                "Death Mountain Return Cave (East)": {"x": 201.5, "y": 70.0},
                "Death Mountain Return Cave (West)": {"x": 183.5, "y": 78.0},
                "Spectacle Rock Cave Peak": {"x": 249.5, "y": 52.0},
                "Spectacle Rock Cave": {"x": 249.5, "y": 74.0},
                "Spectacle Rock Cave (Bottom)": {"x": 233.5, "y": 70.0},
                "Paradox Cave (Bottom)": {"x": 441.5, "y": 110.5},
                "Paradox Cave (Middle)": {"x": 438.0, "y": 74.5},
                "Paradox Cave (Top)": {"x": 439.5, "y": 32.5},
                "Fairy Ascension Cave (Bottom)": {"x": 419.5, "y": 70.0},
                "Fairy Ascension Cave (Top)": {"x": 419.5, "y": 58.5},
                "Spiral Cave": {"x": 407.5, "y": 46.0},
                "Spiral Cave (Bottom)": {"x": 410.0, "y": 66.5},
                "Waterfall of Wishing": {"x": 460.5, "y": 69.5},
                "Dam": {"x": 240.0, "y": 480.0},
                "Blinds Hideout": {"x": 65.5, "y": 214.5},
                "Hyrule Castle Secret Entrance Drop": {"x": 304.5, "y": 213.0},
                "Bonk Fairy (Light)": {"x": 241.5, "y": 334.0},
                "Lake Hylia Fairy": {"x": 421.5, "y": 330.5},
                "Light Hype Fairy": {"x": 305.5, "y": 399.0},
                "Desert Fairy": {"x": 141.5, "y": 456.5},
                "Kings Grave": {"x": 307.5, "y": 151.5},
                "Tavern North": {"x": 81.5, "y": 289.5},
                "Chicken House": {"x": 49.5, "y": 277.0},
                "Aginahs Cave": {"x": 101.5, "y": 422.0},
                "Sahasrahlas Hut": {"x": 414.5, "y": 232.5},
                "Cave Shop (Lake Hylia)": {"x": 371.5, "y": 393.0},
                "Capacity Upgrade": {"x": 405.5, "y": 436.5},
                "Kakariko Well Drop": {"x": 11.5, "y": 218.0},
                "Blacksmiths Hut": {"x": 155.5, "y": 273.0},
                "Bat Cave Drop": {"x": 165.5, "y": 288.0},
                "Sick Kids House": {"x": 79.5, "y": 275.5},
                "North Fairy Cave Drop": {"x": 328.5, "y": 159.0},
                "Lost Woods Gamble": {"x": 94.5, "y": 8.0},
                "Fortune Teller (Light)": {"x": 95.5, "y": 166.0},
                "Snitch Lady (East)": {"x": 105.5, "y": 247.5},
                "Snitch Lady (West)": {"x": 25.5, "y": 239.5},
                "Bush Covered House": {"x": 103.5, "y": 273.5},
                "Tavern (Front)": {"x": 81.5, "y": 305.5},
                "Light World Bomb Hut": {"x": 13.5, "y": 305.0},
                "Kakariko Shop": {"x": 56.0, "y": 299.5},
                "Lost Woods Hideout Drop": {"x": 96.5, "y": 67.0},
                "Lumberjack Tree Tree": {"x": 153.5, "y": 38.0},
                "Cave 45": {"x": 136.0, "y": 423.0},
                "Graveyard Cave": {"x": 292.0, "y": 141.0},
                "Checkerboard Cave": {"x": 89.5, "y": 398.5},
                "Mini Moldorm Cave": {"x": 333.5, "y": 481.0},
                "Long Fairy Cave": {"x": 501.5, "y": 358.5},
                "Good Bee Cave": {"x": 467.5, "y": 395.0},
                "20 Rupee Cave": {"x": 462.0, "y": 402.5},
                "50 Rupee Cave": {"x": 159.5, "y": 490.5},
                "Ice Rod Cave": {"x": 457.5, "y": 395.0},
                "Bonk Rock Cave": {"x": 199.5, "y": 150.0},
                "Library": {"x": 79.5, "y": 338.0},
                "Potion Shop": {"x": 409.5, "y": 172.0},
                "Sanctuary Grave": {"x": 265.5, "y": 150.0},
                "Hookshot Fairy": {"x": 431.5, "y": 74.5},
                "Mimic Cave": {"x": 431.5, "y": 46.5},
                "Lumberjack House": {"x": 171.5, "y": 31.5},
                "Lake Hylia Fortune Teller": {"x": 332.0, "y": 411.5},
                "Kakariko Gamble Game": {"x": 109.5, "y": 359.5},
            },
            "map_image": None,
            "canvas_image": None,
        },
        World.DarkWorld: {
            "locations": {
                "Thieves Town": {"x": 63.5, "y": 248.5},
                "Skull Woods First Section Door": {"x": 93.5, "y": 76.0},
                "Skull Woods Second Section Door (East)": {"x": 74.0, "y": 75.0},
                "Skull Woods Second Section Door (West)": {"x": 29.5, "y": 67.0},
                "Skull Woods Final Section": {"x": 19.5, "y": 26.0},
                "Ice Palace": {"x": 407.5, "y": 442.0},
                "Misery Mire": {"x": 37.5, "y": 412.0},
                "Palace of Darkness": {"x": 491.0, "y": 202.0},
                "Swamp Palace": {"x": 240.0, "y": 480.0},
                "Turtle Rock": {"x": 481.5, "y": 41.5},
                "Dark Death Mountain Ledge (West)": {"x": 408.0, "y": 47.0},
                "Dark Death Mountain Ledge (East)": {"x": 432.0, "y": 47.0},
                "Turtle Rock Isolated Ledge Entrance": {"x": 419.5, "y": 59.5},
                "Bumper Cave (Bottom)": {"x": 181.5, "y": 90.5},
                "Bumper Cave (Top)": {"x": 183.5, "y": 79.0},
                "Superbunny Cave (Top)": {"x": 440.0, "y": 32.5},
                "Superbunny Cave (Bottom)": {"x": 431.5, "y": 74.5},
                "Hookshot Cave": {"x": 425.5, "y": 34.5},
                "Hookshot Cave Back Entrance": {"x": 409.5, "y": 8.0},
                "Ganons Tower": {"x": 287.5, "y": 10.0},
                "Pyramid Entrance": {"x": 221.5, "y": 249.5},
                "Skull Woods First Section Hole (West)": {"x": 79.5, "y": 90.5},
                "Skull Woods First Section Hole (East)": {"x": 100.0, "y": 86.5},
                "Skull Woods First Section Hole (North)": {"x": 96.5, "y": 66.5},
                "Skull Woods Second Section Hole": {"x": 61.5, "y": 46.0},
                "Pyramid Hole": {"x": 254.5, "y": 209.0},
                "Pyramid Fairy": {"x": 239.5, "y": 249.5},
                "East Dark World Hint": {"x": 502.0, "y": 359.0},
                "Palace of Darkness Hint": {"x": 434.5, "y": 257.5},
                "Dark Lake Hylia Fairy": {"x": 422.0, "y": 331.0},
                "Dark Lake Hylia Ledge Fairy": {"x": 458.0, "y": 395.0},
                "Dark Lake Hylia Ledge Spike Cave": {"x": 461.5, "y": 402.5},
                "Dark Lake Hylia Ledge Hint": {"x": 467.5, "y": 395.0},
                "Hype Cave": {"x": 305.5, "y": 399.0},
                "Bonk Fairy (Dark)": {"x": 241.5, "y": 334.5},
                "Brewery": {"x": 55.5, "y": 299.5},
                "C-Shaped House": {"x": 106.0, "y": 247.5},
                "Chest Game": {"x": 25.5, "y": 239.0},
                "Dark World Hammer Peg Cave": {"x": 161.5, "y": 310.0},
                "Red Shield Shop": {"x": 169.5, "y": 236.0},
                "Dark Sanctuary Hint": {"x": 235.5, "y": 141.0},
                "Fortune Teller (Dark)": {"x": 96.0, "y": 166.0},
                "Dark World Shop": {"x": 103.5, "y": 273.0},
                "Dark World Lumberjack Shop": {"x": 171.5, "y": 29.5},
                "Dark World Potion Shop": {"x": 411.5, "y": 173.0},
                "Archery Game": {"x": 109.5, "y": 359.5},
                "Mire Shed": {"x": 19.5, "y": 411.0},
                "Dark Desert Hint": {"x": 101.5, "y": 423.0},
                "Dark Desert Fairy": {"x": 55.5, "y": 411.0},
                "Spike Cave": {"x": 293.5, "y": 74.5},
                "Cave Shop (Dark Death Mountain)": {"x": 438.0, "y": 74.5},
                "Dark Death Mountain Fairy": {"x": 207.5, "y": 96.5},
                "Big Bomb Shop": {"x": 279.5, "y": 353.5},
                "Dark Lake Hylia Shop": {"x": 331.5, "y": 411.0},
            },
            "map_image": None,
            "canvas_image": None,
        },
    }

    def change_world(self):
        if self.current_world == World.LightWorld:
            self.old_world = World.LightWorld
            self.current_world = World.DarkWorld
        else:
            self.old_world = World.DarkWorld
            self.current_world = World.LightWorld

        img = worlds_data[self.current_world]["map_image"]

        # Display only the current world, create if needed, hide the old world if it exists
        if worlds_data[self.old_world]["canvas_image"]:
            self.canvas.itemconfigure(worlds_data[self.old_world]["canvas_image"], state="hidden")
        if worlds_data[self.current_world]["canvas_image"]:
            self.canvas.itemconfigure(worlds_data[self.current_world]["canvas_image"], state="normal")
        else:
            worlds_data[self.current_world]["canvas_image"] = (
                self.canvas.create_image(BORDER_SIZE, BORDER_SIZE, anchor=NW, image=img),
            )

        # Hide the old world's locations
        for name, loc in worlds_data[self.old_world]["locations"].items():
            if "button" in loc:
                location_oval = loc["button"]
                self.canvas.itemconfigure((location_oval,), state="hidden")

        self.displayed_connections = hide_all_connections(self)

        # Create or show the current world's locations
        for name, loc in worlds_data[self.current_world]["locations"].items():
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
                worlds_data[self.current_world]["locations"][name]["button"] = location_oval
            else:
                location_oval = loc["button"]
                self.canvas.itemconfigure((location_oval,), state="normal")
            self.canvas.tag_bind(
                location_oval,
                "<Button-1>",
                lambda event: select_location(self, event),
            )
            self.canvas.tag_bind(
                location_oval,
                "<Button-3>",
                lambda event: select_location(self, event, remove_connection=True),
            )

    def get_loc_by_button(self, button):
        for name, loc in (
            worlds_data[World.LightWorld]["locations"] | worlds_data[World.DarkWorld]["locations"]
        ).items():
            if loc["button"] == button[0]:
                return name

    def get_existing_connection(self, location):
        for source in self.defined_connections:
            if source == location or self.defined_connections[source] == location:
                source_world = (
                    World.LightWorld if source in worlds_data[World.LightWorld]["locations"] else World.DarkWorld
                )
                target_world = (
                    World.LightWorld
                    if self.defined_connections[source] in worlds_data[World.LightWorld]["locations"]
                    else World.DarkWorld
                )
                return source, source_world, self.defined_connections[source], target_world
        return None, None, None, None

    def hide_all_connections(self):
        for source, connection in self.displayed_connections.items():
            self.canvas.itemconfigure(connection, state="hidden")
        return {}

    def select_location(self, event, remove_connection=False):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [
            worlds_data[self.current_world]["canvas_image"],
            worlds_data[self.old_world]["canvas_image"],
        ]:
            return

        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)
        current_source, source_world, current_target, target_world = get_existing_connection(self, loc_name)
        print(current_source, source_world, current_target, target_world)

        # If the location has a connection, draw it
        if current_source:
            if remove_connection:
                if current_source in self.displayed_connections:
                    self.canvas.itemconfigure(self.displayed_connections[current_source], state="hidden")
                    del self.displayed_connections[current_source]
                del self.defined_connections[current_source]
                self.canvas.itemconfigure(worlds_data[source_world]["locations"][current_source]["button"], fill="#0f0")
                self.canvas.itemconfigure(worlds_data[target_world]["locations"][current_target]["button"], fill="#0f0")

                return
            if current_source == current_target:
                connection_line = self.canvas.create_oval(
                    worlds_data[source_world]["locations"][current_source]["x"] + BORDER_SIZE - 3,
                    worlds_data[source_world]["locations"][current_source]["y"] + BORDER_SIZE - 3,
                    worlds_data[source_world]["locations"][current_source]["x"] + BORDER_SIZE + 3,
                    worlds_data[source_world]["locations"][current_source]["y"] + BORDER_SIZE + 3,
                    fill="red",
                    state="disabled",
                )
            else:
                connection_line = self.canvas.create_line(
                    worlds_data[source_world]["locations"][current_source]["x"] + BORDER_SIZE,
                    worlds_data[source_world]["locations"][current_source]["y"] + BORDER_SIZE,
                    worlds_data[target_world]["locations"][current_target]["x"] + BORDER_SIZE,
                    worlds_data[target_world]["locations"][current_target]["y"] + BORDER_SIZE,
                    fill="red",
                    state="disabled",
                    dash=(4, 4) if source_world != target_world else None,
                )

            self.displayed_connections[current_source] = connection_line
            return
        elif remove_connection:
            return

        # TODO: Check for dropdowns, maybe grey out incompatible targets for a source?

        if self.select_state == SelectState.NoneSelected:
            self.canvas.itemconfigure(item, fill="orange")
            self.select_state = SelectState.SourceSelected
            self.source_location = item
        elif self.select_state == SelectState.SourceSelected:
            self.canvas.itemconfigure(self.source_location, fill="blue")
            self.canvas.itemconfigure(item, fill="blue")
            self.defined_connections[get_loc_by_button(self, self.source_location)] = get_loc_by_button(self, item)
            self.select_state = SelectState.NoneSelected

    # Custom Item Pool
    self = ttk.Frame(parent)
    self.current_world = World.DarkWorld
    self.select_state = SelectState.NoneSelected
    self.defined_connections = {}
    self.displayed_connections = {}
    self.canvas = Canvas(self, width=552, height=552)
    self.canvas.pack()
    worlds_data[World.LightWorld]["map_image"] = ImageTk.PhotoImage(
        Image.open("source\gui\customizer\lightworld512.png")
    )
    worlds_data[World.DarkWorld]["map_image"] = ImageTk.PhotoImage(Image.open("source\gui\customizer\darkworld512.png"))

    change_world(self)
    # Create a button below the image to change the world
    world_button = ttk.Button(self, text="Change World", command=lambda: change_world(self))
    world_button.pack()

    # TODO: Add a new button to show all links - How to show both worlds?
    # TODO: Add a new button to store this info somwhere as JSON for the generation

    return self
