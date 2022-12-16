from enum import Enum
from tkinter import ttk, NW, Canvas, LAST
from PIL import ImageTk, Image
from source.overworld.EntranceShuffle2 import entrance_map, default_connections, drop_map, single_entrance_map
from source.gui.customizer.worlds_data import worlds_data, World
import source.gui.customizer.new_location_data as location_data

# TODO: Do I add underworld? This will be needed for decoupled shuffles


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


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

    def load_yaml(self, yaml_data):
        self.select_state = SelectState.NoneSelected
        for source, target in list(self.defined_connections.items()):
            if (source, target) in self.displayed_connections:
                self.canvas.itemconfig(self.displayed_connections[(source, target)], state="hidden")
                del self.displayed_connections[(source, target)]
            del self.defined_connections[source]

        for source, target in yaml_data.items():
            if target in single_entrance_map:
                target = single_entrance_map[target]
            else:
                for name, loc_map in {
                    "single_entrance_map": single_entrance_map,
                    "drop_map": drop_map,
                    "default_connections": default_connections,
                    "entrance_map": entrance_map,
                }.items():
                    if target in loc_map.values():
                        idx = list(loc_map.values()).index(target)
                        target = list(loc_map.keys())[idx]
            self.defined_connections[source] = target
            draw_connection(self, target)

    def display_world_locations(self, world):
        objects = self.canvas.find_all()
        for name, loc in worlds_data[world]["entrances"].items():
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
                worlds_data[world]["entrances"][name]["button"] = location_oval
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
                lambda event: show_chain_connection(self, event),
            )
            self.canvas.tag_bind(
                location_oval,
                "<Button-2>",
                lambda event: mark_location_complete(self, event),
            )

    def mark_location_complete(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return

        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)

        if loc_name in self.defined_connections.values() or loc_name in self.defined_connections.keys():
            return

        if loc_name in self.disabled_locations:
            self.canvas.itemconfigure(item, fill="#0f0")
            self.disabled_locations.remove(loc_name)
        else:
            self.canvas.itemconfigure(item, fill="grey")
            self.disabled_locations.add(loc_name)


    def get_loc_by_button(self, button):
        for name, loc in (
            {**worlds_data[World.LightWorld]["entrances"], **worlds_data[World.DarkWorld]["entrances"], **worlds_data[World.LightWorldInside]["entrances"], **worlds_data[World.DarkWorldInside]["entrances"]}
        ).items():
            if loc["button"] == button[0]:
                return name

    def get_location_world(loc_name):
        if loc_name in worlds_data[World.LightWorld]["entrances"]:
            return World.LightWorld
        elif loc_name in worlds_data[World.DarkWorld]["entrances"]:
            return World.DarkWorld
        elif loc_name in worlds_data[World.LightWorldInside]["entrances"]:
            return World.LightWorldInside
        elif loc_name in worlds_data[World.DarkWorldInside]["entrances"]:
            return World.DarkWorldInside
        else:
            return World.UnderWorld

    def get_existing_connection(self, location):
        for source, target in self.defined_connections.items():
            if target == location:
                source_world = get_location_world(source)
                target_world = get_location_world(target)
                return source, source_world, target, target_world
        for source, target in self.defined_connections.items():
            if source == location:
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
        return True if loc_name.endswith(' Inside') else False

    def mask_locations(self, entrance_type):
        masked = []
        for name, loc in (
            {**worlds_data[World.LightWorld]["entrances"], **worlds_data[World.DarkWorld]["entrances"], **worlds_data[World.LightWorldInside]["entrances"], **worlds_data[World.DarkWorldInside]["entrances"]}
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
            loc = worlds_data[get_location_world(name)]["entrances"][name]
            colour_node(self, name)
            self.canvas.itemconfigure(loc["button"], state="normal")

        self.masked_locations = []

    def select_location(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return

        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)

        if loc_name in self.disabled_locations:
            return

        if self.select_state == SelectState.NoneSelected:
            if has_source(self, loc_name):
                draw_connection(self, loc_name)
                draw_connection(self, self.defined_connections[loc_name])
                return
            self.masked_locations = mask_locations(self, "Regular" if not is_dropdown(loc_name) else "Dropdown")
            self.canvas.itemconfigure(item, fill="orange")
            self.select_state = SelectState.SourceSelected
            self.source_location = item
        elif self.select_state == SelectState.SourceSelected:
            if has_target(self, loc_name):
                return
            unmask_locations(self)

            self.defined_connections[get_loc_by_button(self, self.source_location)] = loc_name
            draw_connection(self, loc_name)
            self.select_state = SelectState.NoneSelected

    def remove_connection(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return
        idx = list(self.displayed_connections.values()).index(item[0])
        current_source, current_target = list(self.displayed_connections.keys())[idx]

        del self.defined_connections[current_source]
        del self.displayed_connections[(current_source, current_target)]
        colour_node(self, current_source)
        colour_node(self, current_target)
        self.canvas.itemconfigure(item, state="hidden")

    def colour_node(self, loc_name):
        if loc_name in self.disabled_locations:
            return
        current_source, source_world, current_target, target_world = get_existing_connection(self, loc_name)
        for node, world in [(current_source, source_world), (current_target, target_world)]:
            if node is None:
                self.canvas.itemconfigure(
                    worlds_data[get_location_world(loc_name)]["entrances"][loc_name]["button"], fill="#0f0"
                )
            elif node in self.defined_connections.values() and node in self.defined_connections.keys():
                self.canvas.itemconfigure(worlds_data[world]["entrances"][node]["button"], fill="#00f")
            elif node in self.defined_connections.values():
                self.canvas.itemconfigure(worlds_data[world]["entrances"][node]["button"], fill="#0ff")
            elif node in self.defined_connections.keys():
                self.canvas.itemconfigure(worlds_data[world]["entrances"][node]["button"], fill="#ff0")

    def draw_connection(self, loc_name):
        current_source, source_world, current_target, target_world = get_existing_connection(self, loc_name)
        if (current_source, current_target) in self.displayed_connections or current_source is None:
            return
        if current_source == current_target:
            connection_line = self.canvas.create_oval(
                worlds_data[source_world]["entrances"][current_source]["x"] + BORDER_SIZE - 3,
                worlds_data[source_world]["entrances"][current_source]["y"] + BORDER_SIZE - 3,
                worlds_data[source_world]["entrances"][current_source]["x"] + BORDER_SIZE + 3,
                worlds_data[source_world]["entrances"][current_source]["y"] + BORDER_SIZE + 3,
                fill="white",
            )
        else:
            connection_line = self.canvas.create_line(
                worlds_data[source_world]["entrances"][current_source]["x"] + BORDER_SIZE,
                worlds_data[source_world]["entrances"][current_source]["y"] + BORDER_SIZE,
                worlds_data[target_world]["entrances"][current_target]["x"] + BORDER_SIZE,
                worlds_data[target_world]["entrances"][current_target]["y"] + BORDER_SIZE,
                # fill='black' if source_world != target_world else 'white',
                fill='black' if source_world in [World.LightWorld, World.DarkWorld] else 'white',
                # fill="black",
                arrow=LAST,
                width=2,
                # dash=(4, 4) if source_world != target_world else None,
                activefill="black",
                activewidth=4,
                activedash=None,
            )
        self.canvas.tag_bind(
            connection_line,
            "<Button-3>",
            lambda event: remove_connection(self, event),
        )
        colour_node(self, loc_name)

        self.displayed_connections[(current_source, current_target)] = connection_line

    def return_connections(defined_connections):
        final_connections = {"entrances": {}, "exits": {}, "two-way": {}}
        er_type = 'vanilla'
        if len(defined_connections) == 0:
            return final_connections, False
        for source, target in defined_connections.items():
            if er_type != 'crossed':
                er_type = 'full'
                _, source_world, _, target_world = get_existing_connection(self, source)
                if source_world != target_world:
                    er_type = 'crossed'
            target = single_entrance_map[target] if target in single_entrance_map else target
            if source == "Tavern North" or target == "Tavern North":
                final_connections["entrances"]["Tavern North"] = "Tavern"
                continue
            if target in entrance_map:
                final_connections["two-way"][source] = entrance_map[target]
                # if target == "Links House":
                #     final_connections["exits"][source] = "Chris Houlihan Room Exit"
            elif target in default_connections and default_connections[target] != target and not is_dropdown(source):
                final_connections["two-way"][source] = default_connections[target]
            # elif is_dropdown(target):
                # final_connections["entrances"][source] = drop_map[target]
            else:
                final_connections["entrances"][source] = target
        if "Links House Exit" not in final_connections["two-way"].values():
            final_connections["two-way"]["Links House"] = "Links House Exit"
        if "Chris Houlihan Room Exit" not in final_connections["two-way"].values():
            final_connections["exits"]["Links House"] = "Chris Houlihan Room Exit"

        return final_connections, er_type

    def get_connection_chain(self, loc_name):
        # print("get_connection_chain", loc_name)
        locs_to_check = [loc_name]
        chain = []
        connectors_checked = set()
        while len(locs_to_check) > 0:
            # print("locs_to_check", locs_to_check)
            loc = locs_to_check.pop(0)
            if loc in chain:
                continue
            if loc in location_data.entrances_to_connectors and loc not in connectors_checked:
                connectors_checked.add(loc)
                for connector_loc in location_data.inside_connectors[location_data.entrances_to_connectors[loc]]:
                    connectors_checked.add(connector_loc)
                    locs_to_check.append(connector_loc)
            chain.append(loc)
            for k, v in self.defined_connections.items():
                if v == loc:
                    locs_to_check.append(k)
                if k == loc:
                    locs_to_check.append(v)
        return chain

    def show_chain_connection(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return

        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)


        # print("show_chain_connection", loc_name)
        hide_all_connections(self)
        chain = get_connection_chain(self, loc_name)
        # print("chain", chain)
        for i in chain:
            draw_connection(self, i)
   

        

    # Custom Item Pool
    self = ttk.Frame(parent)
    self.cwidth = 512
    self.cheight = 512
    self.select_state = SelectState.NoneSelected
    self.defined_connections = {}
    self.displayed_connections = {}
    self.disabled_locations = set()
    self.canvas = Canvas(self, width=self.cwidth * 2 + (BORDER_SIZE * 2), height=self.cheight * 2 + (BORDER_SIZE * 2))
    self.canvas.pack()

    # Load in the world images
    worlds_data[World.LightWorld]["map_image"] = ImageTk.PhotoImage(
        Image.open(worlds_data[World.LightWorld]["map_file"])
    )
    worlds_data[World.DarkWorld]["map_image"] = ImageTk.PhotoImage(Image.open(worlds_data[World.DarkWorld]["map_file"]))

    worlds_data[World.LightWorld]["canvas_image"] = (
        self.canvas.create_image(BORDER_SIZE, BORDER_SIZE, anchor=NW, image=worlds_data[World.LightWorld]["map_image"]),
    )

    worlds_data[World.DarkWorld]["canvas_image"] = (
        self.canvas.create_image(
            BORDER_SIZE + 512, BORDER_SIZE, anchor=NW, image=worlds_data[World.DarkWorld]["map_image"]
        ),
    )

    worlds_data[World.LightWorldInside]["map_image"] = ImageTk.PhotoImage(
        Image.open(worlds_data[World.LightWorldInside]["map_file"])
    )
    worlds_data[World.DarkWorldInside]["map_image"] = ImageTk.PhotoImage(Image.open(worlds_data[World.DarkWorldInside]["map_file"]))

    worlds_data[World.LightWorldInside]["canvas_image"] = (
        self.canvas.create_image(BORDER_SIZE, BORDER_SIZE + 512, anchor=NW, image=worlds_data[World.LightWorldInside]["map_image"]),
    )

    worlds_data[World.DarkWorldInside]["canvas_image"] = (
        self.canvas.create_image(
            BORDER_SIZE + 512, BORDER_SIZE + 512, anchor=NW, image=worlds_data[World.DarkWorldInside]["map_image"]
        ),
    )

    # Offset darkworld locations
    for name, loc in worlds_data[World.DarkWorld]["entrances"].items():
        worlds_data[World.DarkWorld]["entrances"][name]["x"] += self.cwidth

    for name, loc in worlds_data[World.DarkWorldInside]["entrances"].items():
        worlds_data[World.DarkWorldInside]["entrances"][name]["x"] += self.cwidth
        worlds_data[World.DarkWorldInside]["entrances"][name]["y"] += self.cwidth

    for name, loc in worlds_data[World.LightWorldInside]["entrances"].items():
        worlds_data[World.LightWorldInside]["entrances"][name]["y"] += self.cwidth

    # Display locations (and map?)
    for world in [World.LightWorld, World.DarkWorld, World.LightWorldInside, World.DarkWorldInside]:
        display_world_locations(self, world)

    hide_connections_button = ttk.Button(self, text="Hide All Connections", command=lambda: hide_all_connections(self))
    hide_connections_button.pack()
    show_connections_button = ttk.Button(self, text="Show All Connections", command=lambda: show_all_connections(self))
    show_connections_button.pack()

    self.load_yaml = load_yaml
    self.return_connections = return_connections

    # TODO: Add a new button to store this info somwhere as JSON for the generation
    return self
