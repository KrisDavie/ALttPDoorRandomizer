from enum import Enum
import pickle
from tkinter import BOTH, BooleanVar, Toplevel, ttk, NW, Canvas
from PIL import ImageTk, Image, ImageOps
from collections import deque, defaultdict
import source.gui.customizer.doors_sprite_data as doors_sprite_data
from source.gui.customizer.worlds_data import worlds_data, dungeon_worlds
from source.gui.customizer.doors_data import (
    doors_data,
    dungeon_lobbies,
    door_coordinates,
    doors_to_regions,
    regions_to_doors,
)
from DoorShuffle import (
    interior_doors,
    logical_connections,
    dungeon_warps,
    falldown_pits,
    vanilla_logical_connections,
)
from pathlib import Path


class SelectState(Enum):
    NoneSelected = 0
    SourceSelected = 1


BORDER_SIZE = 20
TAB_ITEM_TYPE = tab_item_type = "Doors"
TILE_BORDER_SIZE = 3
DOOR_COLOURS = {
    "Key Door": "gold",
    "Bomb Door": "blue",
    "Dash Door": "red",
    "Big Key Door": "green",
    "Trap Door": "gray",
    "Lobby Door": "white",
}
MANUAL_REGIONS_ADDED = {
    "Sewers Secret Room Up Stairs": "Sewers Rat Path",  # Sewer Drop
    "Skull Small Hall ES": "Skull Back Drop",  # Skull Back Drop
    "Skull Pot Circle WN": "Skull Pot Circle",  # Skull Pot Circle
    "Skull Left Drop ES": "Skull Left Drop",  # Skull Left Drop
    "Skull Pinball NE": "Skull Pinball",  # Skull Pinball
}


item_sheet_path = Path("resources") / "app" / "gui" / "plandomizer" / "Doors_Sheet.png"


def door_customizer_page(
    top, parent, tab_world, eg_img=None, eg_selection_mode=False, vanilla_data=None, plando_window=None
):
    def init_page(self, redraw=False):
        # Do we have a canvas already? If so, destroy it and make a new one
        if hasattr(self, "canvas"):
            self.canvas.destroy()
        self.canvas = Canvas(self, width=self.cwidth + (BORDER_SIZE * 2), height=self.cheight + (BORDER_SIZE * 2))
        self.canvas.pack()

        # Are we plotting the vanilla map? If so, we need leave the vanilla data in place (added when the page is created)
        if not self.eg_selection_mode:
            self.tile_map = []

        # Initialise the variables we need
        self.door_links = []
        self.doors = {}
        self.tiles_added = {}
        self.lobby_doors = []
        self.special_doors = {}
        self.eg_tiles = {}
        self.placed_icons = defaultdict(dict)

        #  If we're redrawing, we need to keep tiles with no current connections, we store them temporarily in old_tiles
        if redraw:
            self.old_tiles = self.tiles.copy()
        else:
            self.old_tiles = {}

        #  reinitialise the tiles dict
        self.tiles = {}

    def redraw_canvas(self):
        yaml = return_connections(self.door_links, self.lobby_doors, self.special_doors)[0]
        load_yaml(self, yaml, redraw=True)

    def load_yaml(self, yaml_data, redraw=False):
        self.doors_processed = set()
        self.door_links_to_make = set()
        self.doors_to_process = deque()
        self.regions_processed = set()
        init_page(self, redraw=redraw)
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

        # We somehow need to include the dropdowns from the overworld here
        # They don't have an external door, but we need to include them in the map
        # otherwise dropdowns leading to isloated areas will be missed when drawing the map

        self.inverse_doors = {v: k for k, v in self.doors.items()}

        for lobby in dungeon_lobbies[tab_world]:
            if len(yaml_data["lobbies"]) == 0:
                break
            lobby_door = yaml_data["lobbies"][lobby]
            add_lobby(self, lobby_door, lobby)
            queue_regions_doors(self, lobby_door)

        while self.doors_to_process:
            # Get the next door

            next_door = self.doors_to_process.pop()

            if next_door in MANUAL_REGIONS_ADDED:
                queue_regions_doors(self, MANUAL_REGIONS_ADDED[next_door], region=True)

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

    def draw_vanilla_eg_map(self, top):
        for tile_y, x_tiles in enumerate(self.tile_map):
            for tile_x, tile_data in enumerate(x_tiles):
                if tile_data["tile"] == None:
                    continue
                x, y = tile_data["tile"]
                x1 = (tile_x * self.tile_size) + BORDER_SIZE + (((2 * tile_x + 1) - 1) * TILE_BORDER_SIZE)
                y1 = (tile_y * self.tile_size) + BORDER_SIZE + (((2 * tile_y + 1) - 1) * TILE_BORDER_SIZE)
                img = ImageTk.PhotoImage(
                    eg_img.crop((x * 512, y * 512, (x + 1) * 512, (y + 1) * 512)).resize(
                        (self.tile_size, self.tile_size), Image.ANTIALIAS
                    )
                )
                kwargs = {}
                # if parent.eg_tile_multiuse[tile_data["tile"]] == 0:
                #     kwargs = {"stipple": "gray12", "state": "disabled"}
                map = self.canvas.create_image(x1, y1, image=img, anchor=NW, **kwargs)
                self.tile_map[tile_y][tile_x]["map"] = map
                self.eg_tiles[(map,)] = (x, y)
                self.canvas.tag_bind(map, "<Button-1>", lambda event: select_eg_tile(self, top, event, plando_window))
                self.tiles_added[(x, y)] = img

    def draw_map(self):
        icon_queue = []
        if len(self.tiles) > 0:
            min_x = min(self.tiles.values(), key=lambda x: x[0])[0]
            min_y = min(self.tiles.values(), key=lambda x: x[1])[1]
            for k, v in self.tiles.items():
                self.tiles[k] = (v[0] - min_x, v[1] - min_y)

            max_y = max(self.tiles.values(), key=lambda x: x[0])[0] + 1
            max_x = max(self.tiles.values(), key=lambda x: x[1])[1]
        else:
            max_x = max_y = 2
            min_y = min_x = 3

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
                self.eg_tiles[(tile,)] = (col, row)

        for tile in self.old_tiles:
            if tile not in self.tiles:
                for row in range(self.map_dims[0]):
                    for col in range(self.map_dims[1]):
                        if self.tile_map[row][col]["tile"] == None:
                            self.tiles[tile] = self.old_tiles[tile]
        self.old_tiles = {}

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
            # TODO: There's a bug here when loading a second yaml file - possibly also with redrawing the map
            try:
                self.tile_map[tile_y][tile_x]["map"] = map
            except:
                print("Error: ", tile_x, tile_y, self.tile_map)
            self.eg_tiles[(map,)] = (x, y)
            self.tile_map[tile_y][tile_x]["tile"] = (x, y)
            self.tiles_added[(x, y)] = img

        # Display links between doors here
        doors_linked = set()

        # I don't know why this needs to be different for the unlinked doors...
        flat_tile_map = [item for sublist in self.tile_map for item in sublist]
        min_x = abs(min([x["tile"][0] if x["tile"] is not None else 0 for x in flat_tile_map]))
        min_y = abs(min([x["tile"][1] if x["tile"] is not None else 0 for x in flat_tile_map]))

        for n, door_link in enumerate(self.door_links):
            # min_x = abs(
            #     min([x["source_tile"][0] for x in self.door_links] + [x["linked_tile"][0] for x in self.door_links])
            # )
            # min_y = abs(
            #     min([x["source_tile"][1] for x in self.door_links] + [x["linked_tile"][1] for x in self.door_links])
            # )

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
            doors_linked.add(door_link["door"])
            doors_linked.add(door_link["linked_door"])

            if door_link["door"] in self.special_doors:
                icon_queue.append((self.special_doors[door_link["door"]], x1, y1))
            if door_link["linked_door"] in self.special_doors:
                icon_queue.append((self.special_doors[door_link["linked_door"]], x1, y1))

        for n, lobby in enumerate(self.lobby_doors):
            # min_x = abs(
            #     min([x["source_tile"][0] for x in self.door_links] + [x["linked_tile"][0] for x in self.door_links])
            # )
            # min_y = abs(
            #     min([x["source_tile"][1] for x in self.door_links] + [x["linked_tile"][1] for x in self.door_links])
            # )

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
            doors_linked.add(lobby["door"])
            doors_linked.add(lobby["lobby"])

        # Draw any unlinked doors
        for door, data in doors_data.items():
            if door not in doors_linked:
                d_eg_x = int(data[0]) % 16
                d_eg_y = int(data[0]) // 16
                if (d_eg_x, d_eg_y) not in self.tiles_added:
                    continue
                d_t_x, d_t_y = self.tiles[(d_eg_x, d_eg_y)]
                d_data = [x for x in door_coordinates[(d_eg_x, d_eg_y)] if x["name"] == door][0]
                _data = {
                    "door": door,
                    "source_tile": (d_t_x, d_t_y),
                    "source_coords": (d_data["x"], d_data["y"]),
                }
                x1, y1 = get_final_door_coords(self, _data, "source", min_x, min_y)
                self.canvas.create_oval(
                    x1 - 5,
                    y1 - 5,
                    x1 + 5,
                    y1 + 5,
                    fill="#0f0",
                    width=2,
                    activefill="red",
                )

        while icon_queue:
            icon, x, y = icon_queue.pop()
            place_door_icon(self, icon, x, y)

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
        for name, data in self.placed_icons.items():
            if data["image"] == button[0]:
                return name

    def place_door_icon(self, placed_icon, x_loc, y_loc):
        # self.canvas.itemconfigure(item, state="hidden")

        # Place a new sprite
        sprite_y, sprite_x = doors_sprite_data.item_table[placed_icon]
        self.placed_icons[(x_loc, y_loc)]["sprite"] = ImageTk.PhotoImage(
            ImageOps.expand(
                Image.open(item_sheet_path).crop(
                    (sprite_x * 16, sprite_y * 16, sprite_x * 16 + 16, sprite_y * 16 + 16)
                ),
                1,
                "#fff",
            )
        )
        self.placed_icons[(x_loc, y_loc)]["image"] = self.canvas.create_image(
            x_loc,
            y_loc,
            image=self.placed_icons[(x_loc, y_loc)]["sprite"],
        )
        # self.canvas.tag_bind(
        #     self.placed_icons[loc_name]["image"],
        #     "<Button-3>",
        #     lambda event: remove_item(self, event),
        # )

    def select_location(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if item in [w["canvas_image"] for w in worlds_data.values()]:
            return

        # Get the location name from the button
        loc_name = get_loc_by_button(self, item)

        if self.select_state == SelectState.NoneSelected:
            self.canvas.itemconfigure(item, fill="orange")
            self.select_state = SelectState.SourceSelected
            self.source_location = item
        elif self.select_state == SelectState.SourceSelected:
            if has_target(self, loc_name):
                return

            add_door_link(self, get_loc_by_button(self, self.source_location), loc_name)
            self.defined_connections[get_loc_by_button(self, self.source_location)] = loc_name
            self.select_state = SelectState.NoneSelected

    def has_source(self, loc_name):
        return loc_name in self.defined_connections

    def has_target(self, loc_name):
        return loc_name in self.defined_connections.values()

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

    def select_tile(self, event):
        self.setvar("selected_eg_tile", BooleanVar(value=False))
        if self.eg_tile_window:
            self.eg_tile_window.deiconify()
        else:
            eg_tile_window = Toplevel(self)
            self.eg_tile_window_notebook = ttk.Notebook(eg_tile_window)
            self.eg_tile_window_notebook.pages = {}
            with open(Path("resources/app/gui/plandomizer/vanilla_layout.pickle"), "rb") as f:
                vanilla_layout = pickle.load(f)
            for dungeon, world in dungeon_worlds.items():
                if dungeon in ["Overworld", "Underworld"]:
                    continue
                self.eg_tile_window_notebook.pages[dungeon] = ttk.Frame(self.eg_tile_window_notebook)
                self.eg_tile_window_notebook.add(
                    self.eg_tile_window_notebook.pages[dungeon], text=dungeon.replace("_", " ")
                )
                self.eg_tile_window_notebook.pages[dungeon].content = door_customizer_page(
                    eg_tile_window,
                    self.eg_tile_window_notebook.pages[dungeon],
                    world,
                    eg_img=eg_img,
                    eg_selection_mode=True,
                    vanilla_data=vanilla_layout[dungeon],
                    plando_window=self,
                )
                self.eg_tile_window_notebook.pages[dungeon].content.pack(fill=BOTH, expand=True)

            self.eg_tile_window_notebook.pack()

            eg_tile_window.title("EG Map Window")
            self.eg_tile_window = eg_tile_window

        self.eg_tile_window.focus_set()
        self.eg_tile_window.grab_set()
        # self.eg_tile_window.wait_visibility(self.eg_tile_window)
        self.wait_variable("selected_eg_tile")

        empty_tile = self.canvas.find_closest(event.x, event.y)
        tile_x, tile_y = self.eg_tiles[empty_tile]
        x1 = (tile_x * self.tile_size) + BORDER_SIZE + (((2 * tile_x + 1) - 1) * TILE_BORDER_SIZE)
        y1 = (tile_y * self.tile_size) + BORDER_SIZE + (((2 * tile_y + 1) - 1) * TILE_BORDER_SIZE)

        x, y = self.selected_eg_tile

        # Add clicked EG tile to clicked empty tile

        img = ImageTk.PhotoImage(
            eg_img.crop((x * 512, y * 512, (x + 1) * 512, (y + 1) * 512)).resize(
                (self.tile_size, self.tile_size), Image.ANTIALIAS
            )
        )
        self.tiles_added[(x, y)] = img
        map = self.canvas.create_image(x1, y1, image=img, anchor=NW)
        self.tiles[self.selected_eg_tile] = (tile_x, tile_y)

        self.tile_map[tile_y][tile_x]["map"] = map
        flat_tile_map = [item for sublist in self.tile_map for item in sublist]
        orig_min_x = abs(min([x["tile"][0] if x["tile"] is not None else 0 for x in flat_tile_map]))
        orig_min_y = abs(min([x["tile"][1] if x["tile"] is not None else 0 for x in flat_tile_map]))
        # Draw any unlinked doors
        for door, data in doors_data.items():
            if door not in [dl["door"] for dl in self.door_links] + [dl["linked_door"] for dl in self.door_links]:
                d_eg_x = int(data[0]) % 16
                d_eg_y = int(data[0]) // 16
                if (d_eg_x, d_eg_y) not in self.tiles_added:
                    continue
                d_t_x, d_t_y = self.tiles[(d_eg_x, d_eg_y)]
                d_data = [x for x in door_coordinates[(d_eg_x, d_eg_y)] if x["name"] == door][0]
                _data = {
                    "door": door,
                    "source_tile": (d_t_x, d_t_y),
                    "source_coords": (d_data["x"], d_data["y"]),
                }
                x1, y1 = get_final_door_coords(self, _data, "source", orig_min_x, orig_min_y)
                self.canvas.create_oval(
                    x1 - 5,
                    y1 - 5,
                    x1 + 5,
                    y1 + 5,
                    fill="lightgreen",
                    width=2,
                    activefill="red",
                )

    def select_eg_tile(self, top, event, parent):
        tile = self.canvas.find_closest(event.x, event.y)
        eg_tile = self.eg_tiles[tile]
        parent.selected_eg_tile = eg_tile
        parent.setvar("selected_eg_tile", BooleanVar(value=True))
        top.grab_release()
        top.withdraw()

    self = ttk.Frame(parent)
    self.eg_selection_mode = eg_selection_mode
    self.eg_tile_window = None
    # self.cwidth = 1024
    # self.cheight = 512
    self.cwidth = 2048
    self.cheight = 1024
    self.select_state = SelectState.NoneSelected
    if not eg_selection_mode:
        redraw_canvas_button = ttk.Button(self, text="Redraw Canvas", command=lambda: redraw_canvas(self))
        redraw_canvas_button.pack()
    if vanilla_data:
        self.tile_map = vanilla_data["tile_map"]
        self.tile_size = vanilla_data["tile_size"]
        self.map_dims = vanilla_data["map_dims"]

    init_page(self)

    #  If we're in eg selection mode, we need to use the special function to only draw tiles and not connections
    if self.eg_selection_mode:
        draw_vanilla_eg_map(self, top)
    else:
        draw_map(self)

    self.load_yaml = load_yaml
    self.return_connections = return_connections

    # TODO: Add a new button to store this info somwhere as JSON for the generation
    return self
