from enum import Enum
from tkinter import ttk, NW, Canvas, LAST
from PIL import ImageTk, Image
import source.gui.customizer.location_data as location_data
from source.overworld.EntranceShuffle2 import entrance_map, default_connections, drop_map, single_entrance_map
import yaml

# TODO: Do I add underworld? This will be needed for decoupled shuffles


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


class World(Enum):
    LightWorld = 0
    DarkWorld = 1
    UnderWorld = 2


BORDER_SIZE = 20


def entrance_customizer_page(top, parent):

    boilerplate = {
        "meta": {"players": 1, "algorithm": "balanced", "seed": 42, "names": "Lonk"},
        "settings": {
            1: {
                "door_shuffle": "basic",
                "dropshuffle": True,
                "experimental": True,
                "goal": "ganon",
                "hints": True,
                "intensity": 3,
                "overworld_map": "compass",
                "pseudoboots": True,
                "pottery": "keys",
                "shopsanity": True,
                "shuffle": "crossed",
                "shufflelinks": True,
            }
        },
        "entrances": {
            1: {},
        },
    }

    worlds_data = {
        World.LightWorld: {
            "locations": location_data.lightworld_coordinates,
            "map_image": None,
            "canvas_image": None,
        },
        World.DarkWorld: {
            "locations": location_data.darkworld_coordinates,
            "map_image": None,
            "canvas_image": None,
        },
        World.UnderWorld: {
            "locations": {},
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

    # def change_world(self):
    # if self.current_world == 'Underworld':
    #     self.old_world = self.current_world
    #     self.current_world = 'Overworld'
    # else:
    #     self.old_world = World.DarkWorld
    #     self.current_world = World.LightWorld

    # # Display only the current world, create if needed, hide the old world if it exists
    # if not sidebyside:
    #     if worlds_data[self.old_world]["canvas_image"]:
    #         self.canvas.itemconfigure(worlds_data[self.old_world]["canvas_image"], state="hidden")
    #     if worlds_data[self.current_world]["canvas_image"]:
    #         self.canvas.itemconfigure(worlds_data[self.current_world]["canvas_image"], state="normal")
    #     else:
    #         worlds_data[self.current_world]["canvas_image"] = (
    #             self.canvas.create_image(
    #                 BORDER_SIZE, BORDER_SIZE, anchor=NW, image=worlds_data[self.current_world]["map_image"]
    #             ),
    #         )
    # # Hide the old world's locations
    # if not sidebyside:
    #     for name, loc in worlds_data[self.old_world]["locations"].items():
    #         if "button" in loc:
    #             location_oval = loc["button"]
    #             self.canvas.itemconfigure((location_oval,), state="hidden")

    #     self.displayed_connections = hide_all_connections(self)

    # # Create or show the current world's locations
    # worlds_to_show = [self.current_world] if not sidebyside else [World.LightWorld, World.DarkWorld]

    def get_loc_by_button(self, button):
        for name, loc in (
            {**worlds_data[World.LightWorld]["locations"], **worlds_data[World.DarkWorld]["locations"]}
        ).items():
            if loc["button"] == button[0]:
                return name

    def get_location_world(loc_name):
        if loc_name in worlds_data[World.LightWorld]["locations"]:
            return World.LightWorld
        elif loc_name in worlds_data[World.DarkWorld]["locations"]:
            return World.DarkWorld
        else:
            return World.UnderWorld

    def get_existing_connection(self, location):
        for source, target in self.defined_connections.items():
            if target == location:
                source_world = get_location_world(source)
                target_world = get_location_world(target)
                return source, source_world, target, target_world
        return None, None, None, None

    def hide_all_connections(self):
        for source, connection in self.displayed_connections.items():
            self.canvas.itemconfigure(connection, state="hidden")
        self.displayed_connections = {}

    def show_all_connections(self):
        hide_all_connections(self)
        for source, target in self.defined_connections.items():
            draw_connection(self, target)

    def has_source(self, loc_name):
        return loc_name in self.defined_connections

    def has_target(self, loc_name):
        return loc_name in self.defined_connections.values()

    def is_dropdown(loc_name):
        return True if loc_name in drop_map else False

    def mask_locations(self, entrance_type):
        masked = []
        for name, loc in (
            {**worlds_data[World.LightWorld]["locations"], **worlds_data[World.DarkWorld]["locations"]}
        ).items():
            if is_dropdown(name) and entrance_type == "Dropdown":
                self.canvas.itemconfigure(loc["button"], fill="#888", state="disabled")
                masked.append(name)
            elif not is_dropdown(name) and entrance_type == "Regular":
                self.canvas.itemconfigure(loc["button"], fill="#888", state="disabled")
                masked.append(name)
        return masked

    def unmask_locations(self):
        if not self.masked_locations:
            return
        for name in self.masked_locations:
            loc = worlds_data[get_location_world(name)]["locations"][name]
            if name not in self.defined_connections and name not in self.defined_connections.values():
                self.canvas.itemconfigure(loc["button"], fill="#0f0", state="normal")
            else:
                self.canvas.itemconfigure(loc["button"], fill="#00f", state="normal")
        self.masked_locations = []

    def select_location(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [w["canvas_image"] for w in worlds_data.values()] or item[0] in self.displayed_connections.values():
            return

        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)

        if self.select_state == SelectState.NoneSelected:
            if has_source(self, loc_name):
                return
            self.masked_locations = mask_locations(self, "Dropdown" if not is_dropdown(loc_name) else "Regular")
            self.canvas.itemconfigure(item, fill="orange")
            self.select_state = SelectState.SourceSelected
            self.source_location = item
        elif self.select_state == SelectState.SourceSelected:
            if has_target(self, loc_name):
                return
            unmask_locations(self)
            self.canvas.itemconfigure(self.source_location, fill="blue")
            self.canvas.itemconfigure(item, fill="blue")
            self.defined_connections[get_loc_by_button(self, self.source_location)] = loc_name
            draw_connection(self, loc_name)
            self.select_state = SelectState.NoneSelected

    def remove_connection(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return
        idx = list(self.displayed_connections.values()).index(item[0])
        current_source, current_target = list(self.displayed_connections.keys())[idx]

        source_world = (
            World.LightWorld if current_source in worlds_data[World.LightWorld]["locations"] else World.DarkWorld
        )
        target_world = (
            World.LightWorld if current_target in worlds_data[World.LightWorld]["locations"] else World.DarkWorld
        )

        del self.defined_connections[current_source]
        del self.displayed_connections[(current_source, current_target)]
        if current_source not in self.defined_connections.values():
            self.canvas.itemconfigure(worlds_data[source_world]["locations"][current_source]["button"], fill="#0f0")
        if current_target not in self.defined_connections:
            self.canvas.itemconfigure(worlds_data[target_world]["locations"][current_target]["button"], fill="#0f0")
        self.canvas.itemconfigure(item, state="hidden")

    def draw_connection(self, loc_name):
        current_source, source_world, current_target, target_world = get_existing_connection(self, loc_name)

        if current_source == current_target:
            connection_line = self.canvas.create_oval(
                worlds_data[source_world]["locations"][current_source]["x"] + BORDER_SIZE - 3,
                worlds_data[source_world]["locations"][current_source]["y"] + BORDER_SIZE - 3,
                worlds_data[source_world]["locations"][current_source]["x"] + BORDER_SIZE + 3,
                worlds_data[source_world]["locations"][current_source]["y"] + BORDER_SIZE + 3,
                fill="red",
            )
        else:
            connection_line = self.canvas.create_line(
                worlds_data[source_world]["locations"][current_source]["x"] + BORDER_SIZE,
                worlds_data[source_world]["locations"][current_source]["y"] + BORDER_SIZE,
                worlds_data[target_world]["locations"][current_target]["x"] + BORDER_SIZE,
                worlds_data[target_world]["locations"][current_target]["y"] + BORDER_SIZE,
                fill="red",
                arrow=LAST,
                dash=(4, 4) if source_world != target_world else None,
            )
        self.canvas.tag_bind(
            connection_line,
            "<Button-3>",
            lambda event: remove_connection(self, event),
        )

        # TODO: Make this a tuple of course and target
        self.displayed_connections[(current_source, current_target)] = connection_line

    def print_all_connections(defined_connections):
        print_connections = {"entrances": {}, "exits": {}, "two-way": {}}
        for source, target in defined_connections.items():
            print(source, target)
            if source in single_entrance_map:
                print_connections["entrances"][target] = single_entrance_map[source]
            if target in entrance_map:
                print_connections["two-way"][source] = entrance_map[target]
                if target == "Links House":
                    print_connections["exits"][source] = "Chris Houlihan Room Exit"
            elif target in default_connections and default_connections[target] != target and not is_dropdown(source):
                print_connections["two-way"][source] = default_connections[target]
            elif is_dropdown(target):
                print_connections["entrances"][source] = default_connections[target]
            else:
                print(f"Error finding entrance {source} -> {target}")
                print_connections["entrances"][target] = source

        bp = boilerplate.copy()
        bp["entrances"][1] = print_connections
        print(yaml.dump(bp))

    # Custom Item Pool
    self = ttk.Frame(parent)
    self.cwidth = 512
    self.cheight = 512
    self.select_state = SelectState.NoneSelected
    self.defined_connections = {}
    self.displayed_connections = {}
    self.canvas = Canvas(self, width=self.cwidth * 2 + (BORDER_SIZE * 2), height=self.cheight + (BORDER_SIZE * 2))
    self.canvas.pack()

    # Load in the world images
    worlds_data[World.LightWorld]["map_image"] = ImageTk.PhotoImage(
        Image.open("source\gui\customizer\Entrances\lightworld512.png")
    )
    worlds_data[World.DarkWorld]["map_image"] = ImageTk.PhotoImage(
        Image.open("source\gui\customizer\Entrances\darkworld512.png")
    )

    worlds_data[World.LightWorld]["canvas_image"] = (
        self.canvas.create_image(BORDER_SIZE, BORDER_SIZE, anchor=NW, image=worlds_data[World.LightWorld]["map_image"]),
    )

    worlds_data[World.DarkWorld]["canvas_image"] = (
        self.canvas.create_image(
            BORDER_SIZE + 512, BORDER_SIZE, anchor=NW, image=worlds_data[World.DarkWorld]["map_image"]
        ),
    )

    # Offset darkworld locations
    for name, loc in worlds_data[World.DarkWorld]["locations"].items():
        worlds_data[World.DarkWorld]["locations"][name]["x"] += self.cwidth

    # Display locations (and map?)
    for world in [World.LightWorld, World.DarkWorld]:
        display_world_locations(self, world)

    # change_world(self)
    # Create a button below the image to change the world
    # world_button = ttk.Button(self, text="Change World", command=lambda: change_world(self))
    # world_button.pack()

    connections_button = ttk.Button(
        self, text="List Connections", command=lambda: print_all_connections(self.defined_connections)
    )
    connections_button.pack()
    hide_connections_button = ttk.Button(self, text="Hide All Connections", command=lambda: hide_all_connections(self))
    hide_connections_button.pack()
    show_connections_button = ttk.Button(self, text="Show All Connections", command=lambda: show_all_connections(self))
    show_connections_button.pack()

    # TODO: Add a new button to store this info somwhere as JSON for the generation
    return self
