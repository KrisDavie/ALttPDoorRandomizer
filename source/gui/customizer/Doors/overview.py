from dataclasses import dataclass
import pickle
from tkinter import BOTH, BooleanVar, Toplevel, ttk, NW, Canvas
from typing import List, Tuple, TypedDict, Union
import typing
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
    mandatory_tiles
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


class DoorData(TypedDict):
    door: str
    source_tile: tuple
    source_coords: tuple
    button: int


class DoorLink(DoorData):
    linked_door: str
    linked_tile: tuple
    linked_coords: tuple


class LobbyData(DoorData):
    lobby: str
    lobby_tile: tuple
    lobby_coords: tuple

class EGTileData(TypedDict):
    # Key =    eg_tile: Tuple[int, int]
    map_tile: Tuple[int, int]
    img_obj: ImageTk.PhotoImage
    button: int # TKinter button number


# These data structures drastically need to be cleaned up, but I'm not sure how to do it yet
class DoorPage(ttk.Frame):
    canvas: Canvas
    cwidth: int
    cheight: int
    tile_size: int
    map_dims: tuple[int, int]

    eg_tile_window: Union[Toplevel, None]
    eg_tile_window_notebook: Union[ttk.Notebook, None]
    eg_tile_multiuse: dict

    eg_selection_mode: bool
    select_state: SelectState
    redraw: bool

    doors: dict[str, str]
    inverse_doors: dict[str, str]

    tile_map: list
    disabled_tiles: dict
    door_links: List[DoorLink]
    lobby_doors: list[LobbyData]
    special_doors: dict
    placed_icons: dict
    unlinked_doors: set
    door_buttons: dict
    sanc_dungeon: bool
    old_tiles: dict
    tiles: dict[Tuple[int, int], EGTileData]
    unusued_map_tiles: dict
    eg_tile: Union[str, None]
    eg_tile_data: Union[dict, None]
    load_yaml: typing.Callable
    return_connections: typing.Callable
    y_offset: int
    x_offset: int
    source_location: tuple

def get_tile_data_by_map_tile(tiles: dict[Tuple[int, int], EGTileData], map_tile: Tuple[int, int]) -> Union[Tuple[int, int], None]:
    for eg_tile in tiles:
        if "map_tile" in tiles[eg_tile] and tiles[eg_tile]["map_tile"] == map_tile:
            return eg_tile
    return None

def get_tile_data_by_button(tiles: dict[Tuple[int, int], EGTileData], button: int) -> Union[Tuple[int, int], None]:
    for eg_tile in tiles:
        if 'button' in tiles[eg_tile] and tiles[eg_tile]["button"] == button:
            return eg_tile
    return None

def door_customizer_page(
    top,
    parent,
    tab_world,
    eg_img=None,
    eg_selection_mode=False,
    vanilla_data=None,
    plando_window=None,
) -> DoorPage:
    def init_page(self: DoorPage, redraw=False) -> None:
        self.select_state = SelectState.NoneSelected

        # Do we have a canvas already? If so, destroy it and make a new one
        if hasattr(self, "canvas"):
            self.canvas.destroy()
        self.canvas = Canvas(self, width=self.cwidth + (BORDER_SIZE * 2), height=self.cheight + (BORDER_SIZE * 2))
        self.canvas.pack()
        self.disabled_tiles = {}

        # Initialise the variables we need
        self.door_links = []
        self.doors = {}
        self.lobby_doors = []
        self.special_doors = {}
        self.placed_icons = defaultdict(dict)
        self.unlinked_doors = set()
        self.door_buttons = {}
        self.sanc_dungeon = False

        #  If we're redrawing, we need to keep tiles with no current connections, we store them temporarily in old_tiles
        if redraw:
            self.old_tiles = self.tiles.copy()
            self.redraw = True
        else:
            self.old_tiles = {}
            self.redraw = False

        # Are we plotting the vanilla map? If so, we need leave the vanilla data in place (added when the page is created)
        if not self.eg_selection_mode:
            self.tiles = defaultdict(dict) # type: ignore
            if not redraw:
                for n, tile in enumerate(mandatory_tiles[tab_world]):
                    self.tiles[tile] = {'map_tile': (n, 0)} # type: ignore
        else:
            self.tiles = defaultdict(dict, vanilla_data['tiles']) # type: ignore

        self.unusued_map_tiles = {}


    def redraw_canvas(self: DoorPage) -> None:
        yaml = return_connections(self.door_links, self.lobby_doors, self.special_doors)[0]
        load_yaml(self, yaml, redraw=True)

    def load_yaml(self: DoorPage, yaml_data: dict, redraw=False):
        
        doors_processed = set()
        door_links_to_make = set()
        doors_to_process: deque = deque()
        regions_processed = set()

        def queue_regions_doors(door: str, region=False):
            if not region:
                if door in doors_to_regions:
                    nd_region = doors_to_regions[door]
                else:
                    print("ERROR: Door not found in doors_to_regions", door)
                    return
            else:
                nd_region = door

            if nd_region in regions_processed:
                return

            region_doors = regions_to_doors[nd_region]

            # Add doors to queue
            for future_door in region_doors:
                if not (
                    future_door == door
                    or future_door in doors_processed
                    or future_door in doors_to_process
                    or future_door in regions_to_doors
                ):
                    doors_to_process.append(future_door)
            regions_processed.add(nd_region)


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
            if not lobby in yaml_data["lobbies"]:
                continue
            lobby_door = yaml_data["lobbies"][lobby]
            add_lobby(self, lobby_door, lobby)
            queue_regions_doors(lobby_door)

        if len(doors_to_process) == 0:
            for tile in mandatory_tiles[tab_world]:
                for door in door_coordinates[tile]:
                    doors_to_process.append(door["name"])

        while doors_to_process:
            next_door = doors_to_process.pop()
            if len(doors_to_process) == 0:
                for tile in mandatory_tiles[tab_world]:
                    for door in door_coordinates[tile]:
                        if door["name"] in doors_processed:
                            continue
                        doors_to_process.append(door["name"])

            if next_door in MANUAL_REGIONS_ADDED:
                queue_regions_doors(MANUAL_REGIONS_ADDED[next_door], region=True)

            doors_processed.add(next_door)
            door_tile_x, door_tile_y = get_doors_eg_tile(next_door)

            if (door_tile_x, door_tile_y) != (None, None):
                queue_regions_doors(next_door)
                door_links_to_make.add(next_door)
            else:
                if next_door not in self.doors:
                    print("ERROR: Door not found in doors", next_door)
                    continue
                _region = self.doors[next_door]
                if _region not in regions_to_doors:
                    print("ERROR: Region not found in regions_to_doors", _region)
                    queue_regions_doors(self.doors[next_door])
                else:
                    queue_regions_doors(self.doors[next_door], region=True)

            # Find the door that this door is linked to
            linked_door = None
            for d in [self.doors, self.inverse_doors]:
                if next_door in d:
                    linked_door = d[next_door]
                    if linked_door not in doors_processed and linked_door not in regions_to_doors:
                        doors_to_process.appendleft(linked_door)

            linked_door_x, linked_door_y = get_doors_eg_tile(linked_door)

            # (Is this a door) or (have we already added the tile)?
            if (door_tile_x, door_tile_y) == (None, None) or (door_tile_x, door_tile_y) in self.tiles:
                continue

            # PoD warp tile (Never seen but still linked, start from 0,0)
            if (linked_door_x, linked_door_y) in self.tiles:
                new_tile_x, new_tile_y = self.tiles[(linked_door_x, linked_door_y)]['map_tile']
            else:
                new_tile_x = new_tile_y = 0

            # Find closest unused map tile to place supertile in, respect directionality where possible
            direction = doors_data[next_door][1]
            last_cardinal = 0
            while get_tile_data_by_map_tile(self.tiles, (new_tile_x, new_tile_y)):
                if (direction == "We" and last_cardinal == 0) or (
                    ((direction == "No" or direction == "Up") or (direction == "So" or direction == "Dn"))
                    and last_cardinal == -1
                ):
                    new_tile_x += 1
                elif (direction == "Ea" and last_cardinal == 0) or (
                    ((direction == "No" or direction == "Up") or (direction == "So" or direction == "Dn"))
                    and last_cardinal == 1
                ):
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
            self.tiles[(door_tile_x, door_tile_y)]['map_tile'] = (new_tile_x, new_tile_y)

        for door in door_links_to_make:
            try:
                linked_door = self.doors[door] if door in self.doors else self.inverse_doors[door]
                add_door_link(self, door, linked_door)
            except KeyError:
                # Couldn't make link for {door}, possibly a lobby or unlinked
                pass
        for tile in mandatory_tiles[tab_world]:
            if tile not in self.tiles:
                self.tiles[tile]['map_tile'] = find_first_unused_tile()
                    
                            
        draw_map(self)
    
    def find_first_unused_tile():
        for row in range(self.map_dims[0]):
            for col in range(self.map_dims[1]):
                if not get_tile_data_by_map_tile(self.tiles, (col, row)):
                    return (col, row)


    def get_doors_eg_tile(door):
        # Coords are x = left -> right, y = top -> bottom, 0,0 is top left
        if door in doors_data:
            # (found, x, y)
            return (
                int(doors_data[door][0]) % 16,
                int(doors_data[door][0]) // 16,
            )
        else:
            return (None, None)
        
    def find_map_tile(map_tile: Tuple[int, int]):
        for eg_tile, tile_data in self.tiles.items():
            if tile_data['map_tile'] == map_tile:
                return eg_tile
        return None
    
    def get_min_max_map_tiles():
        min_x = min(self.tiles.values(), key=lambda x: x['map_tile'][0])['map_tile'][0]
        max_x = max(self.tiles.values(), key=lambda x: x['map_tile'][0])['map_tile'][0]
        min_y = min(self.tiles.values(), key=lambda x: x['map_tile'][1])['map_tile'][1]
        max_y = max(self.tiles.values(), key=lambda x: x['map_tile'][1])['map_tile'][1]
        return min_x, max_x, min_y, max_y

    def add_lobby(self: DoorPage, lobby_room: str, lobby: str):
        x, y = get_doors_eg_tile(lobby_room)

        if (x, y) in self.tiles:
            add_lobby_door(self, lobby_room, lobby)
            return
        if find_map_tile((0, 0)):
            min_x, max_x, min_y, max_y = get_min_max_map_tiles()
            if "East" in lobby_room:
                tile_x = max_x + 1
            else:
                tile_x = min_x - 1
            self.tiles[(x, y)]['map_tile'] = (tile_x, 0)
        else:
            self.tiles[(x, y)]['map_tile'] = (0, 0)
        add_lobby_door(self, lobby_room, lobby)

    def remove_eg_tile(self: DoorPage, event):
        button = self.canvas.find_closest(event.x, event.y)[0]
        eg_tile = get_tile_data_by_button(self.tiles, button)
        if not eg_tile:
            return
        del(self.tiles[eg_tile])
        top.eg_tile_multiuse[eg_tile] += 1
        for page in top.eg_tile_window.pages.values():
            if eg_tile in page.content.tiles:
                page.content.deactivate_tiles(page.content, top.eg_tile_multiuse, top.disabled_eg_tiles)

        
        # find doors in this tile:
        for door in door_coordinates[eg_tile]:
            if door['name'] in self.special_doors:
                del(self.special_doors[door['name']])
            _lobby_doors = [x['door'] for x in self.lobby_doors]
            if door['name'] in _lobby_doors:
                del(self.lobby_doors[_lobby_doors.index(door['name'])])
                continue
            while True:
                _dl_idx, _door_link = get_link_by_door(door["name"])  # type: ignore
                if not _door_link:
                    self.canvas.delete(self.door_buttons[door['name']])
                    break
                self.canvas.delete(_door_link["button"])  # type: ignore
                # Set colors back to normal
                if _door_link["door"] == door['name']:
                    self.canvas.itemconfigure(self.door_buttons[_door_link["linked_door"]], fill="#f00")
                    self.canvas.delete(self.door_buttons[_door_link["door"]])
                else:
                    self.canvas.itemconfigure(self.door_buttons[_door_link["door"]], fill="#0f0")
                    self.canvas.delete(self.door_buttons[_door_link["linked_door"]])
                del(self.door_links[_dl_idx])
                for _d in [_door_link["door"], _door_link["linked_door"]]:
                    if _d in self.special_doors:
                        del(self.special_doors[_d])

        draw_empty_map(self)

    def add_eg_tile_img(self: DoorPage, x, y, tile_x, tile_y, ci_kwargs={}):
        x1 = (tile_x * self.tile_size) + BORDER_SIZE + (((2 * tile_x + 1) - 1) * TILE_BORDER_SIZE)
        y1 = (tile_y * self.tile_size) + BORDER_SIZE + (((2 * tile_y + 1) - 1) * TILE_BORDER_SIZE)
        if not eg_selection_mode and 'img_obj' not in self.tiles[(x, y)]:
            top.eg_tile_multiuse[(x, y)] -= 1

        img = ImageTk.PhotoImage(
            eg_img.crop((x * 512, y * 512, (x + 1) * 512, (y + 1) * 512)).resize(
                (self.tile_size, self.tile_size), Image.ANTIALIAS
            )
        )
        map = self.canvas.create_image(x1, y1, image=img, anchor=NW, **ci_kwargs)
        if not self.eg_selection_mode:
            self.canvas.tag_bind(map, "<Button-3>", lambda event: remove_eg_tile(self, event))
        else:
            self.canvas.tag_bind(map, "<Button-1>", lambda event: select_eg_tile(self, top, event, plando_window))
        self.tiles[(x, y)]["img_obj"] = img
        self.tiles[(x, y)]["button"] = map
        return map

    def draw_vanilla_eg_map(self: DoorPage, top):
        for (eg_tile_x, eg_tile_y), tile_data in self.tiles.items():
            if tile_data["map_tile"] == None:
                continue
            x, y = tile_data["map_tile"]
            add_eg_tile_img(self,eg_tile_x, eg_tile_y, x + self.x_offset, y + self.y_offset)

    def get_door_coords(door):
        eg_tile, list_pos = door_coordinates_key[door]
        return door_coordinates[eg_tile][list_pos]

    def draw_empty_map(self: DoorPage):
        for row in range(self.map_dims[0]):
            for col in range(self.map_dims[1]):
                if get_tile_data_by_map_tile(self.tiles, (col - self.x_offset, row - self.y_offset)):
                    continue

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
                self.canvas.tag_lower(tile)
                self.unusued_map_tiles[(col, row)] = tile

    def draw_map(self: DoorPage):
        # x is columns, y is rows
        icon_queue = []
        if len(self.tiles) > 0:
            # Get the min x and y values
            min_x, max_x, min_y, max_y = get_min_max_map_tiles()
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

        #  Add any old tiles, with no connections to the tiles to be plotted. Put them in the first empty space
        for tile, tile_data in self.old_tiles.items():
            if tile in self.tiles or len(tile_data) == 0:
                continue
            # if not get_tile_data_by_map_tile(self.tiles, tile_data['map_tile']):
            #     self.tiles[tile]['map_tile'] = tile_data['map_tile']
            #     continue
            self.tiles[tile]['map_tile'] = find_first_unused_tile()
        self.old_tiles = {}

        for (eg_x, eg_y), tile_data in self.tiles.items():
            tile_x, tile_y = tile_data["map_tile"]
            if eg_x == None or eg_y == None:
                continue

            tile_x += x_offset
            tile_y += y_offset
            add_eg_tile_img(self, eg_x, eg_y, tile_x, tile_y)

        for door, data in doors_data.items():
            d_eg_x = int(data[0]) % 16
            d_eg_y = int(data[0]) // 16
            if "img_obj" not in self.tiles[(d_eg_x, d_eg_y)]:
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
            self.canvas.tag_bind(
                self.door_links[n]["button"], "<Button-3>", lambda event: remove_door_link(self, event)
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

        # Draw the empty map
        draw_empty_map(self)


    def get_final_door_coords(self: DoorPage, door, door_type, min_x, min_y):
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

    def add_door_link(self: DoorPage, door, linked_door):
        try:
            link_data = create_door_dict(door)
            link_data.update(create_door_dict(linked_door, linked=True))  # type: ignore
            self.door_links.append(link_data)
        except:
            print(f"Error adding door link for {door} and {linked_door}")

    def add_lobby_door(self: DoorPage, door, lobby):
        d_data = typing.cast(LobbyData, create_door_dict(door))
        d_data["lobby"] = lobby
        self.lobby_doors.append(d_data)

    def get_loc_by_button(self: DoorPage, button):
        for name, loc in self.door_buttons.items():
            if loc == button[0]:
                return name

    def show_door_icons(self: DoorPage, event):
        door = self.canvas.find_closest(event.x, event.y)
        loc_name = get_loc_by_button(self, door)
        selected_item = doors_sprite_data.show_sprites(self, top, event)
        if selected_item == "Lobby Door":
            lobby_number = len(self.lobby_doors)
            if self.sanc_dungeon:
                lobby_number -= 1
            if lobby_number == len(dungeon_lobbies[tab_world]):
                return
            lobby = dungeon_lobbies[tab_world][lobby_number]
            print(f"Adding lobby door for {loc_name} to {lobby} ({lobby_number}")
            add_lobby_door(self, loc_name, lobby)

            x_loc, y_loc = get_final_door_coords(self, self.lobby_doors[-1], "source", self.x_offset, self.y_offset)
        else:
            _data = create_door_dict(loc_name)
            x_loc, y_loc = get_final_door_coords(self, _data, "source", self.x_offset, self.y_offset)
            self.special_doors[loc_name] = selected_item

        place_door_icon(self, selected_item, x_loc, y_loc, loc_name)

    def place_door_icon(self: DoorPage, placed_icon, x_loc, y_loc, loc_name=None):
        # self.canvas.itemconfigure(item, state="hidden")

        # Place a new sprite
        if placed_icon == None:
            return
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

    def remove_item(self: DoorPage, event):
        item = self.canvas.find_closest(event.x, event.y)
        self.canvas.delete(item)  # type: ignore
        for loc, data in self.placed_icons.items():
            if data["image"] == item[0]:
                del self.special_doors[data["name"]]
                del self.placed_icons[loc]
                break

    def select_location(self: DoorPage, event):
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
            self.canvas.itemconfigure(door, fill="orange")  # type: ignore
            self.select_state = SelectState.SourceSelected
            self.source_location = door
        elif self.select_state == SelectState.SourceSelected:
            if has_target(self, loc_name) or self.source_location == door:
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
            self.canvas.tag_bind(
                self.door_links[-1]["button"], "<Button-3>", lambda event: remove_door_link(self, event)
            )
            self.select_state = SelectState.NoneSelected
            self.canvas.itemconfigure(self.door_buttons[loc_name], fill="grey")
            self.canvas.itemconfigure(self.source_location, fill="grey")  # type: ignore

    def has_target(self: DoorPage, loc_name):
        return loc_name in self.door_links

    def return_connections(door_links, lobby_doors, special_doors):
        # print(lobby_doors)
        final_connections = {"doors": {}, "lobbies": {}}
        doors_type = "vanilla" if len(door_links) > 0 else False

        for data in door_links:
            door = data["door"]
            linked_door = data["linked_door"]
            if "Drop Entrance" in door or "Drop Entrance" in linked_door:
                continue
            final_connections["doors"][door] = linked_door
            if door in special_doors:
                door_type = special_doors[door]
                final_connections["doors"][door] = {"dest": final_connections["doors"][door], "type": door_type}

        for lobby_data in lobby_doors:
            lobby = lobby_data["lobby"]
            if lobby == "Sanctuary_Mirror":
                continue
            lobby_door = lobby_data["door"]
            final_connections["lobbies"][lobby] = lobby_door

        return final_connections, doors_type

    def remove_door_link(self: DoorPage, event):
        link = self.canvas.find_closest(event.x, event.y)
        for data in self.door_links:
            if data["button"] == link[0]:
                self.door_links.remove(data)
                self.canvas.delete(link[0])  # type: ignore
                # Set colors back to normal
                self.canvas.itemconfigure(self.door_buttons[data["door"]], fill="#0f0")
                self.canvas.itemconfigure(self.door_buttons[data["linked_door"]], fill="#0f0")
                break

    def deactivate_tiles(self: DoorPage, eg_tile_multiuse, disabled_eg_tiles):
        for tile in self.tiles:
            if eg_tile_multiuse[tile] > 0:
                if tile in disabled_eg_tiles:
                    self.canvas.delete(disabled_eg_tiles[tile])  # type: ignore
                    del disabled_eg_tiles[tile]
                continue
            elif tile in disabled_eg_tiles:
                continue
            tile_x, tile_y = self.tiles[tile]["map_tile"]
            tile_x += self.x_offset
            tile_y += self.y_offset

            x1 = (tile_x * self.tile_size) + BORDER_SIZE + (((2 * tile_x + 1) - 1) * TILE_BORDER_SIZE)
            y1 = (tile_y * self.tile_size) + BORDER_SIZE + (((2 * tile_y + 1) - 1) * TILE_BORDER_SIZE)
            x2 = x1 + self.tile_size
            y2 = y1 + self.tile_size
            rect = self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="#888",
                stipple="gray25",
                state="disabled",
            )
            disabled_eg_tiles[tile] = rect

    def select_tile(self: DoorPage, event):
        parent.setvar("selected_eg_tile", BooleanVar(value=False))  # type: ignore
        for page in top.eg_tile_window.pages.values():
            page.content.deactivate_tiles(page.content, top.eg_tile_multiuse, top.disabled_eg_tiles)

        top.eg_tile_window.deiconify()
        top.eg_tile_window.focus_set()
        top.eg_tile_window.grab_set()
        # self.eg_tile_window.wait_visibility(self.eg_tile_window)
        parent.master.wait_variable("selected_eg_tile")
        if not hasattr(parent.master, "selected_eg_tile"):
            return
        selected_eg_tile =  parent.master.selected_eg_tile

        empty_tile_button = self.canvas.find_closest(event.x, event.y)[0]
        for (tile_x, tile_y), button in self.unusued_map_tiles.items():
            if button == empty_tile_button:
                break
        else:
            print(f'No empty tile found at {event.x}, {event.y}')
        x, y = selected_eg_tile

        # Add clicked EG tile to clicked empty tile this function IS needed
        add_eg_tile_img(self, x, y, tile_x, tile_y)
        self.tiles[selected_eg_tile]['map_tile'] = (tile_x - self.x_offset, tile_y - self.y_offset)

        parent.master.setvar("selected_eg_tile", BooleanVar(value=False))  # type: ignore
        delattr(parent.master, "selected_eg_tile")

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
                if "img_obj" not in self.tiles[(d_eg_x, d_eg_y)]:
                    continue
                if door.startswith("Sanctuary") and not self.sanc_dungeon:
                    self.sanc_dungeon = True
                    print("Adding Sanctuary Mirror Route")
                    add_lobby_door(self, "Sanctuary Mirror Route", "Sanctuary_Mirror")
                    x1, y1 = get_final_door_coords(
                        self, self.lobby_doors[-1], "source", self.x_offset, tile_y - self.y_offset
                    )
                    # place_door_icon(self, "Lobby Door", x1, y1)

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

    def create_door_dict(door, linked=False) -> DoorLink:
        d_data = get_door_coords(door)
        d_eg_x, d_eg_y = door_coordinates_key[door][0]
        d_t_x, d_t_y = self.tiles[(d_eg_x, d_eg_y)]['map_tile']
        data: DoorLink = {
            "linked_door" if linked else "door": door,  # type: ignore
            "linked_tile" if linked else "source_tile": (d_t_x, d_t_y),  # type: ignore
            "linked_coords" if linked else "source_coords": (d_data["x"], d_data["y"]),  # type: ignore
        }
        return data

    def get_link_by_door(door: str) -> Union[Tuple[int, DoorLink], Tuple[None, None]]:
        for n, link in enumerate(self.door_links):
            if link["door"] == door or link["linked_door"] == door:
                return n, link
        return None, None

    def select_eg_tile(self: DoorPage, top, event, parent):
        button = self.canvas.find_closest(event.x, event.y)[0]
        eg_tile = get_tile_data_by_button(self.tiles, button)
        if not eg_tile:
            return
        parent.selected_eg_tile = eg_tile
        parent.setvar("selected_eg_tile", BooleanVar(value=True))
        deactivate_tiles(self, top.eg_tile_multiuse, top.disabled_eg_tiles)

        top.eg_tile_window.grab_release()
        top.eg_tile_window.withdraw()

    self: DoorPage = typing.cast(DoorPage, ttk.Frame(parent))
    self.eg_selection_mode = eg_selection_mode
    self.eg_tile_window = None
    self.cwidth = 1024
    self.cheight = 512
    self.cwidth = 2048
    self.cheight = 1024
    self.select_state = SelectState.NoneSelected
    if not eg_selection_mode:
        redraw_canvas_button = ttk.Button(self, text="Redraw Canvas", command=lambda: redraw_canvas(self))
        redraw_canvas_button.pack()
    if vanilla_data:
        # Original vanilla data was stored at 2048x1024, so we need to scale it down to the current size
        self.tile_size = int(vanilla_data["tile_size"] / 2048 * self.cwidth)
        self.map_dims = vanilla_data["map_dims"]
        self.x_offset = vanilla_data["x_offset"]
        self.y_offset = vanilla_data["y_offset"]

    init_page(self)

    self.load_yaml = load_yaml
    self.return_connections = return_connections
    self.deactivate_tiles = deactivate_tiles

    #  If we're in eg selection mode, we need to use the special function to only draw tiles and not connections
    if self.eg_selection_mode:
        draw_vanilla_eg_map(self, top)
    else:
        redraw_canvas(self)
        # draw_map(self)


    # TODO: Add a new button to store this info somwhere as JSON for the generation
    return self
