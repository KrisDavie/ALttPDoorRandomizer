from enum import Enum
import math
from operator import ne
from tkinter import BOTH, Toplevel, ttk, NW, Canvas
from typing import final
from PIL import ImageTk, Image, ImageOps, ImageDraw
from collections import deque, defaultdict
import source.gui.customizer.item_sprite_data as item_sprite_data
from source.gui.customizer.worlds_data import worlds_data
from source.gui.customizer.new_location_data import supertile_overrides
from source.gui.customizer.doors_data import (
    doors_data,
    dungeon_lobbies,
    door_coordinates,
    doors_to_regions,
    regions_to_doors,
)
from DoorShuffle import (
    interior_doors,
    default_one_way_connections,
    logical_connections,
    dungeon_warps,
    spiral_staircases,
    straight_staircases,
    falldown_pits,
    vanilla_logical_connections,
)
from pathlib import Path


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


BORDER_SIZE = 20
TILE_BORDER_SIZE = 3
DOOR_COLOURS = {
    "Key Door": "gold",
    "Bomb Door": "blue",
    "Dash Door": "red",
    "Big Key Door": "green",
    "Trap Door": "gray",
    "Lobby Door": "white",
}

import sys

# TODO: Reaplce with Door sprites
item_sheet_path = Path("resources") / "app" / "gui" / "plandomizer" / "Item_Sheet.png"


# TODO: Crystal barriers are not in any lists and dungeons stop generating at them?
def door_customizer_page(top, parent, tab_world, eg_img=None):
    def init_page(self):
        if hasattr(self, "canvas"):
            self.canvas.destroy()
        self.canvas = Canvas(self, width=self.cwidth + (BORDER_SIZE * 2), height=self.cheight + (BORDER_SIZE * 2))
        self.canvas.pack()
        self.door_links = []
        self.tile_map = []
        self.doors = {}
        self.tiles_added = {}
        self.lobby_doors = []
        self.special_doors = {}

    def redraw_canvas(self):
        yaml = return_connections(self.door_links, self.lobby_doors, self.special_doors)[0]
        if len(yaml["doors"]) == 0:
            init_page(self)
            return
        load_yaml(self, yaml)

    def load_yaml(self, yaml_data):
        self.tiles = {}  # (eg_x, eg_y): (tile_x, tile_y)
        self.doors_processed = set()
        self.door_links_to_make = set()
        self.doors_to_process = deque()
        self.regions_processed = set()
        init_page(self)
        _interior_doors_dict = dict(interior_doors)
        _interior_doors_dict.update(dict([(x[1], x[0]) for x in interior_doors]))

        # Might want to move this above the yaml data, that way we take vanilla connections and just overwrite them
        #  This USED to be below the code below, see note above.
        for door_set in [
            logical_connections,
            interior_doors,
            falldown_pits,
            dungeon_warps,
            vanilla_logical_connections,
        ]:
            self.doors.update(door_set)

        for k, v in yaml_data["doors"].items():
            if type(v) == str:
                self.doors[k] = v
                self.doors[v] = k
            elif type(v) == dict:
                source = k
                if "dest" in v:
                    dest = v["dest"]
                else:
                    try:
                        dest = _interior_doors_dict[source]
                    except KeyError:
                        print("Could not find interior door for " + source)
                        continue
                self.doors[source] = dest
                self.doors[dest] = source
                if "type" in v:
                    if "type" == "Trap Door":
                        self.special_doors[dest] = v["type"]
                    else:
                        self.special_doors[source] = v["type"]
                        self.special_doors[dest] = v["type"]
                if "one-way" in v:
                    self.special_doors[dest] = "Trap Door"

        # Manual connections go here
        self.doors["Ice Bomb Drop Hole"] = "Ice Stalfos Hint Drop Entrance"
        self.doors["Ice Crystal Block Hole"] = "Ice Switch Room Drop Entrance"
        self.doors["Ice Falling Square Hole"] = "Ice Tall Hint Drop Entrance"
        self.doors["Ice Freezors Hole"] = "Ice Big Chest View Drop Entrance"
        self.doors["Ice Antechamber Hole"] = "Ice Boss Drop Entrance"
        self.doors["PoD Pit Room Bomb Hole"] = "PoD Basement Ledge Drop Entrance"
        self.doors["PoD Pit Room Freefall"] = "PoD Stalfos Basement Drop Entrance"
        self.doors["Swamp Attic Left Pit"] = "Swamp West Ledge Drop Entrance"
        self.doors["Swamp Attic Right Pit"] = "Swamp Barrier Ledge Drop Entrance"
        self.doors["Skull Final Drop Hole"] = "Skull Boss Drop Entrance"
        self.doors["Mire Torches Bottom Holes"] = "Mire Warping Pool Drop Entrance"
        self.doors["Mire Torches Top Holes"] = "Mire Conveyor Barrier Drop Entrance"
        self.doors["Mire Attic Hint Hole"] = "Mire BK Chest Ledge Drop Entrance"
        self.doors["GT Bob's Room Hole"] = "GT Ice Armos Drop Entrance"
        self.doors["GT Falling Torches Hole"] = "GT Staredown Drop Entrance"
        self.doors["GT Moldorm Hole"] = "GT Moldorm Pit Drop Entrance"

        self.inverse_doors = {v: k for k, v in self.doors.items()}

        for lobby in dungeon_lobbies[tab_world]:
            lobby_door = yaml_data["lobbies"][lobby]
            add_lobby(self, lobby_door, lobby)
            queue_regions_doors(self, lobby_door)

        while self.doors_to_process:
            # Get the next door

            next_door = self.doors_to_process.pop()

            self.doors_processed.add(next_door)

            # Get the EG tile of the current door
            door_is_door, door_tile_x, door_tile_y = get_doors_eg_tile(next_door)

            if door_is_door:
                queue_regions_doors(self, next_door)
                self.door_links_to_make.add(next_door)

            else:
                if next_door not in self.doors:
                    print("ERROR: Door not found in doors", next_door)
                    continue
                _region = self.doors[next_door]
                if _region not in regions_to_doors:
                    print("ERROR: Region not found in regions_to_doors", _region)
                    queue_regions_doors(self, self.doors[next_door])
                else:
                    queue_regions_doors(self, self.doors[next_door], region=True)

            # Find the door that this door is linked to
            linked_door = None
            for d in [self.doors, self.inverse_doors]:
                if next_door in d:
                    linked_door = d[next_door]
                    if linked_door not in self.doors_processed and linked_door not in regions_to_doors:
                        self.doors_to_process.appendleft(linked_door)

            linked_door_is_door, linked_door_x, linked_door_y = get_doors_eg_tile(linked_door)

            # TODO: Need to add the link here

            # (Is this a door) or (have we already added the tile)?
            if not door_is_door or (door_tile_x, door_tile_y) in self.tiles:
                continue

            # PoD warp tile (Never seen but still linked, start from 0,0)
            if (linked_door_x, linked_door_y) in self.tiles:
                new_tile_x, new_tile_y = self.tiles[(linked_door_x, linked_door_y)]
            else:
                new_tile_x = new_tile_y = 0

            # Find closest unused map tile to place supertile in, respect directionality where possible
            direction = doors_data[next_door][1]
            last_cardinal = 0
            while (new_tile_x, new_tile_y) in self.tiles.values():
                if (direction == "We" and last_cardinal == 0) or (
                    ((direction == "No" or direction == "Up") or (direction == "So" or direction == "Dn"))
                    and last_cardinal == -1
                ):
                    # new_tile_x -= 1
                    new_tile_x += 1
                elif (direction == "Ea" and last_cardinal == 0) or (
                    ((direction == "No" or direction == "Up") or (direction == "So" or direction == "Dn"))
                    and last_cardinal == 1
                ):
                    # new_tile_x += 1
                    new_tile_x -= 1
                elif ((direction == "No" or direction == "Up") and last_cardinal == 0) or (
                    (direction == "We" or direction == "Ea") and last_cardinal == -1
                ):
                    new_tile_y += 1
                elif ((direction == "So" or direction == "Dn") and last_cardinal == 0) or (
                    (direction == "We" or direction == "Ea") and last_cardinal == 1
                ):
                    new_tile_y -= 1
                if last_cardinal == 0:
                    last_cardinal = -1
                elif last_cardinal == -1:
                    last_cardinal = 1
                elif last_cardinal == 1:
                    last_cardinal = 0
            self.tiles[(door_tile_x, door_tile_y)] = (new_tile_x, new_tile_y)

        for door in self.door_links_to_make:
            try:
                linked_door = self.doors[door] if door in self.doors else self.inverse_doors[door]
            except KeyError:
                print(f"  Couldn't make link for {door}, likely a lobby")
            add_door_link(self, door, linked_door)
        draw_map(self)

    def queue_regions_doors(self, door, region=False):
        if not region:
            if door in doors_to_regions:
                nd_region = doors_to_regions[door]
            else:
                print("ERROR: Door not found in doors_to_regions", door)
                return
        else:
            nd_region = door

        if nd_region in self.regions_processed:
            return

        region_doors = regions_to_doors[nd_region]

        # Add doors to queue
        for future_door in region_doors:
            if not (
                future_door == door
                or future_door in self.doors_processed
                or future_door in self.doors_to_process
                or future_door in regions_to_doors
            ):
                self.doors_to_process.append(future_door)
        self.regions_processed.add(nd_region)

    def get_doors_eg_tile(door):
        if door in doors_data:
            return (
                True,
                int(doors_data[door][0]) % 16,
                int(doors_data[door][0]) // 16,
            )
        else:
            return (False, None, None)

    def add_lobby(self, lobby_room, lobby):
        _, x, y = get_doors_eg_tile(lobby_room)
        if (0, 0) in self.tiles.values():
            if "East" in lobby_room:
                tile_x = max(self.tiles.values(), key=lambda x: x[0])[0] + 1
            else:
                tile_x = min(self.tiles.values(), key=lambda x: x[0])[0] - 1
            self.tiles[(x, y)] = (tile_x, 0)
        else:
            self.tiles[(x, y)] = (0, 0)
        add_lobby_door(self, lobby_room, lobby)

    def draw_map(self):
        # Normalise tile map to have origin at (0,0)
        # First invert map to bring y0 to top

        min_x = min(self.tiles.values(), key=lambda x: x[0])[0]
        min_y = min(self.tiles.values(), key=lambda x: x[1])[1]
        for k, v in self.tiles.items():
            self.tiles[k] = (v[0] - min_x, v[1] - min_y)

        max_y = max(self.tiles.values(), key=lambda x: x[0])[0] + 1
        max_x = max(self.tiles.values(), key=lambda x: x[1])[1]

        if max_y // 2 < max_x:
            self.map_dims = (max_x, max_x * 2)
        else:
            self.map_dims = (max_y // 2, ((max_y // 2) * 2))

        self.map_dims = (self.map_dims[0] + 1, self.map_dims[1] + 2)

        self.tile_size = (self.cwidth // (self.map_dims[1])) - (TILE_BORDER_SIZE * 2)
        self.tile_map = []

        for row in range(self.map_dims[0]):
            self.tile_map.append([])
            for col in range(self.map_dims[1]):
                x1 = (col * self.tile_size) + BORDER_SIZE + (((2 * col + 1) - 1) * TILE_BORDER_SIZE)
                y1 = (row * self.tile_size) + BORDER_SIZE + (((2 * row + 1) - 1) * TILE_BORDER_SIZE)
                tile = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x1 + self.tile_size,
                    y1 + self.tile_size,
                    outline="",
                    fill=f"#888",
                    activefill=f"#800",
                )
                self.canvas.tag_bind(tile, "<Button-1>", lambda event: select_tile(self, event))
                self.tile_map[row].append({"button": tile, "tile": None})

        for tile in self.tiles:
            x, y = tile
            if x == None or y == None:
                continue
            tile_x, tile_y = self.tiles[tile]
            x1 = (tile_x * self.tile_size) + BORDER_SIZE + (((2 * tile_x + 1) - 1) * TILE_BORDER_SIZE)
            y1 = (tile_y * self.tile_size) + BORDER_SIZE + (((2 * tile_y + 1) - 1) * TILE_BORDER_SIZE)
            img = ImageTk.PhotoImage(
                eg_img.crop((x * 512, y * 512, (x + 1) * 512, (y + 1) * 512)).resize(
                    (self.tile_size, self.tile_size), Image.ANTIALIAS
                )
            )
            map = self.canvas.create_image(x1, y1, image=img, anchor=NW)
            self.tile_map[tile_y][tile_x]["map"] = map
            self.tile_map[tile_y][tile_x]["tile"] = (x, y)
            self.tiles_added[(x, y)] = img

        # Display links between doors here
        for n, door_link in enumerate(self.door_links):
            min_x = abs(
                min([x["source_tile"][0] for x in self.door_links] + [x["linked_tile"][0] for x in self.door_links])
            )
            min_y = abs(
                min([x["source_tile"][1] for x in self.door_links] + [x["linked_tile"][1] for x in self.door_links])
            )

            x1, y1 = get_final_door_coords(self, door_link, "source", min_x, min_y)
            x2, y2 = get_final_door_coords(self, door_link, "linked", min_x, min_y)
            self.door_links[n]["button"] = self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="black",
                width=2,
                arrow=BOTH,
                activefill="red",
            )

            if door_link["door"] in self.special_doors:
                self.door_links[n]["special_button"] = self.canvas.create_rectangle(
                    x1 - 5,
                    y1 - 5,
                    x1 + 5,
                    y1 + 5,
                    fill=DOOR_COLOURS[self.special_doors[door_link["door"]]],
                    width=2,
                    activefill="red",
                )
            if door_link["linked_door"] in self.special_doors:
                self.door_links[n]["special_button"] = self.canvas.create_rectangle(
                    x2 - 5,
                    y2 - 5,
                    x2 + 5,
                    y2 + 5,
                    fill=DOOR_COLOURS[self.special_doors[door_link["linked_door"]]],
                    width=2,
                    activefill="red",
                )

        for n, lobby in enumerate(self.lobby_doors):
            min_x = abs(
                min([x["source_tile"][0] for x in self.door_links] + [x["linked_tile"][0] for x in self.door_links])
            )
            min_y = abs(
                min([x["source_tile"][1] for x in self.door_links] + [x["linked_tile"][1] for x in self.door_links])
            )

            x1, y1 = get_final_door_coords(self, lobby, "source", min_x, min_y)
            self.lobby_doors[n]["button"] = self.canvas.create_rectangle(
                x1 - 5,
                y1 - 5,
                x1 + 5,
                y1 + 5,
                fill=DOOR_COLOURS["Lobby Door"],
                width=2,
                activefill="red",
            )
            # self.canvas.create_text(x1, y1, text=f"{door_link['door']}", fill="black")
            # self.canvas.create_text(x2, y2, text=f"{door_link['linked_door']}", fill="black")

    def get_final_door_coords(self, door, door_type, min_x, min_y):
        if door_type == "source":
            tile = "source_tile"
            coords = "source_coords"
        elif door_type == "linked":
            tile = "linked_tile"
            coords = "linked_coords"

        door_tile_x = door[tile][0] + (min_x)
        door_tile_y = door[tile][1] + (min_y)
        x = ((door[coords][0] / 512) * self.tile_size) + (
            (door_tile_x * self.tile_size) + BORDER_SIZE + (((2 * door_tile_x + 1) - 1) * TILE_BORDER_SIZE)
        )
        y = ((door[coords][1] / 512) * self.tile_size) + (
            (door_tile_y * self.tile_size) + BORDER_SIZE + (((2 * door_tile_y + 1) - 1) * TILE_BORDER_SIZE)
        )
        return x, y

    def add_door_link(self, door, linked_door):
        try:
            ld_eg_x = int(doors_data[linked_door][0]) % 16
            ld_eg_y = int(doors_data[linked_door][0]) // 16
            d_eg_x = int(doors_data[door][0]) % 16
            d_eg_y = int(doors_data[door][0]) // 16
            ld_t_x, ld_t_y = self.tiles[(ld_eg_x, ld_eg_y)]
            d_t_x, d_t_y = self.tiles[(d_eg_x, d_eg_y)]
            ld_data = [x for x in door_coordinates[(ld_eg_x, ld_eg_y)] if x["name"] == linked_door][0]
            d_data = [x for x in door_coordinates[(d_eg_x, d_eg_y)] if x["name"] == door][0]
            self.door_links.append(
                {
                    "door": door,
                    "linked_door": linked_door,
                    "source_tile": (d_t_x, d_t_y),
                    "linked_tile": (ld_t_x, ld_t_y),
                    "source_coords": (d_data["x"], d_data["y"]),
                    "linked_coords": (ld_data["x"], ld_data["y"]),
                }
            )
        except:
            print(f"Error adding door link for {door} and {linked_door}")

    def add_lobby_door(self, door, lobby):
        d_eg_x = int(doors_data[door][0]) % 16
        d_eg_y = int(doors_data[door][0]) // 16
        d_t_x, d_t_y = self.tiles[(d_eg_x, d_eg_y)]
        d_data = [x for x in door_coordinates[(d_eg_x, d_eg_y)] if x["name"] == door][0]
        self.lobby_doors.append(
            {
                "door": door,
                "lobby": lobby,
                "source_tile": (d_t_x, d_t_y),
                "source_coords": (d_data["x"], d_data["y"]),
            }
        )

    # def get_linked_doors(self, door, tiles=set()):
    #     x = int(doors_data[door][0]) % 16
    #     y = int(doors_data[door][0]) // 16
    #     if (x, y) in tiles:
    #         return tiles
    #     else:
    #         tiles.add((x, y))
    #         for door in door_coordinates[(x, y)]:
    #             door = door["name"]
    #             try:
    #                 if door in self.doors:
    #                     linked_door = self.doors[door]
    #                 else:
    #                     linked_door = self.inverse_doors[door]
    #             except KeyError:
    #                 continue
    #             tiles = tiles.union(get_linked_tiles(self, linked_door, tiles))
    #         return tiles

    def get_tile(self):
        x = y = None
        for row in range(self.map_dims[0]):
            for col in range(self.map_dims[1]):
                if self.tile_map[row][col]["tile"] == None:
                    x = row
                    y = col
                    x1 = (col * self.tile_size) + BORDER_SIZE + (((2 * col + 1) - 1) * TILE_BORDER_SIZE)
                    y1 = (row * self.tile_size) + BORDER_SIZE + (((2 * row + 1) - 1) * TILE_BORDER_SIZE)
                    return x1, y1, (x, y)

        # if x == None and y == None:
        # print("No more room for tiles!")

    def add_connection(self, door, linked_door):
        if door not in self.doors:
            self.doors[door] = linked_door
            x1, y1, map_tile = get_tile(self)
            x = int(doors_data[door][0]) % 16
            y = int(doors_data[door][0]) // 16
            self.tile_map[map_tile[0]][map_tile[1]]["tile"] = (x, y)
            if (x, y) not in self.tiles_added:
                img = ImageTk.PhotoImage(
                    eg_img.crop((x * 512, y * 512, (x + 1) * 512, (y + 1) * 512)).resize(
                        (self.tile_size, self.tile_size), Image.NEAREST
                    )
                )
                map = self.canvas.create_image(x1, y1, image=img, anchor=NW)
                self.tile_map[map_tile[0]][map_tile[1]]["map"] = map
                self.tiles_added[(x, y)] = img

    def get_loc_by_button(self, button):
        for name, loc in worlds_data[tab_world][f"locations_{tab_item_type}"].items():
            if loc["button"] == button[0]:
                return name
        for name, data in self.placed_items.items():
            if data["image"] == button[0]:
                return name

    def return_connections(door_links, lobby_doors, special_doors):

        final_connections = {"doors": {}, "lobbies": {}}
        doors_type = "vanilla"
        if len(door_links) == 0:
            return final_connections, False
        for data in door_links:
            door = data["door"]
            linked_door = data["linked_door"]
            final_connections["doors"][door] = linked_door
            if door in special_doors:
                door_type = special_doors[door]
                final_connections["doors"][door] = {"dest": final_connections["doors"][door], "type": door_type}

        for lobby_data in lobby_doors:
            lobby = lobby_data["lobby"]
            lobby_door = lobby_data["door"]
            final_connections["lobbies"][lobby] = lobby_door

        return final_connections, doors_type

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

    def select_tile(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return
        self.canvas.itemconfigure(item, state="normal", fill="#00f")

    self = ttk.Frame(parent)
    # self.cwidth = 1024
    # self.cheight = 512
    self.cwidth = 2048
    self.cheight = 1024
    self.select_state = SelectState.NoneSelected
    redraw_canvas_button = ttk.Button(self, text="Redraw Canvas", command=lambda: redraw_canvas(self))
    redraw_canvas_button.pack()

    init_page(self)

    self.load_yaml = load_yaml
    self.return_connections = return_connections

    # TODO: Add a new button to store this info somwhere as JSON for the generation
    return self
