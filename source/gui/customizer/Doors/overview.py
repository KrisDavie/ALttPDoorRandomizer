from enum import Enum
import pickle
from tkinter import BOTH, BooleanVar, Toplevel, ttk, NW, Canvas
from PIL import ImageTk, Image, ImageOps
from collections import deque, defaultdict
import source.gui.customizer.doors_sprite_data as doors_sprite_data
from source.gui.customizer.Entrances.overview import SelectState
from source.gui.customizer.worlds_data import worlds_data, dungeon_worlds
from source.gui.customizer.doors_data import (
    doors_data,
    dungeon_lobbies,
    door_coordinates,
    doors_to_regions,
    regions_to_doors,
    door_coordinates_key,
)
from DoorShuffle import (
    interior_doors,
    logical_connections,
    dungeon_warps,
    falldown_pits,
    vanilla_logical_connections,
)
from pathlib import Path


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
    "Eastern Hint Tile WN": "Eastern Hint Tile Blocked Path",  # Eastern Hint Tile
}


item_sheet_path = Path("resources") / "app" / "gui" / "plandomizer" / "Doors_Sheet.png"


def door_customizer_page(
    top, parent, tab_world, eg_img=None, eg_selection_mode=False, vanilla_data=None, plando_window=None
):
    def init_page(self, redraw=False):
        self.select_state = SelectState.NoneSelected

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
        self.unlinked_doors = set()
        self.door_buttons = {}
        self.sanc_dungeon = False

        #  If we're redrawing, we need to keep tiles with no current connections, we store them temporarily in old_tiles
        if redraw:
            self.old_tiles = self.tiles.copy()
            # print("old tiles", self.old_tiles)
        else:
            self.old_tiles = {}

        #  reinitialise the tiles dict
        self.tiles = {}

    def redraw_canvas(self):
        yaml = return_connections(self.door_links, self.lobby_doors, self.special_doors)[0]
        load_yaml(self, yaml, redraw=True)

    def load_yaml(self, yaml_data, redraw=False):
        # print(yaml_data)
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

        if (
            (
                "Sanctuary N" in self.doors
                or "Sanctuary S" in self.doors
                or "Sanctuary N" in self.inverse_doors
                or "Sanctuary S" in self.inverse_doors
            )
            and "Sanctuary" not in yaml_data["lobbies"]
        ) or (2, 1) in self.old_tiles:
            self.sanc_dungeon = True
            add_lobby(self, "Sanctuary Mirror Route", "Sanctuary")
            queue_regions_doors(self, "Sanctuary Mirror Route")

        for lobby in dungeon_lobbies[tab_world]:
            if len(yaml_data["lobbies"]) == 0:
                break
            if not lobby in yaml_data["lobbies"]:
                continue
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
                add_door_link(self, door, linked_door)
            except KeyError:
                # Couldn't make link for {door}, possibly a lobby or unlinked
                pass
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
        # Coords are x = left -> right, y = top -> bottom, 0,0 is top left
        if door in doors_data:
            # (found, x, y)
            return (
                True,
                int(doors_data[door][0]) % 16,
                int(doors_data[door][0]) // 16,
            )
        else:
            return (False, None, None)

    def add_lobby(self, lobby_room, lobby):
        _, x, y = get_doors_eg_tile(lobby_room)

        if (x, y) in self.tiles:
            add_lobby_door(self, lobby_room, lobby)
            return
        if (0, 0) in self.tiles.values():
            if "East" in lobby_room:
                tile_x = max(self.tiles.values(), key=lambda x: x[0])[0] + 1
            else:
                tile_x = min(self.tiles.values(), key=lambda x: x[0])[0] - 1
            self.tiles[(x, y)] = (tile_x, 0)
        else:
            self.tiles[(x, y)] = (0, 0)
        add_lobby_door(self, lobby_room, lobby)

    def get_eg_tile_img(self, x, y, tile_x, tile_y, ci_kwargs={}):
        x1 = (tile_x * self.tile_size) + BORDER_SIZE + (((2 * tile_x + 1) - 1) * TILE_BORDER_SIZE)
        y1 = (tile_y * self.tile_size) + BORDER_SIZE + (((2 * tile_y + 1) - 1) * TILE_BORDER_SIZE)

        img = ImageTk.PhotoImage(
            eg_img.crop((x * 512, y * 512, (x + 1) * 512, (y + 1) * 512)).resize(
                (self.tile_size, self.tile_size), Image.ANTIALIAS
            )
        )
        map = self.canvas.create_image(x1, y1, image=img, anchor=NW, **ci_kwargs)
        self.tiles_added[(x, y)] = img
        try:
            self.tile_map[tile_y][tile_x]["map"] = map
        except:
            print("Err")
        return map, img

    def draw_vanilla_eg_map(self, top):
        for tile_y, x_tiles in enumerate(self.tile_map):
            for tile_x, tile_data in enumerate(x_tiles):
                if tile_data["tile"] == None:
                    continue
                x, y = tile_data["tile"]

                kwargs = {}
                # if parent.eg_tile_multiuse[tile_data["tile"]] == 0:
                #     kwargs = {"stipple": "gray12", "state": "disabled"}
                map, img = get_eg_tile_img(self, x, y, tile_x, tile_y)
                self.eg_tiles[(map,)] = (x, y)
                self.canvas.tag_bind(map, "<Button-1>", lambda event: select_eg_tile(self, top, event, plando_window))

    def get_door_coords(door):
        eg_tile, list_pos = door_coordinates_key[door]
        return door_coordinates[eg_tile][list_pos]

    def draw_map(self):
        # x is columns, y is rows
        icon_queue = []
        # print(self.tiles)
        # print(self.old_tiles)
        if len(self.tiles) > 0:
            # Get the min x and y values
            min_x = min(self.tiles.values(), key=lambda x: x[0])[0]
            min_y = min(self.tiles.values(), key=lambda x: x[1])[1]
            max_x = max(self.tiles.values(), key=lambda x: x[0])[0]
            max_y = max(self.tiles.values(), key=lambda x: x[1])[1]

        else:
            # No tiles to plot, make an empty map
            min_x = min_y = 0
            max_x = 4
            max_y = 2

        len_x = max((max_x - min_x), 4) + 1
        len_y = max((max_y - min_y), 2) + 1
        x_offset = abs(min_x) if min_x < 0 else 0
        y_offset = abs(min_y) if min_y < 0 else 0

        #  dims = (rows, columns), (y, x)
        if len_x >= len_y * 2:
            self.map_dims = ((len_x // 2) + 1), (((len_x // 2) + 1) * 2)
        else:
            self.map_dims = (len_y, len_y * 2)

        y_offset += (self.map_dims[0] - len_y) // 2
        x_offset += (self.map_dims[1] - len_x) // 2
        self.y_offset = y_offset
        self.x_offset = x_offset

        self.tile_size = (self.cwidth // (self.map_dims[1])) - (TILE_BORDER_SIZE * 2)

        # This stores the x, y coords that we're plotting to and the eg x,y coords of the tile we're plotting
        self.tile_map = []

        # Draw the empty map
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

        #  Add any old tiles, with no connections to the tiles to be plotted. Put them in the first empty space
        for tile, pos in self.old_tiles.items():
            if tile in self.tiles:
                continue
            if pos not in self.tiles.values():
                self.tiles[tile] = pos
                continue
            for row in range(self.map_dims[0]):
                for col in range(self.map_dims[1]):
                    if (col, row) not in self.tiles.values():
                        self.tiles[tile] = (col, row)
        self.old_tiles = {}

        for (eg_x, eg_y), (tile_x, tile_y) in self.tiles.items():
            if eg_x == None or eg_y == None:
                continue

            tile_x += x_offset
            tile_y += y_offset
            map, img = get_eg_tile_img(self, eg_x, eg_y, tile_x, tile_y)
            self.eg_tiles[(map,)] = (tile_x, tile_y)

        for door, data in doors_data.items():
            d_eg_x = int(data[0]) % 16
            d_eg_y = int(data[0]) // 16
            if (d_eg_x, d_eg_y) not in self.tiles_added:
                continue

            _data = create_door_dict(door)
            x1, y1 = get_final_door_coords(self, _data, "source", x_offset, y_offset)
            if door == "Sanctuary Mirror Route":
                continue
            self.door_buttons[door] = self.canvas.create_oval(
                x1 - 5,
                y1 - 5,
                x1 + 5,
                y1 + 5,
                fill="#0f0",
                width=2,
                activefill="red",
            )
            self.unlinked_doors.add(door)
            self.canvas.tag_bind(self.door_buttons[door], "<Button-1>", lambda event: select_location(self, event))
            self.canvas.tag_bind(self.door_buttons[door], "<Button-3>", lambda event: show_door_icons(self, event))

        # Display links between doors here
        doors_linked = set()
        for n, door_link in enumerate(self.door_links):
            x1, y1 = get_final_door_coords(self, door_link, "source", x_offset, y_offset)
            x2, y2 = get_final_door_coords(self, door_link, "linked", x_offset, y_offset)
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

            # TODO: Refactor this
            doors_linked.add(door_link["door"])
            doors_linked.add(door_link["linked_door"])
            try:
                self.unlinked_doors.remove(door_link["door"])
                self.unlinked_doors.remove(door_link["linked_door"])
            except KeyError:
                pass
            self.canvas.itemconfigure(self.door_buttons[door_link["door"]], fill="grey")
            self.canvas.itemconfigure(self.door_buttons[door_link["linked_door"]], fill="grey")

            if door_link["door"] in self.special_doors:
                icon_queue.append((self.special_doors[door_link["door"]], x1, y1, door_link["door"]))
            if door_link["linked_door"] in self.special_doors:
                icon_queue.append((self.special_doors[door_link["linked_door"]], x1, y1, door_link["linked_door"]))

        for n, lobby in enumerate(self.lobby_doors):
            x1, y1 = get_final_door_coords(self, lobby, "source", x_offset, y_offset)
            icon_queue.append(("Lobby Door", x1, y1, lobby["door"]))
            doors_linked.add(lobby["door"])
            doors_linked.add(lobby["lobby"])

        while icon_queue:
            icon, eg_x, eg_y, loc_name = icon_queue.pop()
            place_door_icon(self, icon, eg_x, eg_y, loc_name)

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
            link_data = create_door_dict(door)
            link_data.update(create_door_dict(linked_door, linked=True))
            self.door_links.append(link_data)
        except:
            print(f"Error adding door link for {door} and {linked_door}")

    def add_lobby_door(self, door, lobby):
        d_data = create_door_dict(door)
        d_data["lobby"] = lobby
        self.lobby_doors.append(d_data)

    def get_loc_by_button(self, button):
        for name, loc in self.door_buttons.items():
            if loc == button[0]:
                return name

    def show_door_icons(self, event):
        door = self.canvas.find_closest(event.x, event.y)
        loc_name = get_loc_by_button(self, door)
        selected_item = doors_sprite_data.show_sprites(self, top, event)
        if selected_item == "Lobby Door":
            lobby_number = len(self.lobby_doors)
            if self.sanc_dungeon:
                lobby_number -= 1
            lobby = dungeon_lobbies[tab_world][lobby_number]
            print(f"Adding lobby door for {loc_name} to {lobby} ({lobby_number}")
            add_lobby_door(self, loc_name, lobby)

            x_loc, y_loc = get_final_door_coords(self, self.lobby_doors[-1], "source", self.x_offset, self.y_offset)
        else:
            _data = create_door_dict(loc_name)
            x_loc, y_loc = get_final_door_coords(self, _data, "source", self.x_offset, self.y_offset)
            self.special_doors[loc_name] = selected_item

        place_door_icon(self, selected_item, x_loc, y_loc, loc_name)

    def place_door_icon(self, placed_icon, x_loc, y_loc, loc_name=None):
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
        if loc_name:
            self.placed_icons[(x_loc, y_loc)]["name"] = loc_name
        self.placed_icons[(x_loc, y_loc)]["image"] = self.canvas.create_image(
            x_loc,
            y_loc,
            image=self.placed_icons[(x_loc, y_loc)]["sprite"],
        )
        self.canvas.tag_bind(
            self.placed_icons[(x_loc, y_loc)]["image"],
            "<Button-3>",
            lambda event: remove_item(self, event),
        )

    def remove_item(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        self.canvas.delete(item)
        for loc, data in self.placed_icons.items():
            if data["image"] == item[0]:
                del self.special_doors[data["name"]]
                del self.placed_icons[loc]
                break

    def select_location(self, event):
        door = self.canvas.find_closest(event.x, event.y)

        # Catch when the user clicks on the world rather than a location
        if door[0] not in self.door_buttons.values():
            return

        # Get the location name from the button
        loc_name = get_loc_by_button(self, door)
        if loc_name in [x["door"] for x in self.door_links] + [x["linked_door"] for x in self.door_links] + [
            x["door"] for x in self.lobby_doors
        ]:
            return

        if self.select_state == SelectState.NoneSelected:
            self.canvas.itemconfigure(door, fill="orange")
            self.select_state = SelectState.SourceSelected
            self.source_location = door
        elif self.select_state == SelectState.SourceSelected:
            if has_target(self, loc_name):
                return
            add_door_link(self, get_loc_by_button(self, self.source_location), loc_name)
            x1, y1 = get_final_door_coords(self, self.door_links[-1], "source", self.x_offset, self.y_offset)
            x2, y2 = get_final_door_coords(self, self.door_links[-1], "linked", self.x_offset, self.y_offset)
            self.door_links[-1]["button"] = self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="black",
                width=2,
                arrow=BOTH,
                activefill="red",
            )
            self.select_state = SelectState.NoneSelected
            self.canvas.itemconfigure(self.door_buttons[loc_name], fill="grey")
            self.canvas.itemconfigure(self.source_location, fill="grey")

    def has_target(self, loc_name):
        return loc_name in self.door_links

    def return_connections(door_links, lobby_doors, special_doors):
        # print(lobby_doors)
        final_connections = {"doors": {}, "lobbies": {}}
        doors_type = "vanilla" if len(door_links) > 0 else False

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

            def hide_dont_close(self):
                eg_tile_window.grab_release()
                eg_tile_window.withdraw()

            eg_tile_window = Toplevel(self)
            eg_tile_window.wm_title("EG Tiles")
            eg_tile_window.protocol("WM_DELETE_WINDOW", lambda: hide_dont_close(self))
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
        if not hasattr(self, "selected_eg_tile"):
            return

        empty_tile = self.canvas.find_closest(event.x, event.y)
        tile_x, tile_y = self.eg_tiles[empty_tile]
        x, y = self.selected_eg_tile

        # Add clicked EG tile to clicked empty tile
        map, img = get_eg_tile_img(self, x, y, tile_x, tile_y)
        self.tiles[self.selected_eg_tile] = (tile_x - self.x_offset, tile_y - self.y_offset)

        self.setvar("selected_eg_tile", BooleanVar(value=False))
        delattr(self, "selected_eg_tile")

        # Draw any _new_ unlinked doors
        for door, data in doors_data.items():
            if (
                door
                not in [dl["door"] for dl in self.door_links]
                + [dl["linked_door"] for dl in self.door_links]
                + [ld["door"] for ld in self.lobby_doors]
                and door not in self.unlinked_doors
            ):
                d_eg_x = int(data[0]) % 16
                d_eg_y = int(data[0]) // 16
                if (d_eg_x, d_eg_y) not in self.tiles_added:
                    continue
                if door.startswith("Sanctuary") and not self.sanc_dungeon:
                    self.sanc_dungeon = True
                    print("Adding Sanctuary Mirror Route")
                    add_lobby_door(self, "Sanctuary Mirror Route", "Sanctuary")
                    x1, y1 = get_final_door_coords(
                        self, self.lobby_doors[-1], "source", self.x_offset, tile_y - self.y_offset
                    )
                    place_door_icon(self, "Lobby Door", x1, y1)

                _data = create_door_dict(door)

                x1, y1 = get_final_door_coords(self, _data, "source", self.x_offset, self.y_offset)
                self.door_buttons[door] = self.canvas.create_oval(
                    x1 - 5,
                    y1 - 5,
                    x1 + 5,
                    y1 + 5,
                    fill="#0f0",
                    width=2,
                    activefill="red",
                )
                self.unlinked_doors.add(door)
                self.canvas.tag_bind(self.door_buttons[door], "<Button-1>", lambda event: select_location(self, event))
                self.canvas.tag_bind(self.door_buttons[door], "<Button-3>", lambda event: show_door_icons(self, event))

    def create_door_dict(door, linked=False):
        d_data = get_door_coords(door)
        d_eg_x, d_eg_y = door_coordinates_key[door][0]
        d_t_x, d_t_y = self.tiles[(d_eg_x, d_eg_y)]
        data = {
            "linked_door" if linked else "door": door,
            "linked_tile" if linked else "source_tile": (d_t_x, d_t_y),
            "linked_coords" if linked else "source_coords": (d_data["x"], d_data["y"]),
        }
        return data

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
    self.cwidth = 1024
    self.cheight = 512
    # self.cwidth = 2048
    # self.cheight = 1024
    self.select_state = SelectState.NoneSelected
    if not eg_selection_mode:
        redraw_canvas_button = ttk.Button(self, text="Redraw Canvas", command=lambda: redraw_canvas(self))
        redraw_canvas_button.pack()
    if vanilla_data:
        self.tile_map = vanilla_data["tile_map"]
        # Original vanilla data was stored at 2048x1024, so we need to scale it down to the current size
        self.tile_size = int(vanilla_data["tile_size"] / 2048 * self.cwidth)
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
