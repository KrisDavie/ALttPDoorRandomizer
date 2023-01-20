from source.gui.customizer.worlds_data import World
from DoorShuffle import falldown_pits
from collections import defaultdict

# Doors data


def add_manual_drop(source, source_eg_tile, dest_eg_tile, dest_region=None):
    if dest_region is None:
        dest_region = dict(falldown_pits)[source]
    dest = f"{dest_region} Drop Entrance"
    doors_data[source] = (source_eg_tile, "Dn")
    doors_data[dest] = (dest_eg_tile, "Up")
    doors_to_regions[dest] = dest_region
    regions_to_doors[dest_region].append(dest)

    if source not in [x["name"] for x in door_coordinates[(source_eg_tile % 16, source_eg_tile // 16)]]:
        print(f"WARNING: {source} not in door_coordinates")
    if dest not in [x["name"] for x in door_coordinates[(dest_eg_tile % 16, dest_eg_tile // 16)]]:
        print(f"WARNING: {dest} not in door_coordinates")


# We use this to rename logical connectors to their actual, physical door
door_fix_map = {
    "Ice Cross Left Push Block": "Ice Cross Bottom SE",
    "Ice Cross Bottom Push Block Left": "Ice Cross Left WS",
    "Ice Cross Bottom Push Block Right": "Ice Cross Right ES",
    "Ice Cross Right Push Block Top": "Ice Cross Top NE",
    "Ice Cross Right Push Block Bottom": "Ice Cross Bottom SE",
    "Ice Cross Top Push Block Bottom": "Ice Cross Bottom SE",
    "Ice Cross Top Push Block Right": "Ice Cross Right ES",
}

doors_data = {}
with open("Doors.py", "r") as f:
    for line in f.readlines():
        direction = None
        room = None
        line = line.strip()
        if not line.startswith("create_door(player, "):
            continue
        method_data = line.split(").")
        door = method_data[0].split(", ")[1].strip().strip(" '\"").replace("\\", "")
        for d in method_data[1:]:
            if d.startswith("dir("):
                direction, room, _, _ = d[4:-1].split(", ")
        if room and direction:
            doors_data[door] = (int(room, 16), direction)

doors_data["Sanctuary Mirror Route"] = (18, "Up")

door_coordinates = {
    (1, 6): [
        {"x": 57, "y": 263, "loc_type": "door", "button": 9, "name": "Hyrule Castle Lobby W"},
        {"x": 453, "y": 264, "loc_type": "door", "button": 10, "name": "Hyrule Castle Lobby E"},
        {"x": 33, "y": 138, "loc_type": "door", "button": 11, "name": "Hyrule Castle Lobby WN"},
        {"x": 255, "y": 453, "loc_type": "door", "button": 12, "name": "Hyrule Castle Lobby S"},
        {"x": 256, "y": 50, "loc_type": "door", "button": 13, "name": "Hyrule Castle Lobby North Stairs"},
    ],
    (0, 6): [
        {"x": 454, "y": 264, "loc_type": "door", "button": 15, "name": "Hyrule Castle West Lobby E"},
        {"x": 383, "y": 73, "loc_type": "door", "button": 16, "name": "Hyrule Castle West Lobby N"},
        {"x": 477, "y": 136, "loc_type": "door", "button": 17, "name": "Hyrule Castle West Lobby EN"},
        {"x": 383, "y": 478, "loc_type": "door", "button": 18, "name": "Hyrule Castle West Lobby S"},
    ],
    (2, 6): [
        {"x": 58, "y": 264, "loc_type": "door", "button": 20, "name": "Hyrule Castle East Lobby W"},
        {"x": 256, "y": 50, "loc_type": "door", "button": 22, "name": "Hyrule Castle East Lobby N"},
        {"x": 127, "y": 74, "loc_type": "door", "button": 23, "name": "Hyrule Castle East Lobby NW"},
        {"x": 127, "y": 478, "loc_type": "door", "button": 24, "name": "Hyrule Castle East Lobby S"},
    ],
    (2, 5): [
        {"x": 57, "y": 136, "loc_type": "door", "button": 26, "name": "Hyrule Castle East Hall W"},
        {"x": 257, "y": 478, "loc_type": "door", "button": 28, "name": "Hyrule Castle East Hall S"},
        {"x": 127, "y": 454, "loc_type": "door", "button": 29, "name": "Hyrule Castle East Hall SW"},
    ],
    (0, 5): [
        {"x": 454, "y": 136, "loc_type": "door", "button": 31, "name": "Hyrule Castle West Hall E"},
        {"x": 383, "y": 454, "loc_type": "door", "button": 32, "name": "Hyrule Castle West Hall S"},
    ],
    (1, 0): [
        {"x": 56, "y": 136, "loc_type": "door", "button": 34, "name": "Hyrule Castle Back Hall W"},
        {"x": 454, "y": 136, "loc_type": "door", "button": 35, "name": "Hyrule Castle Back Hall E"},
        {"x": 255, "y": 96, "loc_type": "door", "button": 36, "name": "Hyrule Castle Back Hall Down Stairs"},
    ],
    (1, 5): [
        {"x": 256, "y": 51, "loc_type": "door", "button": 38, "name": "Hyrule Castle Throne Room N"},
        {"x": 255, "y": 455, "loc_type": "door", "button": 39, "name": "Hyrule Castle Throne Room South Stairs"},
    ],
    (2, 7): [
        {"x": 256, "y": 72, "loc_type": "door", "button": 41, "name": "Hyrule Dungeon Map Room Up Stairs"},
        {"x": 255, "y": 223, "loc_type": "door", "button": 42, "name": "Hyrule Dungeon Map Room Key Door S"},
        {"x": 255, "y": 306, "loc_type": "door", "button": 43, "name": "Hyrule Dungeon North Abyss Key Door N"},
        {"x": 176, "y": 511, "loc_type": "door", "button": 44, "name": "Hyrule Dungeon North Abyss South Edge"},
        {"x": 54, "y": 510, "loc_type": "door", "button": 45, "name": "Hyrule Dungeon North Abyss Catwalk Edge"},
    ],
    (2, 8): [
        {"x": 176, "y": 2, "loc_type": "door", "button": 47, "name": "Hyrule Dungeon South Abyss North Edge"},
        {"x": 2, "y": 404, "loc_type": "door", "button": 48, "name": "Hyrule Dungeon South Abyss West Edge"},
        {"x": 53, "y": 2, "loc_type": "door", "button": 49, "name": "Hyrule Dungeon South Abyss Catwalk North Edge"},
        {"x": 1, "y": 120, "loc_type": "door", "button": 50, "name": "Hyrule Dungeon South Abyss Catwalk West Edge"},
    ],
    (1, 8): [
        {"x": 510, "y": 118, "loc_type": "door", "button": 52, "name": "Hyrule Dungeon Guardroom Catwalk Edge"},
        {"x": 510, "y": 404, "loc_type": "door", "button": 53, "name": "Hyrule Dungeon Guardroom Abyss Edge"},
        {"x": 128, "y": 74, "loc_type": "door", "button": 54, "name": "Hyrule Dungeon Guardroom N"},
    ],
    (1, 7): [
        {"x": 127, "y": 451, "loc_type": "door", "button": 56, "name": "Hyrule Dungeon Armory S"},
        {"x": 194, "y": 392, "loc_type": "door", "button": 57, "name": "Hyrule Dungeon Armory ES"},
        {"x": 317, "y": 393, "loc_type": "door", "button": 58, "name": "Hyrule Dungeon Armory Boomerang WS"},
        {"x": 128, "y": 306, "loc_type": "door", "button": 59, "name": "Hyrule Dungeon Armory Interior Key Door N"},
        {"x": 127, "y": 221, "loc_type": "door", "button": 60, "name": "Hyrule Dungeon Armory Interior Key Door S"},
        {"x": 168, "y": 74, "loc_type": "door", "button": 61, "name": "Hyrule Dungeon Armory Down Stairs"},
    ],
    (0, 7): [
        {"x": 168, "y": 49, "loc_type": "door", "button": 63, "name": "Hyrule Dungeon Staircase Up Stairs"},
        {"x": 88, "y": 49, "loc_type": "door", "button": 64, "name": "Hyrule Dungeon Staircase Down Stairs"},
    ],
    (0, 8): [{"x": 89, "y": 48, "loc_type": "door", "button": 66, "name": "Hyrule Dungeon Cellblock Up Stairs"}],
    (1, 4): [
        {"x": 256, "y": 479, "loc_type": "door", "button": 68, "name": "Sewers Behind Tapestry S"},
        {"x": 432, "y": 50, "loc_type": "door", "button": 69, "name": "Sewers Behind Tapestry Down Stairs"},
    ],
    (2, 4): [
        {"x": 432, "y": 48, "loc_type": "door", "button": 71, "name": "Sewers Rope Room Up Stairs"},
        {"x": 255, "y": 49, "loc_type": "door", "button": 72, "name": "Sewers Rope Room North Stairs"},
    ],
    (2, 3): [
        {"x": 256, "y": 480, "loc_type": "door", "button": 74, "name": "Sewers Dark Cross South Stairs"},
        {"x": 255, "y": 49, "loc_type": "door", "button": 75, "name": "Sewers Dark Cross Key Door N"},
    ],
    (2, 2): [
        {"x": 255, "y": 479, "loc_type": "door", "button": 77, "name": "Sewers Water S"},
        {"x": 33, "y": 392, "loc_type": "door", "button": 78, "name": "Sewers Water W"},
    ],
    (1, 2): [
        {"x": 255, "y": 204, "loc_type": "door", "button": 80, "name": "Sewers Key Rat S"},
        {"x": 384, "y": 51, "loc_type": "door", "button": 81, "name": "Sewers Key Rat NE"},
        {"x": 255, "y": 302, "loc_type": "door", "button": 80, "name": "Sewers Dark Aquabats N"},
        {"x": 477, "y": 392, "loc_type": "door", "button": 81, "name": "Sewers Dark Aquabats ES"},
    ],
    (1, 1): [
        {"x": 383, "y": 478, "loc_type": "door", "button": 83, "name": "Sewers Secret Room Key Door S"},
        {"x": 291, "y": 393, "loc_type": "door", "button": 84, "name": "Sewers Rat Path WS"},
        {"x": 289, "y": 137, "loc_type": "door", "button": 85, "name": "Sewers Rat Path WN"},
        {"x": 222, "y": 395, "loc_type": "door", "button": 86, "name": "Sewers Secret Room ES"},
        {"x": 221, "y": 136, "loc_type": "door", "button": 87, "name": "Sewers Secret Room EN"},
        {"x": 383, "y": 49, "loc_type": "door", "button": 88, "name": "Sewers Secret Room Up Stairs"},
    ],
    (2, 0): [
        {"x": 383, "y": 75, "loc_type": "door", "button": 90, "name": "Sewers Pull Switch Down Stairs"},
        {"x": 253, "y": 195, "loc_type": "door", "button": 91, "name": "Sewers Yet More Rats S"},
        {"x": 256, "y": 327, "loc_type": "door", "button": 92, "name": "Sewers Pull Switch N"},
        {"x": 256, "y": 455, "loc_type": "door", "button": 93, "name": "Sewers Pull Switch S"},
    ],
    (2, 1): [
        {"x": 255, "y": 74, "loc_type": "door", "button": 95, "name": "Sanctuary N"},
        {"x": 256, "y": 204, "loc_type": "door", "button": 96, "name": "Sanctuary Mirror Route"},
        {"x": 256, "y": 454, "loc_type": "door", "button": 96, "name": "Sanctuary S"},
    ],
    (9, 12): [
        {"x": 255, "y": 483, "loc_type": "door", "button": 98, "name": "Eastern Lobby S"},
        {"x": 256, "y": 304, "loc_type": "door", "button": 99, "name": "Eastern Lobby N"},
        {"x": 256, "y": 224, "loc_type": "door", "button": 100, "name": "Eastern Lobby Bridge S"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 101, "name": "Eastern Lobby NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 102, "name": "Eastern Lobby Left Ledge SW"},
        {"x": 384, "y": 306, "loc_type": "door", "button": 103, "name": "Eastern Lobby NE"},
        {"x": 383, "y": 223, "loc_type": "door", "button": 104, "name": "Eastern Lobby Right Ledge SE"},
        {"x": 256, "y": 50, "loc_type": "door", "button": 105, "name": "Eastern Lobby Bridge N"},
    ],
    (9, 11): [
        {"x": 255, "y": 479, "loc_type": "door", "button": 107, "name": "Eastern Cannonball S"},
        {"x": 255, "y": 49, "loc_type": "door", "button": 108, "name": "Eastern Cannonball N"},
        {"x": 33, "y": 136, "loc_type": "door", "button": 109, "name": "Eastern Cannonball Ledge WN"},
        {"x": 477, "y": 135, "loc_type": "door", "button": 110, "name": "Eastern Cannonball Ledge Key Door EN"},
    ],
    (9, 10): [
        {"x": 256, "y": 478, "loc_type": "door", "button": 142, "name": "Eastern Courtyard Ledge S"},
        {"x": 31, "y": 263, "loc_type": "door", "button": 143, "name": "Eastern Courtyard Ledge W"},
        {"x": 478, "y": 264, "loc_type": "door", "button": 144, "name": "Eastern Courtyard Ledge E"},
        {"x": 57, "y": 136, "loc_type": "door", "button": 145, "name": "Eastern Courtyard WN"},
        {"x": 454, "y": 136, "loc_type": "door", "button": 146, "name": "Eastern Courtyard EN"},
        {"x": 255, "y": 51, "loc_type": "door", "button": 147, "name": "Eastern Courtyard N"},
    ],
    (10, 10): [
        {"x": 33, "y": 266, "loc_type": "door", "button": 149, "name": "Eastern East Wing W"},
        {"x": 221, "y": 137, "loc_type": "door", "button": 150, "name": "Eastern East Wing EN"},
        {"x": 290, "y": 136, "loc_type": "door", "button": 151, "name": "Eastern Pot Switch WN"},
        {"x": 222, "y": 392, "loc_type": "door", "button": 152, "name": "Eastern East Wing ES"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 153, "name": "Eastern Map Balcony WS"},
        {"x": 383, "y": 223, "loc_type": "door", "button": 154, "name": "Eastern Pot Switch SE"},
        {"x": 384, "y": 304, "loc_type": "door", "button": 155, "name": "Eastern Map Room NE"},
        {"x": 57, "y": 137, "loc_type": "door", "button": 156, "name": "Eastern Map Valley WN"},
        {"x": 127, "y": 479, "loc_type": "door", "button": 157, "name": "Eastern Map Valley SW"},
    ],
    (8, 10): [
        {"x": 477, "y": 265, "loc_type": "door", "button": 132, "name": "Eastern West Wing E"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 133, "name": "Eastern West Wing WS"},
        {"x": 220, "y": 394, "loc_type": "door", "button": 134, "name": "Eastern Stalfos Spawn ES"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 135, "name": "Eastern Stalfos Spawn NW"},
        {"x": 128, "y": 224, "loc_type": "door", "button": 136, "name": "Eastern Compass Room SW"},
        {"x": 193, "y": 137, "loc_type": "door", "button": 137, "name": "Eastern Compass Room EN"},
        {"x": 313, "y": 136, "loc_type": "door", "button": 138, "name": "Eastern Hint Tile WN"},
        {"x": 454, "y": 135, "loc_type": "door", "button": 139, "name": "Eastern Hint Tile EN"},
        {"x": 384, "y": 477, "loc_type": "door", "button": 140, "name": "Eastern Hint Tile Blocked Path SE"},
    ],
    (10, 11): [
        {"x": 127, "y": 50, "loc_type": "door", "button": 159, "name": "Eastern Dark Square NW"},
        {"x": 35, "y": 136, "loc_type": "door", "button": 160, "name": "Eastern Dark Square Key Door WN"},
        {"x": 220, "y": 137, "loc_type": "door", "button": 161, "name": "Eastern Dark Square EN"},
        {"x": 291, "y": 136, "loc_type": "door", "button": 162, "name": "Eastern Dark Pots WN"},
    ],
    (8, 11): [
        {"x": 479, "y": 135, "loc_type": "door", "button": 164, "name": "Eastern Big Key EN"},
        {"x": 383, "y": 51, "loc_type": "door", "button": 165, "name": "Eastern Big Key NE"},
    ],
    (9, 9): [
        {"x": 255, "y": 479, "loc_type": "door", "button": 167, "name": "Eastern Darkness S"},
        {"x": 385, "y": 306, "loc_type": "door", "button": 168, "name": "Eastern Darkness NE"},
        {"x": 384, "y": 223, "loc_type": "door", "button": 169, "name": "Eastern Rupees SE"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 170, "name": "Eastern Darkness Up Stairs"},
    ],
    (10, 13): [
        {"x": 127, "y": 305, "loc_type": "door", "button": 172, "name": "Eastern Attic Start Down Stairs"},
        {"x": 32, "y": 392, "loc_type": "door", "button": 173, "name": "Eastern Attic Start WS"},
    ],
    (9, 13): [
        {"x": 478, "y": 392, "loc_type": "door", "button": 175, "name": "Eastern False Switches ES"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 176, "name": "Eastern False Switches WS"},
        {"x": 221, "y": 394, "loc_type": "door", "button": 177, "name": "Eastern Cannonball Hell ES"},
        {"x": 33, "y": 392, "loc_type": "door", "button": 178, "name": "Eastern Cannonball Hell WS"},
    ],
    (8, 13): [
        {"x": 479, "y": 393, "loc_type": "door", "button": 180, "name": "Eastern Single Eyegore ES"},
        {"x": 383, "y": 305, "loc_type": "door", "button": 181, "name": "Eastern Single Eyegore NE"},
        {"x": 383, "y": 222, "loc_type": "door", "button": 182, "name": "Eastern Duo Eyegores SE"},
        {"x": 383, "y": 48, "loc_type": "door", "button": 183, "name": "Eastern Duo Eyegores NE"},
    ],
    (8, 12): [{"x": 384, "y": 479, "loc_type": "door", "button": 185, "name": "Eastern Boss SE"}],
    (4, 8): [
        {"x": 255, "y": 479, "loc_type": "door", "button": 187, "name": "Desert Main Lobby S"},
        {"x": 64, "y": 2, "loc_type": "door", "button": 188, "name": "Desert Main Lobby NW Edge"},
        {"x": 254, "y": 3, "loc_type": "door", "button": 189, "name": "Desert Main Lobby N Edge"},
        {"x": 448, "y": 2, "loc_type": "door", "button": 190, "name": "Desert Main Lobby NE Edge"},
        {"x": 510, "y": 144, "loc_type": "door", "button": 191, "name": "Desert Main Lobby E Edge"},
    ],
    (4, 7): [
        {"x": 255, "y": 509, "loc_type": "door", "button": 210, "name": "Desert Dead End Edge"},
        {"x": 447, "y": 508, "loc_type": "door", "button": 211, "name": "Desert North Hall SE Edge"},
        {"x": 62, "y": 509, "loc_type": "door", "button": 212, "name": "Desert North Hall SW Edge"},
        {"x": 2, "y": 336, "loc_type": "door", "button": 213, "name": "Desert North Hall W Edge"},
        {"x": 511, "y": 337, "loc_type": "door", "button": 214, "name": "Desert North Hall E Edge"},
        {"x": 127, "y": 305, "loc_type": "door", "button": 215, "name": "Desert North Hall NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 216, "name": "Desert Map SW"},
        {"x": 383, "y": 305, "loc_type": "door", "button": 217, "name": "Desert North Hall NE"},
        {"x": 384, "y": 222, "loc_type": "door", "button": 218, "name": "Desert Map SE"},
    ],
    (5, 8): [
        {"x": 2, "y": 177, "loc_type": "door", "button": 195, "name": "Desert East Wing W Edge"},
        {"x": 129, "y": 2, "loc_type": "door", "button": 196, "name": "Desert East Wing N Edge"},
        {"x": 384, "y": 481, "loc_type": "door", "button": 197, "name": "Desert East Lobby S"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 198, "name": "Desert East Lobby WS"},
        {"x": 222, "y": 393, "loc_type": "door", "button": 199, "name": "Desert East Wing ES"},
        {"x": 222, "y": 135, "loc_type": "door", "button": 200, "name": "Desert East Wing Key Door EN"},
        {"x": 290, "y": 136, "loc_type": "door", "button": 201, "name": "Desert Compass Key Door WN"},
        {"x": 383, "y": 50, "loc_type": "door", "button": 202, "name": "Desert Compass NW"},
    ],
    (5, 7): [
        {"x": 384, "y": 479, "loc_type": "door", "button": 204, "name": "Desert Cannonball S"},
        {"x": 128, "y": 510, "loc_type": "door", "button": 205, "name": "Desert Arrow Pot Corner S Edge"},
        {"x": 2, "y": 337, "loc_type": "door", "button": 206, "name": "Desert Arrow Pot Corner W Edge"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 207, "name": "Desert Arrow Pot Corner NW"},
        {"x": 127, "y": 223, "loc_type": "door", "button": 208, "name": "Desert Trap Room SW"},
    ],
    (3, 7): [
        {"x": 449, "y": 510, "loc_type": "door", "button": 220, "name": "Desert Sandworm Corner S Edge"},
        {"x": 511, "y": 336, "loc_type": "door", "button": 221, "name": "Desert Sandworm Corner E Edge"},
        {"x": 383, "y": 305, "loc_type": "door", "button": 222, "name": "Desert Sandworm Corner NE"},
        {"x": 383, "y": 222, "loc_type": "door", "button": 223, "name": "Desert Bonk Torch SE"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 224, "name": "Desert Sandworm Corner WS"},
        {"x": 223, "y": 392, "loc_type": "door", "button": 225, "name": "Desert Circle of Pots ES"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 226, "name": "Desert Circle of Pots NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 227, "name": "Desert Big Chest SW"},
    ],
    (3, 8): [
        {"x": 449, "y": 3, "loc_type": "door", "button": 229, "name": "Desert West Wing N Edge"},
        {"x": 289, "y": 392, "loc_type": "door", "button": 230, "name": "Desert West Wing WS"},
        {"x": 127, "y": 483, "loc_type": "door", "button": 231, "name": "Desert West S"},
        {"x": 221, "y": 392, "loc_type": "door", "button": 232, "name": "Desert West Lobby ES"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 233, "name": "Desert West Lobby NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 234, "name": "Desert Fairy Fountain SW"},
    ],
    (3, 6): [
        {"x": 127, "y": 481, "loc_type": "door", "button": 236, "name": "Desert Back Lobby S"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 237, "name": "Desert Back Lobby NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 238, "name": "Desert Tiles 1 SW"},
        {"x": 128, "y": 50, "loc_type": "door", "button": 239, "name": "Desert Tiles 1 Up Stairs"},
    ],
    (3, 5): [
        {"x": 127, "y": 48, "loc_type": "door", "button": 241, "name": "Desert Bridge Down Stairs"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 242, "name": "Desert Bridge SW"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 243, "name": "Desert Four Statues NW"},
        {"x": 223, "y": 392, "loc_type": "door", "button": 244, "name": "Desert Four Statues ES"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 245, "name": "Desert Beamos Hall WS"},
        {"x": 383, "y": 50, "loc_type": "door", "button": 246, "name": "Desert Beamos Hall NE"},
    ],
    (3, 4): [
        {"x": 383, "y": 479, "loc_type": "door", "button": 248, "name": "Desert Tiles 2 SE"},
        {"x": 383, "y": 306, "loc_type": "door", "button": 249, "name": "Desert Tiles 2 NE"},
        {"x": 384, "y": 222, "loc_type": "door", "button": 250, "name": "Desert Wall Slide SE"},
        {"x": 77, "y": 49, "loc_type": "door", "button": 251, "name": "Desert Wall Slide NW"},
    ],
    (3, 3): [{"x": 127, "y": 479, "loc_type": "door", "button": 253, "name": "Desert Boss SW"}],
    (7, 7): [
        {"x": 255, "y": 454, "loc_type": "door", "button": 255, "name": "Hera Lobby S"},
        {"x": 143, "y": 345, "loc_type": "door", "button": 256, "name": "Hera Lobby Down Stairs"},
        {"x": 127, "y": 74, "loc_type": "door", "button": 257, "name": "Hera Lobby Key Stairs"},
        {"x": 367, "y": 344, "loc_type": "door", "button": 258, "name": "Hera Lobby Up Stairs"},
    ],
    (7, 8): [
        {"x": 143, "y": 320, "loc_type": "door", "button": 260, "name": "Hera Basement Cage Up Stairs"},
        {"x": 128, "y": 48, "loc_type": "door", "button": 261, "name": "Hera Tile Room Up Stairs"},
        {"x": 223, "y": 137, "loc_type": "door", "button": 262, "name": "Hera Tile Room EN"},
        {"x": 289, "y": 137, "loc_type": "door", "button": 263, "name": "Hera Tridorm WN"},
        {"x": 384, "y": 222, "loc_type": "door", "button": 264, "name": "Hera Tridorm SE"},
        {"x": 383, "y": 305, "loc_type": "door", "button": 265, "name": "Hera Torches NE"},
    ],
    (1, 3): [
        {"x": 367, "y": 321, "loc_type": "door", "button": 267, "name": "Hera Beetles Down Stairs"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 268, "name": "Hera Beetles WS"},
        {"x": 221, "y": 392, "loc_type": "door", "button": 269, "name": "Hera Startile Corner ES"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 270, "name": "Hera Startile Corner NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 271, "name": "Hera Startile Wide SW"},
        {"x": 447, "y": 129, "loc_type": "door", "button": 272, "name": "Hera Startile Wide Up Stairs"},
    ],
    (7, 2): [
        {"x": 446, "y": 129, "loc_type": "door", "button": 274, "name": "Hera 4F Down Stairs"},
        {"x": 63, "y": 129, "loc_type": "door", "button": 275, "name": "Hera 4F Up Stairs"},
    ],
    (7, 1): [
        {"x": 63, "y": 129, "loc_type": "door", "button": 277, "name": "Hera 5F Down Stairs"},
        {"x": 431, "y": 129, "loc_type": "door", "button": 278, "name": "Hera 5F Up Stairs"},
    ],
    (7, 0): [{"x": 431, "y": 129, "loc_type": "door", "button": 280, "name": "Hera Boss Down Stairs"}],
    (0, 14): [
        {"x": 127, "y": 482, "loc_type": "door", "button": 282, "name": "Tower Lobby S"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 283, "name": "Tower Lobby NW"},
        {"x": 128, "y": 224, "loc_type": "door", "button": 284, "name": "Tower Gold Knights SW"},
        {"x": 223, "y": 135, "loc_type": "door", "button": 285, "name": "Tower Gold Knights EN"},
        {"x": 289, "y": 136, "loc_type": "door", "button": 286, "name": "Tower Room 03 WN"},
        {"x": 383, "y": 50, "loc_type": "door", "button": 287, "name": "Tower Room 03 Up Stairs"},
    ],
    (0, 13): [
        {"x": 383, "y": 50, "loc_type": "door", "button": 289, "name": "Tower Lone Statue Down Stairs"},
        {"x": 290, "y": 136, "loc_type": "door", "button": 290, "name": "Tower Lone Statue WN"},
        {"x": 219, "y": 136, "loc_type": "door", "button": 291, "name": "Tower Dark Maze EN"},
        {"x": 222, "y": 392, "loc_type": "door", "button": 292, "name": "Tower Dark Maze ES"},
        {"x": 289, "y": 392, "loc_type": "door", "button": 293, "name": "Tower Dark Chargers WS"},
        {"x": 416, "y": 306, "loc_type": "door", "button": 294, "name": "Tower Dark Chargers Up Stairs"},
    ],
    (0, 12): [
        {"x": 415, "y": 307, "loc_type": "door", "button": 296, "name": "Tower Dual Statues Down Stairs"},
        {"x": 290, "y": 393, "loc_type": "door", "button": 297, "name": "Tower Dual Statues WS"},
        {"x": 219, "y": 393, "loc_type": "door", "button": 298, "name": "Tower Dark Pits ES"},
        {"x": 220, "y": 137, "loc_type": "door", "button": 299, "name": "Tower Dark Pits EN"},
        {"x": 288, "y": 136, "loc_type": "door", "button": 300, "name": "Tower Dark Archers WN"},
        {"x": 384, "y": 50, "loc_type": "door", "button": 301, "name": "Tower Dark Archers Up Stairs"},
    ],
    (0, 11): [
        {"x": 383, "y": 49, "loc_type": "door", "button": 303, "name": "Tower Red Spears Down Stairs"},
        {"x": 287, "y": 136, "loc_type": "door", "button": 304, "name": "Tower Red Spears WN"},
        {"x": 221, "y": 136, "loc_type": "door", "button": 305, "name": "Tower Red Guards EN"},
        {"x": 127, "y": 224, "loc_type": "door", "button": 306, "name": "Tower Red Guards SW"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 307, "name": "Tower Circle of Pots NW"},
        {"x": 222, "y": 392, "loc_type": "door", "button": 308, "name": "Tower Circle of Pots ES"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 309, "name": "Tower Pacifist Run WS"},
        {"x": 415, "y": 305, "loc_type": "door", "button": 310, "name": "Tower Pacifist Run Up Stairs"},
    ],
    (0, 4): [
        {"x": 415, "y": 329, "loc_type": "door", "button": 312, "name": "Tower Push Statue Down Stairs"},
        {"x": 313, "y": 392, "loc_type": "door", "button": 313, "name": "Tower Push Statue WS"},
        {"x": 193, "y": 394, "loc_type": "door", "button": 314, "name": "Tower Catwalk ES"},
        {"x": 128, "y": 48, "loc_type": "door", "button": 315, "name": "Tower Catwalk North Stairs"},
    ],
    (0, 3): [
        {"x": 127, "y": 480, "loc_type": "door", "button": 317, "name": "Tower Antechamber South Stairs"},
        {"x": 129, "y": 306, "loc_type": "door", "button": 318, "name": "Tower Antechamber NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 319, "name": "Tower Altar SW"},
        {"x": 127, "y": 50, "loc_type": "door", "button": 320, "name": "Tower Altar NW"},
    ],
    (0, 2): [{"x": 128, "y": 480, "loc_type": "door", "button": 322, "name": "Tower Agahnim 1 SW"}],
    (10, 4): [
        {"x": 256, "y": 480, "loc_type": "door", "button": 324, "name": "PoD Lobby S"},
        {"x": 255, "y": 306, "loc_type": "door", "button": 325, "name": "PoD Lobby N"},
        {"x": 127, "y": 305, "loc_type": "door", "button": 326, "name": "PoD Lobby NW"},
        {"x": 384, "y": 304, "loc_type": "door", "button": 327, "name": "PoD Lobby NE"},
        {"x": 127, "y": 223, "loc_type": "door", "button": 328, "name": "PoD Left Cage SW"},
        {"x": 255, "y": 220, "loc_type": "door", "button": 329, "name": "PoD Middle Cage S"},
        {"x": 384, "y": 221, "loc_type": "door", "button": 330, "name": "PoD Middle Cage SE"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 331, "name": "PoD Left Cage Down Stairs"},
        {"x": 383, "y": 50, "loc_type": "door", "button": 333, "name": "PoD Middle Cage Down Stairs"},
        {"x": 255, "y": 50, "loc_type": "door", "button": 334, "name": "PoD Middle Cage N"},
    ],
    (9, 0): [
        {"x": 128, "y": 49, "loc_type": "door", "button": 336, "name": "PoD Shooter Room Up Stairs"},
        {"x": 384, "y": 49, "loc_type": "door", "button": 337, "name": "PoD Warp Room Up Stairs"},
    ],
    (10, 3): [
        {"x": 256, "y": 478, "loc_type": "door", "button": 339, "name": "PoD Pit Room S"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 340, "name": "PoD Pit Room NW"},
        {"x": 383, "y": 50, "loc_type": "door", "button": 341, "name": "PoD Pit Room NE"},
        {"x": 255, "y": 50, "loc_type": "door", "button": 342, "name": "PoD Big Key Landing Down Stairs"},
        {"x": 130, "y": 202, "loc_type": "door", "button": 340, "name": "PoD Pit Room Bomb Hole"},
        {"x": 385, "y": 226, "loc_type": "door", "button": 341, "name": "PoD Pit Room Freefall"},
    ],
    (10, 0): [
        {"x": 255, "y": 50, "loc_type": "door", "button": 344, "name": "PoD Basement Ledge Up Stairs"},
        {"x": 130, "y": 202, "loc_type": "door", "button": 344, "name": "PoD Basement Ledge Drop Entrance"},
        {"x": 385, "y": 226, "loc_type": "door", "button": 344, "name": "PoD Stalfos Basement Drop Entrance"},
    ],
    (10, 2): [
        {"x": 127, "y": 479, "loc_type": "door", "button": 346, "name": "PoD Arena Main SW"},
        {"x": 384, "y": 478, "loc_type": "door", "button": 347, "name": "PoD Arena Bridge SE"},
        {"x": 127, "y": 50, "loc_type": "door", "button": 349, "name": "PoD Arena Main NW"},
        {"x": 384, "y": 49, "loc_type": "door", "button": 350, "name": "PoD Arena Main NE"},
        {"x": 455, "y": 264, "loc_type": "door", "button": 351, "name": "PoD Arena Crystals E"},
        {"x": 474, "y": 392, "loc_type": "door", "button": 352, "name": "PoD Arena Ledge ES"},
    ],
    (11, 2): [
        {"x": 57, "y": 265, "loc_type": "door", "button": 354, "name": "PoD Sexy Statue W"},
        {"x": 127, "y": 48, "loc_type": "door", "button": 355, "name": "PoD Sexy Statue NW"},
        {"x": 38, "y": 392, "loc_type": "door", "button": 356, "name": "PoD Map Balcony WS"},
        {"x": 128, "y": 479, "loc_type": "door", "button": 357, "name": "PoD Map Balcony South Stairs"},
    ],
    (11, 3): [
        {"x": 127, "y": 48, "loc_type": "door", "button": 359, "name": "PoD Conveyor North Stairs"},
        {"x": 127, "y": 480, "loc_type": "door", "button": 360, "name": "PoD Conveyor SW"},
    ],
    (11, 4): [
        {"x": 127, "y": 48, "loc_type": "door", "button": 362, "name": "PoD Mimics 1 NW"},
        {"x": 128, "y": 219, "loc_type": "door", "button": 363, "name": "PoD Mimics 1 SW"},
        {"x": 127, "y": 305, "loc_type": "door", "button": 364, "name": "PoD Jelly Hall NW"},
        {"x": 384, "y": 307, "loc_type": "door", "button": 365, "name": "PoD Jelly Hall NE"},
        {"x": 384, "y": 221, "loc_type": "door", "button": 366, "name": "PoD Warp Hint SE"},
    ],
    (10, 1): [
        {"x": 127, "y": 478, "loc_type": "door", "button": 377, "name": "PoD Falling Bridge SW"},
        {"x": 34, "y": 136, "loc_type": "door", "button": 378, "name": "PoD Falling Bridge WN"},
        {"x": 222, "y": 136, "loc_type": "door", "button": 379, "name": "PoD Falling Bridge EN"},
        {"x": 37, "y": 264, "loc_type": "door", "button": 380, "name": "PoD Big Chest Balcony W"},
        {"x": 289, "y": 135, "loc_type": "door", "button": 381, "name": "PoD Compass Room WN"},
        {"x": 383, "y": 221, "loc_type": "door", "button": 382, "name": "PoD Compass Room SE"},
        {"x": 384, "y": 306, "loc_type": "door", "button": 383, "name": "PoD Harmless Hellway NE"},
        {"x": 383, "y": 478, "loc_type": "door", "button": 384, "name": "PoD Harmless Hellway SE"},
        {"x": 335, "y": 50, "loc_type": "door", "button": 385, "name": "PoD Compass Room W Down Stairs"},
        {"x": 430, "y": 51, "loc_type": "door", "button": 386, "name": "PoD Compass Room E Down Stairs"},
    ],
    (9, 1): [
        {"x": 477, "y": 136, "loc_type": "door", "button": 374, "name": "PoD Dark Maze EN"},
        {"x": 474, "y": 264, "loc_type": "door", "button": 375, "name": "PoD Dark Maze E"},
    ],
    (10, 6): [
        {"x": 335, "y": 51, "loc_type": "door", "button": 388, "name": "PoD Dark Basement W Up Stairs"},
        {"x": 432, "y": 49, "loc_type": "door", "button": 389, "name": "PoD Dark Basement E Up Stairs"},
        {"x": 383, "y": 51, "loc_type": "door", "button": 390, "name": "PoD Dark Alley NE"},
    ],
    (11, 1): [
        {"x": 127, "y": 477, "loc_type": "door", "button": 392, "name": "PoD Mimics 2 SW"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 393, "name": "PoD Mimics 2 NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 394, "name": "PoD Bow Statue SW"},
        {"x": 394, "y": 93, "loc_type": "door", "button": 395, "name": "PoD Bow Statue Down Ladder"},
    ],
    (11, 0): [
        {"x": 408, "y": 106, "loc_type": "door", "button": 397, "name": "PoD Dark Pegs Up Ladder"},
        {"x": 289, "y": 135, "loc_type": "door", "button": 398, "name": "PoD Dark Pegs WN"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 399, "name": "PoD Lonely Turtle SW"},
        {"x": 220, "y": 135, "loc_type": "door", "button": 400, "name": "PoD Lonely Turtle EN"},
        {"x": 223, "y": 392, "loc_type": "door", "button": 401, "name": "PoD Turtle Party ES"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 402, "name": "PoD Turtle Party NW"},
        {"x": 289, "y": 391, "loc_type": "door", "button": 403, "name": "PoD Callback WS"},
    ],
    (10, 5): [{"x": 383, "y": 479, "loc_type": "door", "button": 405, "name": "PoD Boss SE"}],
    (8, 2): [
        {"x": 256, "y": 479, "loc_type": "door", "button": 407, "name": "Swamp Lobby S"},
        {"x": 127, "y": 50, "loc_type": "door", "button": 408, "name": "Swamp Entrance Down Stairs"},
    ],
    (8, 3): [
        {"x": 127, "y": 49, "loc_type": "door", "button": 410, "name": "Swamp Pot Row Up Stairs"},
        {"x": 36, "y": 136, "loc_type": "door", "button": 411, "name": "Swamp Pot Row WN"},
        {"x": 35, "y": 391, "loc_type": "door", "button": 412, "name": "Swamp Pot Row WS"},
    ],
    (7, 3): [
        {"x": 476, "y": 137, "loc_type": "door", "button": 414, "name": "Swamp Map Ledge EN"},
        {"x": 477, "y": 392, "loc_type": "door", "button": 415, "name": "Swamp Trench 1 Approach ES"},
        {"x": 254, "y": 325, "loc_type": "door", "button": 416, "name": "Swamp Trench 1 Nexus N"},
        {"x": 255, "y": 198, "loc_type": "door", "button": 417, "name": "Swamp Trench 1 Alcove S"},
        {"x": 128, "y": 306, "loc_type": "door", "button": 418, "name": "Swamp Trench 1 Key Ledge NW"},
        {"x": 33, "y": 392, "loc_type": "door", "button": 419, "name": "Swamp Trench 1 Departure WS"},
        {"x": 127, "y": 221, "loc_type": "door", "button": 420, "name": "Swamp Hammer Switch SW"},
        {"x": 36, "y": 135, "loc_type": "door", "button": 421, "name": "Swamp Hammer Switch WN"},
    ],
    (6, 3): [
        {"x": 478, "y": 392, "loc_type": "door", "button": 423, "name": "Swamp Hub ES"},
        {"x": 255, "y": 454, "loc_type": "door", "button": 424, "name": "Swamp Hub S"},
        {"x": 33, "y": 392, "loc_type": "door", "button": 425, "name": "Swamp Hub WS"},
        {"x": 35, "y": 135, "loc_type": "door", "button": 426, "name": "Swamp Hub WN"},
        {"x": 474, "y": 136, "loc_type": "door", "button": 427, "name": "Swamp Hub Dead Ledge EN"},
        {"x": 255, "y": 50, "loc_type": "door", "button": 428, "name": "Swamp Hub North Ledge N"},
    ],
    (6, 4): [
        {"x": 256, "y": 72, "loc_type": "door", "button": 430, "name": "Swamp Donut Top N"},
        {"x": 383, "y": 199, "loc_type": "door", "button": 431, "name": "Swamp Donut Top SE"},
        {"x": 384, "y": 329, "loc_type": "door", "button": 432, "name": "Swamp Donut Bottom NE"},
        {"x": 127, "y": 328, "loc_type": "door", "button": 433, "name": "Swamp Donut Bottom NW"},
        {"x": 127, "y": 198, "loc_type": "door", "button": 434, "name": "Swamp Compass Donut SW"},
    ],
    (5, 3): [
        {"x": 477, "y": 136, "loc_type": "door", "button": 436, "name": "Swamp Crystal Switch EN"},
        {"x": 383, "y": 221, "loc_type": "door", "button": 437, "name": "Swamp Crystal Switch SE"},
        {"x": 382, "y": 303, "loc_type": "door", "button": 440, "name": "Swamp Shortcut NE"},
        {"x": 480, "y": 392, "loc_type": "door", "button": 441, "name": "Swamp Trench 2 Pots ES"},
        {"x": 256, "y": 327, "loc_type": "door", "button": 442, "name": "Swamp Trench 2 Blocks N"},
        {"x": 256, "y": 200, "loc_type": "door", "button": 443, "name": "Swamp Trench 2 Alcove S"},
        {"x": 32, "y": 391, "loc_type": "door", "button": 444, "name": "Swamp Trench 2 Departure WS"},
        {"x": 34, "y": 135, "loc_type": "door", "button": 445, "name": "Swamp Big Key Ledge WN"},
    ],
    (4, 3): [
        {"x": 477, "y": 392, "loc_type": "door", "button": 447, "name": "Swamp West Shallows ES"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 448, "name": "Swamp West Block Path Up Stairs"},
        {"x": 478, "y": 136, "loc_type": "door", "button": 449, "name": "Swamp Barrier EN"},
        {"x": 136, "y": 136, "loc_type": "door", "button": 449, "name": "Swamp West Ledge Drop Entrance"},
        {"x": 348, "y": 136, "loc_type": "door", "button": 449, "name": "Swamp Barrier Ledge Drop Entrance"},
    ],
    (4, 5): [
        {"x": 126, "y": 305, "loc_type": "door", "button": 451, "name": "Swamp Attic Down Stairs"},
        {"x": 136, "y": 136, "loc_type": "door", "button": 451, "name": "Swamp Attic Left Pit"},
        {"x": 348, "y": 136, "loc_type": "door", "button": 451, "name": "Swamp Attic Right Pit"},
    ],
    (6, 2): [
        {"x": 256, "y": 478, "loc_type": "door", "button": 453, "name": "Swamp Push Statue S"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 454, "name": "Swamp Push Statue NW"},
        {"x": 383, "y": 304, "loc_type": "door", "button": 455, "name": "Swamp Push Statue NE"},
        {"x": 447, "y": 304, "loc_type": "door", "button": 456, "name": "Swamp Push Statue Down Stairs"},
        {"x": 128, "y": 223, "loc_type": "door", "button": 457, "name": "Swamp Shooters SW"},
        {"x": 222, "y": 136, "loc_type": "door", "button": 458, "name": "Swamp Shooters EN"},
        {"x": 290, "y": 135, "loc_type": "door", "button": 459, "name": "Swamp Left Elbow WN"},
        {"x": 319, "y": 48, "loc_type": "door", "button": 460, "name": "Swamp Left Elbow Down Stairs"},
        {"x": 383, "y": 223, "loc_type": "door", "button": 461, "name": "Swamp Right Elbow SE"},
        {"x": 430, "y": 48, "loc_type": "door", "button": 462, "name": "Swamp Right Elbow Down Stairs"},
    ],
    (6, 7): [
        {"x": 319, "y": 48, "loc_type": "door", "button": 464, "name": "Swamp Drain Left Up Stairs"},
        {"x": 309, "y": 135, "loc_type": "door", "button": 465, "name": "Swamp Drain WN"},
        {"x": 432, "y": 48, "loc_type": "door", "button": 466, "name": "Swamp Drain Right Up Stairs"},
        {"x": 447, "y": 305, "loc_type": "door", "button": 467, "name": "Swamp Flooded Room Up Stairs"},
        {"x": 311, "y": 391, "loc_type": "door", "button": 468, "name": "Swamp Flooded Room WS"},
        {"x": 128, "y": 70, "loc_type": "door", "button": 469, "name": "Swamp Basement Shallows NW"},
        {"x": 199, "y": 136, "loc_type": "door", "button": 470, "name": "Swamp Basement Shallows EN"},
        {"x": 198, "y": 391, "loc_type": "door", "button": 471, "name": "Swamp Basement Shallows ES"},
    ],
    (6, 6): [
        {"x": 127, "y": 454, "loc_type": "door", "button": 473, "name": "Swamp Waterfall Room SW"},
        {"x": 127, "y": 328, "loc_type": "door", "button": 474, "name": "Swamp Waterfall Room NW"},
        {"x": 384, "y": 330, "loc_type": "door", "button": 475, "name": "Swamp Waterfall Room NE"},
        {"x": 127, "y": 193, "loc_type": "door", "button": 476, "name": "Swamp Refill SW"},
        {"x": 383, "y": 197, "loc_type": "door", "button": 477, "name": "Swamp Behind Waterfall SE"},
        {"x": 384, "y": 49, "loc_type": "door", "button": 478, "name": "Swamp Behind Waterfall Up Stairs"},
    ],
    (6, 1): [
        {"x": 383, "y": 48, "loc_type": "door", "button": 480, "name": "Swamp C Down Stairs"},
        {"x": 383, "y": 222, "loc_type": "door", "button": 481, "name": "Swamp C SE"},
        {"x": 384, "y": 305, "loc_type": "door", "button": 482, "name": "Swamp Waterway NE"},
        {"x": 257, "y": 309, "loc_type": "door", "button": 483, "name": "Swamp Waterway N"},
        {"x": 127, "y": 307, "loc_type": "door", "button": 484, "name": "Swamp Waterway NW"},
        {"x": 256, "y": 221, "loc_type": "door", "button": 485, "name": "Swamp I S"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 486, "name": "Swamp T SW"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 487, "name": "Swamp T NW"},
    ],
    (6, 0): [{"x": 127, "y": 479, "loc_type": "door", "button": 489, "name": "Swamp Boss SW"}],
    (8, 5): [
        {"x": 127, "y": 480, "loc_type": "door", "button": 491, "name": "Skull 1 Lobby S"},
        {"x": 33, "y": 391, "loc_type": "door", "button": 492, "name": "Skull 1 Lobby WS"},
        {"x": 221, "y": 391, "loc_type": "door", "button": 493, "name": "Skull 1 Lobby ES"},
        {"x": 289, "y": 391, "loc_type": "door", "button": 494, "name": "Skull Map Room WS"},
        {"x": 383, "y": 478, "loc_type": "door", "button": 495, "name": "Skull Map Room SE"},
        {"x": 291, "y": 135, "loc_type": "door", "button": 496, "name": "Skull Pot Circle WN"},
        {"x": 219, "y": 135, "loc_type": "door", "button": 497, "name": "Skull Pull Switch EN"},
        {"x": 128, "y": 250, "loc_type": "door", "button": 498, "name": "Skull Pull Switch S"},
        {"x": 127, "y": 264, "loc_type": "door", "button": 499, "name": "Skull Big Chest N"},
    ],
    (8, 6): [
        {"x": 383, "y": 50, "loc_type": "door", "button": 501, "name": "Skull Pinball NE"},
        {"x": 31, "y": 392, "loc_type": "door", "button": 502, "name": "Skull Pinball WS"},
    ],
    (7, 6): [
        {"x": 383, "y": 49, "loc_type": "door", "button": 504, "name": "Skull Compass Room NE"},
        {"x": 477, "y": 392, "loc_type": "door", "button": 505, "name": "Skull Compass Room ES"},
        {"x": 221, "y": 391, "loc_type": "door", "button": 506, "name": "Skull Left Drop ES"},
        {"x": 289, "y": 392, "loc_type": "door", "button": 507, "name": "Skull Compass Room WS"},
    ],
    (7, 5): [
        {"x": 478, "y": 392, "loc_type": "door", "button": 509, "name": "Skull Pot Prison ES"},
        {"x": 383, "y": 479, "loc_type": "door", "button": 510, "name": "Skull Pot Prison SE"},
        {"x": 128, "y": 479, "loc_type": "door", "button": 511, "name": "Skull 2 East Lobby SW"},
        {"x": 33, "y": 392, "loc_type": "door", "button": 512, "name": "Skull 2 East Lobby WS"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 513, "name": "Skull 2 East Lobby NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 514, "name": "Skull Big Key SW"},
        {"x": 221, "y": 137, "loc_type": "door", "button": 515, "name": "Skull Big Key EN"},
        {"x": 291, "y": 136, "loc_type": "door", "button": 516, "name": "Skull Lone Pot WN"},
    ],
    (6, 5): [
        {"x": 477, "y": 393, "loc_type": "door", "button": 518, "name": "Skull Small Hall ES"},
        {"x": 290, "y": 392, "loc_type": "door", "button": 519, "name": "Skull Small Hall WS"},
        {"x": 128, "y": 480, "loc_type": "door", "button": 520, "name": "Skull 2 West Lobby S"},
        {"x": 222, "y": 392, "loc_type": "door", "button": 521, "name": "Skull 2 West Lobby ES"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 522, "name": "Skull 2 West Lobby NW"},
        {"x": 128, "y": 221, "loc_type": "door", "button": 523, "name": "Skull X Room SW"},
    ],
    (9, 5): [
        {"x": 127, "y": 477, "loc_type": "door", "button": 525, "name": "Skull 3 Lobby SW"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 526, "name": "Skull 3 Lobby NW"},
        {"x": 193, "y": 136, "loc_type": "door", "button": 527, "name": "Skull 3 Lobby EN"},
        {"x": 313, "y": 136, "loc_type": "door", "button": 528, "name": "Skull East Bridge WN"},
        {"x": 314, "y": 393, "loc_type": "door", "button": 529, "name": "Skull East Bridge WS"},
        {"x": 194, "y": 392, "loc_type": "door", "button": 530, "name": "Skull West Bridge Nook ES"},
    ],
    (9, 4): [
        {"x": 127, "y": 478, "loc_type": "door", "button": 532, "name": "Skull Star Pits SW"},
        {"x": 221, "y": 392, "loc_type": "door", "button": 533, "name": "Skull Star Pits ES"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 534, "name": "Skull Torch Room WS"},
        {"x": 287, "y": 135, "loc_type": "door", "button": 535, "name": "Skull Torch Room WN"},
        {"x": 221, "y": 136, "loc_type": "door", "button": 536, "name": "Skull Vines EN"},
        {"x": 127, "y": 53, "loc_type": "door", "button": 537, "name": "Skull Vines NW"},
    ],
    (9, 3): [
        {"x": 127, "y": 479, "loc_type": "door", "button": 539, "name": "Skull Spike Corner SW"},
        {"x": 221, "y": 391, "loc_type": "door", "button": 540, "name": "Skull Spike Corner ES"},
        {"x": 289, "y": 391, "loc_type": "door", "button": 541, "name": "Skull Final Drop WS"},
        {"x": 390, "y": 384, "loc_type": "door", "button": 1002, "name": "Skull Final Drop Hole"},
    ],
    (9, 2): [
        {"x": 390, "y": 384, "loc_type": "door", "button": 1001, "name": "Skull Boss Drop Entrance"},
    ],
    (11, 13): [
        {"x": 255, "y": 479, "loc_type": "door", "button": 558, "name": "Thieves Lobby S"},
        {"x": 256, "y": 62, "loc_type": "door", "button": 562, "name": "Thieves Lobby N Edge"},
        {"x": 390, "y": 60, "loc_type": "door", "button": 563, "name": "Thieves Lobby NE Edge"},
        {"x": 480, "y": 265, "loc_type": "door", "button": 564, "name": "Thieves Lobby E"},
        {"x": 467, "y": 365, "loc_type": "door", "button": 565, "name": "Thieves Big Chest Nook ES Edge"},
    ],
    (11, 12): [
        {"x": 258, "y": 467, "loc_type": "door", "button": 567, "name": "Thieves Ambush S Edge"},
        {"x": 390, "y": 469, "loc_type": "door", "button": 568, "name": "Thieves Ambush SE Edge"},
        {"x": 470, "y": 357, "loc_type": "door", "button": 569, "name": "Thieves Ambush ES Edge"},
        {"x": 469, "y": 167, "loc_type": "door", "button": 570, "name": "Thieves Ambush EN Edge"},
        {"x": 475, "y": 265, "loc_type": "door", "button": 571, "name": "Thieves Ambush E"},
    ],
    (12, 12): [
        {"x": 42, "y": 160, "loc_type": "door", "button": 573, "name": "Thieves BK Corner WN Edge"},
        {"x": 40, "y": 364, "loc_type": "door", "button": 574, "name": "Thieves BK Corner WS Edge"},
        {"x": 256, "y": 470, "loc_type": "door", "button": 576, "name": "Thieves BK Corner S Edge"},
        {"x": 117, "y": 470, "loc_type": "door", "button": 577, "name": "Thieves BK Corner SW Edge"},
        {"x": 35, "y": 264, "loc_type": "door", "button": 578, "name": "Thieves Rail Ledge W"},
        {"x": 128, "y": 51, "loc_type": "door", "button": 579, "name": "Thieves Rail Ledge NW"},
        {"x": 383, "y": 51, "loc_type": "door", "button": 580, "name": "Thieves BK Corner NE"},
    ],
    (12, 13): [
        {"x": 125, "y": 62, "loc_type": "door", "button": 582, "name": "Thieves Compass Room NW Edge"},
        {"x": 256, "y": 62, "loc_type": "door", "button": 583, "name": "Thieves Compass Room N Edge"},
        {"x": 41, "y": 365, "loc_type": "door", "button": 584, "name": "Thieves Compass Room WS Edge"},
        {"x": 34, "y": 265, "loc_type": "door", "button": 585, "name": "Thieves Compass Room W"},
    ],
    (12, 11): [
        {"x": 382, "y": 478, "loc_type": "door", "button": 587, "name": "Thieves Hallway SE"},
        {"x": 384, "y": 48, "loc_type": "door", "button": 588, "name": "Thieves Hallway NE"},
        {"x": 292, "y": 391, "loc_type": "door", "button": 589, "name": "Thieves Pot Alcove Mid WS"},
        {"x": 128, "y": 476, "loc_type": "door", "button": 590, "name": "Thieves Pot Alcove Bottom SW"},
        {"x": 34, "y": 136, "loc_type": "door", "button": 591, "name": "Thieves Conveyor Maze WN"},
        {"x": 290, "y": 135, "loc_type": "door", "button": 592, "name": "Thieves Hallway WS"},
        {"x": 220, "y": 390, "loc_type": "door", "button": 593, "name": "Thieves Pot Alcove Mid ES"},
        {"x": 128, "y": 222, "loc_type": "door", "button": 594, "name": "Thieves Conveyor Maze SW"},
        {"x": 128, "y": 303, "loc_type": "door", "button": 595, "name": "Thieves Pot Alcove Top NW"},
        {"x": 222, "y": 136, "loc_type": "door", "button": 596, "name": "Thieves Conveyor Maze EN"},
        {"x": 32, "y": 393, "loc_type": "door", "button": 597, "name": "Thieves Hallway WN"},
        {"x": 128, "y": 50, "loc_type": "door", "button": 598, "name": "Thieves Conveyor Maze Down Stairs"},
    ],
    (12, 10): [{"x": 382, "y": 480, "loc_type": "door", "button": 600, "name": "Thieves Boss SE"}],
    (11, 11): [
        {"x": 479, "y": 393, "loc_type": "door", "button": 611, "name": "Thieves Spike Track ES"},
        {"x": 128, "y": 49, "loc_type": "door", "button": 612, "name": "Thieves Hellway NW"},
        {"x": 479, "y": 136, "loc_type": "door", "button": 613, "name": "Thieves Triple Bypass EN"},
        {"x": 289, "y": 392, "loc_type": "door", "button": 614, "name": "Thieves Spike Track WS"},
        {"x": 224, "y": 392, "loc_type": "door", "button": 615, "name": "Thieves Hellway Crystal ES"},
        {"x": 382, "y": 305, "loc_type": "door", "button": 616, "name": "Thieves Spike Track NE"},
        {"x": 384, "y": 224, "loc_type": "door", "button": 617, "name": "Thieves Triple Bypass SE"},
        {"x": 221, "y": 136, "loc_type": "door", "button": 618, "name": "Thieves Hellway Crystal EN"},
        {"x": 290, "y": 136, "loc_type": "door", "button": 619, "name": "Thieves Triple Bypass WN"},
    ],
    (11, 10): [
        {"x": 127, "y": 478, "loc_type": "door", "button": 621, "name": "Thieves Spike Switch SW"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 622, "name": "Thieves Spike Switch Up Stairs"},
    ],
    (4, 6): [
        {"x": 127, "y": 306, "loc_type": "door", "button": 624, "name": "Thieves Attic Down Stairs"},
        {"x": 223, "y": 393, "loc_type": "door", "button": 625, "name": "Thieves Attic ES"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 626, "name": "Thieves Cricket Hall Left WS"},
        {"x": 510, "y": 396, "loc_type": "door", "button": 627, "name": "Thieves Cricket Hall Left Edge"},
    ],
    (5, 6): [
        {"x": 2, "y": 392, "loc_type": "door", "button": 629, "name": "Thieves Cricket Hall Right Edge"},
        {"x": 226, "y": 392, "loc_type": "door", "button": 630, "name": "Thieves Cricket Hall Right ES"},
        {"x": 287, "y": 392, "loc_type": "door", "button": 631, "name": "Thieves Attic Window WS"},
    ],
    (5, 4): [
        {"x": 127, "y": 48, "loc_type": "door", "button": 633, "name": "Thieves Basement Block Up Stairs"},
        {"x": 32, "y": 136, "loc_type": "door", "button": 634, "name": "Thieves Basement Block WN"},
        {"x": 33, "y": 392, "loc_type": "door", "button": 635, "name": "Thieves Lonely Zazak WS"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 636, "name": "Thieves Blocked Entry SW"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 637, "name": "Thieves Lonely Zazak NW"},
        {"x": 222, "y": 391, "loc_type": "door", "button": 638, "name": "Thieves Lonely Zazak ES"},
        {"x": 288, "y": 394, "loc_type": "door", "button": 639, "name": "Thieves Blind's Cell WS"},
    ],
    (4, 4): [
        {"x": 479, "y": 137, "loc_type": "door", "button": 641, "name": "Thieves Conveyor Bridge EN"},
        {"x": 478, "y": 394, "loc_type": "door", "button": 642, "name": "Thieves Conveyor Bridge ES"},
        {"x": 289, "y": 392, "loc_type": "door", "button": 643, "name": "Thieves Conveyor Bridge WS"},
        {"x": 221, "y": 392, "loc_type": "door", "button": 644, "name": "Thieves Big Chest Room ES"},
        {"x": 289, "y": 137, "loc_type": "door", "button": 645, "name": "Thieves Conveyor Block WN"},
        {"x": 223, "y": 136, "loc_type": "door", "button": 646, "name": "Thieves Trap EN"},
    ],
    (14, 0): [
        {"x": 384, "y": 479, "loc_type": "door", "button": 648, "name": "Ice Lobby SE"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 649, "name": "Ice Lobby WS"},
        {"x": 225, "y": 393, "loc_type": "door", "button": 650, "name": "Ice Jelly Key ES"},
        {"x": 128, "y": 305, "loc_type": "door", "button": 651, "name": "Ice Jelly Key Down Stairs"},
    ],
    (14, 1): [
        {"x": 128, "y": 303, "loc_type": "door", "button": 653, "name": "Ice Floor Switch Up Stairs"},
        {"x": 224, "y": 392, "loc_type": "door", "button": 654, "name": "Ice Floor Switch ES"},
        {"x": 287, "y": 392, "loc_type": "door", "button": 655, "name": "Ice Cross Left WS"},
        {"x": 384, "y": 304, "loc_type": "door", "button": 656, "name": "Ice Cross Top NE"},
        {"x": 384, "y": 222, "loc_type": "door", "button": 657, "name": "Ice Bomb Drop SE"},
        {"x": 384, "y": 122, "loc_type": "door", "button": 657, "name": "Ice Bomb Drop Hole"},
        {"x": 384, "y": 479, "loc_type": "door", "button": 658, "name": "Ice Cross Bottom SE"},
        {"x": 479, "y": 392, "loc_type": "door", "button": 659, "name": "Ice Cross Right ES"},
    ],
    (14, 2): [{"x": 384, "y": 48, "loc_type": "door", "button": 661, "name": "Ice Compass Room NE"}],
    (15, 1): [
        {"x": 30, "y": 391, "loc_type": "door", "button": 663, "name": "Ice Pengator Switch WS"},
        {"x": 224, "y": 391, "loc_type": "door", "button": 664, "name": "Ice Pengator Switch ES"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 665, "name": "Ice Dead End WS"},
        {"x": 359, "y": 344, "loc_type": "door", "button": 666, "name": "Ice Big Key Down Ladder"},
    ],
    (14, 3): [
        {"x": 384, "y": 222, "loc_type": "door", "button": 668, "name": "Ice Stalfos Hint SE"},
        {"x": 384, "y": 122, "loc_type": "door", "button": 668, "name": "Ice Stalfos Hint Drop Entrance"},
        {"x": 384, "y": 305, "loc_type": "door", "button": 669, "name": "Ice Conveyor NE"},
        {"x": 127, "y": 478, "loc_type": "door", "button": 670, "name": "Ice Conveyor SW"},
    ],
    (14, 4): [
        {"x": 127, "y": 50, "loc_type": "door", "button": 672, "name": "Ice Bomb Jump NW"},
        {"x": 223, "y": 136, "loc_type": "door", "button": 673, "name": "Ice Bomb Jump EN"},
        {"x": 287, "y": 135, "loc_type": "door", "button": 674, "name": "Ice Narrow Corridor WN"},
        {"x": 447, "y": 113, "loc_type": "door", "button": 675, "name": "Ice Narrow Corridor Down Stairs"},
    ],
    (14, 6): [
        {"x": 447, "y": 113, "loc_type": "door", "button": 677, "name": "Ice Pengator Trap Up Stairs"},
        {"x": 382, "y": 48, "loc_type": "door", "button": 678, "name": "Ice Pengator Trap NE"},
    ],
    (14, 5): [
        {"x": 384, "y": 480, "loc_type": "door", "button": 680, "name": "Ice Spike Cross SE"},
        {"x": 479, "y": 392, "loc_type": "door", "button": 681, "name": "Ice Spike Cross ES"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 682, "name": "Ice Spike Cross WS"},
        {"x": 225, "y": 391, "loc_type": "door", "button": 683, "name": "Ice Firebar ES"},
        {"x": 70, "y": 423, "loc_type": "door", "button": 684, "name": "Ice Firebar Down Ladder"},
        {"x": 384, "y": 305, "loc_type": "door", "button": 685, "name": "Ice Spike Cross NE"},
        {"x": 383, "y": 219, "loc_type": "door", "button": 686, "name": "Ice Falling Square SE"},
        {"x": 440, "y": 120, "loc_type": "door", "button": 686, "name": "Ice Falling Square Hole"},
    ],
    (15, 5): [
        {"x": 33, "y": 392, "loc_type": "door", "button": 688, "name": "Ice Spike Room WS"},
        {"x": 72, "y": 304, "loc_type": "door", "button": 689, "name": "Ice Spike Room Down Stairs"},
        {"x": 184, "y": 304, "loc_type": "door", "button": 690, "name": "Ice Spike Room Up Stairs"},
    ],
    (15, 3): [
        {"x": 183, "y": 304, "loc_type": "door", "button": 692, "name": "Ice Hammer Block Down Stairs"},
        {"x": 223, "y": 393, "loc_type": "door", "button": 693, "name": "Ice Hammer Block ES"},
        {"x": 287, "y": 393, "loc_type": "door", "button": 694, "name": "Ice Tongue Pull WS"},
        {"x": 360, "y": 349, "loc_type": "door", "button": 695, "name": "Ice Tongue Pull Up Ladder"},
    ],
    (14, 7): [
        {"x": 72, "y": 427, "loc_type": "door", "button": 697, "name": "Ice Freezors Up Ladder"},
        {"x": 225, "y": 391, "loc_type": "door", "button": 698, "name": "Ice Freezors Ledge ES"},
        {"x": 288, "y": 393, "loc_type": "door", "button": 699, "name": "Ice Tall Hint WS"},
        {"x": 479, "y": 136, "loc_type": "door", "button": 700, "name": "Ice Tall Hint EN"},
        {"x": 384, "y": 477, "loc_type": "door", "button": 701, "name": "Ice Tall Hint SE"},
        {"x": 186, "y": 390, "loc_type": "door", "button": 697, "name": "Ice Freezors Hole"},
        {"x": 440, "y": 120, "loc_type": "door", "button": 686, "name": "Ice Tall Hint Drop Entrance"},
    ],
    (15, 7): [
        {"x": 31, "y": 136, "loc_type": "door", "button": 703, "name": "Ice Hookshot Ledge WN"},
        {"x": 128, "y": 224, "loc_type": "door", "button": 704, "name": "Ice Hookshot Balcony SW"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 705, "name": "Ice Spikeball NW"},
        {"x": 72, "y": 305, "loc_type": "door", "button": 706, "name": "Ice Spikeball Up Stairs"},
    ],
    (14, 8): [
        {"x": 384, "y": 49, "loc_type": "door", "button": 708, "name": "Ice Lonely Freezor NE"},
        {"x": 335, "y": 49, "loc_type": "door", "button": 709, "name": "Ice Lonely Freezor Down Stairs"},
    ],
    (14, 10): [
        {"x": 478, "y": 137, "loc_type": "door", "button": 711, "name": "Iced T EN"},
        {"x": 335, "y": 48, "loc_type": "door", "button": 712, "name": "Iced T Up Stairs"},
    ],
    (15, 10): [
        {"x": 33, "y": 136, "loc_type": "door", "button": 714, "name": "Ice Catwalk WN"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 715, "name": "Ice Catwalk NW"},
    ],
    (15, 9): [
        {"x": 127, "y": 480, "loc_type": "door", "button": 717, "name": "Ice Many Pots SW"},
        {"x": 32, "y": 392, "loc_type": "door", "button": 718, "name": "Ice Many Pots WS"},
    ],
    (14, 9): [
        {"x": 478, "y": 392, "loc_type": "door", "button": 720, "name": "Ice Crystal Right ES"},
        {"x": 288, "y": 392, "loc_type": "door", "button": 721, "name": "Ice Crystal Left WS"},
        {"x": 221, "y": 393, "loc_type": "door", "button": 722, "name": "Ice Big Chest View ES"},
        {"x": 384, "y": 307, "loc_type": "door", "button": 723, "name": "Ice Crystal Right NE"},
        {"x": 383, "y": 224, "loc_type": "door", "button": 724, "name": "Ice Backwards Room SE"},
        {"x": 385, "y": 49, "loc_type": "door", "button": 725, "name": "Ice Backwards Room Down Stairs"},
        {"x": 186, "y": 390, "loc_type": "door", "button": 722, "name": "Ice Big Chest View Drop Entrance"},
        {"x": 380, "y": 380, "loc_type": "door", "button": 722, "name": "Ice Crystal Block Hole"},
    ],
    (14, 11): [
        {"x": 383, "y": 49, "loc_type": "door", "button": 727, "name": "Ice Anti-Fairy Up Stairs"},
        {"x": 384, "y": 222, "loc_type": "door", "button": 728, "name": "Ice Anti-Fairy SE"},
        {"x": 384, "y": 304, "loc_type": "door", "button": 729, "name": "Ice Switch Room NE"},
        {"x": 478, "y": 392, "loc_type": "door", "button": 730, "name": "Ice Switch Room ES"},
        {"x": 383, "y": 479, "loc_type": "door", "button": 731, "name": "Ice Switch Room SE"},
        {"x": 380, "y": 380, "loc_type": "door", "button": 731, "name": "Ice Switch Room Drop Entrance"},
    ],
    (14, 13): [{"x": 324, "y": 198, "loc_type": "door", "button": 735, "name": "Ice Boss Drop Entrance"}],
    (15, 11): [{"x": 34, "y": 391, "loc_type": "door", "button": 733, "name": "Ice Refill WS"}],
    (14, 12): [
        {"x": 384, "y": 48, "loc_type": "door", "button": 735, "name": "Ice Antechamber NE"},
        {"x": 324, "y": 198, "loc_type": "door", "button": 735, "name": "Ice Antechamber Hole"},
    ],
    (8, 9): [
        {"x": 127, "y": 482, "loc_type": "door", "button": 737, "name": "Mire Lobby S"},
        {"x": 398, "y": 305, "loc_type": "door", "button": 738, "name": "Mire Post-Gap Down Stairs"},
    ],
    (2, 13): [
        {"x": 398, "y": 304, "loc_type": "door", "button": 740, "name": "Mire 2 Up Stairs"},
        {"x": 384, "y": 49, "loc_type": "door", "button": 741, "name": "Mire 2 NE"},
    ],
    (2, 12): [
        {"x": 384, "y": 480, "loc_type": "door", "button": 743, "name": "Mire Hub SE"},
        {"x": 478, "y": 392, "loc_type": "door", "button": 744, "name": "Mire Hub ES"},
        {"x": 480, "y": 264, "loc_type": "door", "button": 750, "name": "Mire Hub E"},
        {"x": 382, "y": 49, "loc_type": "door", "button": 751, "name": "Mire Hub NE"},
        {"x": 34, "y": 136, "loc_type": "door", "button": 752, "name": "Mire Hub WN"},
        {"x": 35, "y": 392, "loc_type": "door", "button": 753, "name": "Mire Hub WS"},
        {"x": 477, "y": 136, "loc_type": "door", "button": 754, "name": "Mire Hub Right EN"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 755, "name": "Mire Hub Top NW"},
    ],
    (3, 12): [
        {"x": 33, "y": 393, "loc_type": "door", "button": 757, "name": "Mire Lone Shooter WS"},
        {"x": 221, "y": 393, "loc_type": "door", "button": 758, "name": "Mire Lone Shooter ES"},
        {"x": 292, "y": 391, "loc_type": "door", "button": 759, "name": "Mire Falling Bridge WS"},
        {"x": 289, "y": 264, "loc_type": "door", "button": 760, "name": "Mire Falling Bridge W"},
        {"x": 221, "y": 264, "loc_type": "door", "button": 761, "name": "Mire Failure Bridge E"},
        {"x": 35, "y": 264, "loc_type": "door", "button": 762, "name": "Mire Failure Bridge W"},
        {"x": 290, "y": 136, "loc_type": "door", "button": 763, "name": "Mire Falling Bridge WN"},
        {"x": 221, "y": 135, "loc_type": "door", "button": 764, "name": "Mire Map Spike Side EN"},
        {"x": 35, "y": 136, "loc_type": "door", "button": 765, "name": "Mire Map Spot WN"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 766, "name": "Mire Crystal Dead End NW"},
    ],
    (2, 11): [
        {"x": 383, "y": 479, "loc_type": "door", "button": 768, "name": "Mire Hidden Shooters SE"},
        {"x": 479, "y": 392, "loc_type": "door", "button": 769, "name": "Mire Hidden Shooters ES"},
        {"x": 289, "y": 392, "loc_type": "door", "button": 770, "name": "Mire Hidden Shooters WS"},
        {"x": 221, "y": 393, "loc_type": "door", "button": 771, "name": "Mire Cross ES"},
        {"x": 382, "y": 305, "loc_type": "door", "button": 772, "name": "Mire Hidden Shooters NE"},
        {"x": 383, "y": 222, "loc_type": "door", "button": 773, "name": "Mire Minibridge SE"},
        {"x": 127, "y": 478, "loc_type": "door", "button": 774, "name": "Mire Cross SW"},
        {"x": 383, "y": 50, "loc_type": "door", "button": 775, "name": "Mire Minibridge NE"},
        {"x": 453, "y": 136, "loc_type": "door", "button": 776, "name": "Mire BK Door Room EN"},
        {"x": 256, "y": 51, "loc_type": "door", "button": 777, "name": "Mire BK Door Room N"},
    ],
    (3, 11): [
        {"x": 33, "y": 393, "loc_type": "door", "button": 779, "name": "Mire Spikes WS"},
        {"x": 128, "y": 479, "loc_type": "door", "button": 780, "name": "Mire Spikes SW"},
        {"x": 127, "y": 308, "loc_type": "door", "button": 781, "name": "Mire Spikes NW"},
        {"x": 128, "y": 222, "loc_type": "door", "button": 782, "name": "Mire Ledgehop SW"},
        {"x": 57, "y": 137, "loc_type": "door", "button": 783, "name": "Mire Ledgehop WN"},
        {"x": 127, "y": 49, "loc_type": "door", "button": 784, "name": "Mire Ledgehop NW"},
    ],
    (3, 10): [
        {"x": 127, "y": 478, "loc_type": "door", "button": 786, "name": "Mire Bent Bridge SW"},
        {"x": 41, "y": 263, "loc_type": "door", "button": 787, "name": "Mire Bent Bridge W"},
    ],
    (2, 10): [
        {"x": 477, "y": 264, "loc_type": "door", "button": 789, "name": "Mire Over Bridge E"},
        {"x": 33, "y": 264, "loc_type": "door", "button": 790, "name": "Mire Over Bridge W"},
        {"x": 384, "y": 480, "loc_type": "door", "button": 791, "name": "Mire Right Bridge SE"},
        {"x": 255, "y": 480, "loc_type": "door", "button": 792, "name": "Mire Left Bridge S"},
        {"x": 255, "y": 72, "loc_type": "door", "button": 793, "name": "Mire Left Bridge Down Stairs"},
    ],
    (1, 10): [
        {"x": 477, "y": 264, "loc_type": "door", "button": 795, "name": "Mire Fishbone E"},
        {"x": 383, "y": 478, "loc_type": "door", "button": 796, "name": "Mire Fishbone SE"},
    ],
    (1, 11): [
        {"x": 384, "y": 50, "loc_type": "door", "button": 798, "name": "Mire Spike Barrier NE"},
        {"x": 383, "y": 480, "loc_type": "door", "button": 799, "name": "Mire Spike Barrier SE"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 800, "name": "Mire Spike Barrier ES"},
        {"x": 221, "y": 392, "loc_type": "door", "button": 801, "name": "Mire Square Rail WS"},
        {"x": 127, "y": 307, "loc_type": "door", "button": 802, "name": "Mire Square Rail NW"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 803, "name": "Mire Lone Warp SW"},
    ],
    (1, 12): [
        {"x": 477, "y": 137, "loc_type": "door", "button": 805, "name": "Mire Wizzrobe Bypass EN"},
        {"x": 384, "y": 50, "loc_type": "door", "button": 806, "name": "Mire Wizzrobe Bypass NE"},
        {"x": 477, "y": 391, "loc_type": "door", "button": 807, "name": "Mire Conveyor Crystal ES"},
        {"x": 383, "y": 479, "loc_type": "door", "button": 808, "name": "Mire Conveyor Crystal SE"},
        {"x": 292, "y": 391, "loc_type": "door", "button": 809, "name": "Mire Conveyor Crystal WS"},
        {"x": 221, "y": 392, "loc_type": "door", "button": 810, "name": "Mire Tile Room ES"},
        {"x": 127, "y": 479, "loc_type": "door", "button": 811, "name": "Mire Tile Room SW"},
        {"x": 126, "y": 304, "loc_type": "door", "button": 812, "name": "Mire Tile Room NW"},
        {"x": 128, "y": 222, "loc_type": "door", "button": 813, "name": "Mire Compass Room SW"},
        {"x": 223, "y": 136, "loc_type": "door", "button": 814, "name": "Mire Compass Room EN"},
        {"x": 291, "y": 136, "loc_type": "door", "button": 815, "name": "Mire Wizzrobe Bypass WN"},
    ],
    (1, 13): [
        {"x": 383, "y": 49, "loc_type": "door", "button": 817, "name": "Mire Neglected Room NE"},
        {"x": 127, "y": 50, "loc_type": "door", "button": 818, "name": "Mire Conveyor Barrier NW"},
        {"x": 175, "y": 49, "loc_type": "door", "button": 819, "name": "Mire Conveyor Barrier Up Stairs"},
        {"x": 383, "y": 221, "loc_type": "door", "button": 820, "name": "Mire Neglected Room SE"},
        {"x": 384, "y": 305, "loc_type": "door", "button": 821, "name": "Mire Chest View NE"},
        {"x": 290, "y": 392, "loc_type": "door", "button": 822, "name": "Mire BK Chest Ledge WS"},
        {"x": 222, "y": 391, "loc_type": "door", "button": 823, "name": "Mire Warping Pool ES"},
        {"x": 168, "y": 433, "loc_type": "door", "button": 828, "name": "Mire Warping Pool Drop Entrance"},
        {"x": 78, "y": 78, "loc_type": "door", "button": 828, "name": "Mire Conveyor Barrier Drop Entrance"},
        {"x": 369, "y": 393, "loc_type": "door", "button": 828, "name": "Mire BK Chest Ledge Drop Entrance"},
    ],
    (7, 9): [
        {"x": 175, "y": 49, "loc_type": "door", "button": 825, "name": "Mire Torches Top Down Stairs"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 826, "name": "Mire Torches Top SW"},
        {"x": 127, "y": 305, "loc_type": "door", "button": 827, "name": "Mire Torches Bottom NW"},
        {"x": 223, "y": 391, "loc_type": "door", "button": 828, "name": "Mire Torches Bottom WS"},
        {"x": 168, "y": 433, "loc_type": "door", "button": 828, "name": "Mire Torches Bottom Holes"},
        {"x": 78, "y": 78, "loc_type": "door", "button": 828, "name": "Mire Torches Top Holes"},
        {"x": 369, "y": 393, "loc_type": "door", "button": 828, "name": "Mire Attic Hint Hole"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 829, "name": "Mire Attic Hint ES"},
    ],
    (3, 9): [
        {"x": 255, "y": 49, "loc_type": "door", "button": 831, "name": "Mire Dark Shooters Up Stairs"},
        {"x": 128, "y": 223, "loc_type": "door", "button": 832, "name": "Mire Dark Shooters SW"},
        {"x": 127, "y": 305, "loc_type": "door", "button": 833, "name": "Mire Block X NW"},
        {"x": 383, "y": 221, "loc_type": "door", "button": 834, "name": "Mire Dark Shooters SE"},
        {"x": 383, "y": 308, "loc_type": "door", "button": 835, "name": "Mire Key Rupees NE"},
        {"x": 32, "y": 393, "loc_type": "door", "button": 836, "name": "Mire Block X WS"},
    ],
    (2, 9): [
        {"x": 478, "y": 392, "loc_type": "door", "button": 838, "name": "Mire Tall Dark and Roomy ES"},
        {"x": 291, "y": 135, "loc_type": "door", "button": 839, "name": "Mire Tall Dark and Roomy WN"},
        {"x": 221, "y": 136, "loc_type": "door", "button": 840, "name": "Mire Shooter Rupees EN"},
        {"x": 290, "y": 393, "loc_type": "door", "button": 841, "name": "Mire Tall Dark and Roomy WS"},
        {"x": 221, "y": 392, "loc_type": "door", "button": 842, "name": "Mire Crystal Right ES"},
        {"x": 129, "y": 306, "loc_type": "door", "button": 843, "name": "Mire Crystal Mid NW"},
        {"x": 129, "y": 223, "loc_type": "door", "button": 844, "name": "Mire Crystal Top SW"},
        {"x": 33, "y": 394, "loc_type": "door", "button": 845, "name": "Mire Crystal Left WS"},
    ],
    (1, 9): [
        {"x": 478, "y": 393, "loc_type": "door", "button": 847, "name": "Mire Falling Foes ES"},
        {"x": 384, "y": 176, "loc_type": "door", "button": 848, "name": "Mire Falling Foes Up Stairs"},
    ],
    (0, 10): [
        {"x": 384, "y": 177, "loc_type": "door", "button": 850, "name": "Mire Firesnake Skip Down Stairs"},
        {"x": 128, "y": 51, "loc_type": "door", "button": 851, "name": "Mire Antechamber NW"},
    ],
    (0, 9): [{"x": 127, "y": 480, "loc_type": "door", "button": 853, "name": "Mire Boss SW"}],
    (6, 13): [
        {"x": 383, "y": 481, "loc_type": "door", "button": 855, "name": "TR Main Lobby SE"},
        {"x": 383, "y": 52, "loc_type": "door", "button": 856, "name": "TR Lobby Ledge NE"},
        {"x": 126, "y": 54, "loc_type": "door", "button": 857, "name": "TR Compass Room NW"},
    ],
    (6, 12): [
        {"x": 127, "y": 481, "loc_type": "door", "button": 859, "name": "TR Hub SW"},
        {"x": 383, "y": 481, "loc_type": "door", "button": 860, "name": "TR Hub SE"},
        {"x": 478, "y": 393, "loc_type": "door", "button": 861, "name": "TR Hub ES"},
        {"x": 478, "y": 138, "loc_type": "door", "button": 862, "name": "TR Hub EN"},
        {"x": 127, "y": 51, "loc_type": "door", "button": 863, "name": "TR Hub NW"},
        {"x": 382, "y": 51, "loc_type": "door", "button": 864, "name": "TR Hub NE"},
    ],
    (7, 12): [
        {"x": 36, "y": 392, "loc_type": "door", "button": 866, "name": "TR Torches Ledge WS"},
        {"x": 35, "y": 138, "loc_type": "door", "button": 867, "name": "TR Torches WN"},
        {"x": 127, "y": 51, "loc_type": "door", "button": 868, "name": "TR Torches NW"},
    ],
    (7, 11): [{"x": 127, "y": 481, "loc_type": "door", "button": 870, "name": "TR Roller Room SW"}],
    (6, 11): [
        {"x": 127, "y": 478, "loc_type": "door", "button": 872, "name": "TR Pokey 1 SW"},
        {"x": 382, "y": 479, "loc_type": "door", "button": 873, "name": "TR Tile Room SE"},
        {"x": 383, "y": 307, "loc_type": "door", "button": 874, "name": "TR Tile Room NE"},
        {"x": 384, "y": 220, "loc_type": "door", "button": 875, "name": "TR Refill SE"},
        {"x": 128, "y": 306, "loc_type": "door", "button": 876, "name": "TR Pokey 1 NW"},
        {"x": 127, "y": 223, "loc_type": "door", "button": 877, "name": "TR Chain Chomps SW"},
        {"x": 127, "y": 52, "loc_type": "door", "button": 878, "name": "TR Chain Chomps Down Stairs"},
    ],
    (5, 1): [
        {"x": 126, "y": 49, "loc_type": "door", "button": 880, "name": "TR Pipe Pit Up Stairs"},
        {"x": 35, "y": 137, "loc_type": "door", "button": 881, "name": "TR Pipe Pit WN"},
        {"x": 34, "y": 392, "loc_type": "door", "button": 882, "name": "TR Pipe Ledge WS"},
    ],
    (4, 1): [
        {"x": 478, "y": 137, "loc_type": "door", "button": 884, "name": "TR Lava Dual Pipes EN"},
        {"x": 35, "y": 136, "loc_type": "door", "button": 885, "name": "TR Lava Dual Pipes WN"},
        {"x": 127, "y": 480, "loc_type": "door", "button": 886, "name": "TR Lava Dual Pipes SW"},
        {"x": 35, "y": 393, "loc_type": "door", "button": 887, "name": "TR Lava Island WS"},
        {"x": 478, "y": 393, "loc_type": "door", "button": 888, "name": "TR Lava Island ES"},
        {"x": 383, "y": 479, "loc_type": "door", "button": 889, "name": "TR Lava Escape SE"},
        {"x": 128, "y": 48, "loc_type": "door", "button": 890, "name": "TR Lava Escape NW"},
    ],
    (3, 1): [
        {"x": 476, "y": 138, "loc_type": "door", "button": 892, "name": "TR Pokey 2 EN"},
        {"x": 476, "y": 393, "loc_type": "door", "button": 893, "name": "TR Pokey 2 ES"},
    ],
    (4, 2): [
        {"x": 127, "y": 49, "loc_type": "door", "button": 895, "name": "TR Twin Pokeys NW"},
        {"x": 127, "y": 223, "loc_type": "door", "button": 896, "name": "TR Twin Pokeys SW"},
        {"x": 126, "y": 303, "loc_type": "door", "button": 897, "name": "TR Hallway NW"},
        {"x": 34, "y": 393, "loc_type": "door", "button": 898, "name": "TR Hallway WS"},
        {"x": 221, "y": 138, "loc_type": "door", "button": 899, "name": "TR Twin Pokeys EN"},
        {"x": 291, "y": 136, "loc_type": "door", "button": 900, "name": "TR Dodgers WN"},
        {"x": 224, "y": 394, "loc_type": "door", "button": 901, "name": "TR Hallway ES"},
        {"x": 290, "y": 392, "loc_type": "door", "button": 902, "name": "TR Big View WS"},
        {"x": 382, "y": 478, "loc_type": "door", "button": 903, "name": "TR Big Chest Entrance SE"},
        {"x": 383, "y": 303, "loc_type": "door", "button": 904, "name": "TR Big Chest NE"},
        {"x": 383, "y": 225, "loc_type": "door", "button": 905, "name": "TR Dodgers SE"},
        {"x": 382, "y": 52, "loc_type": "door", "button": 906, "name": "TR Dodgers NE"},
    ],
    (3, 2): [
        {"x": 383, "y": 479, "loc_type": "door", "button": 908, "name": "TR Lazy Eyes SE"},
        {"x": 478, "y": 391, "loc_type": "door", "button": 909, "name": "TR Lazy Eyes ES"},
    ],
    (4, 0): [
        {"x": 127, "y": 480, "loc_type": "door", "button": 911, "name": "TR Dash Room SW"},
        {"x": 226, "y": 392, "loc_type": "door", "button": 912, "name": "TR Dash Room ES"},
        {"x": 288, "y": 395, "loc_type": "door", "button": 913, "name": "TR Tongue Pull WS"},
        {"x": 383, "y": 306, "loc_type": "door", "button": 914, "name": "TR Tongue Pull NE"},
        {"x": 383, "y": 225, "loc_type": "door", "button": 915, "name": "TR Rupees SE"},
        {"x": 126, "y": 305, "loc_type": "door", "button": 916, "name": "TR Dash Room NW"},
        {"x": 126, "y": 224, "loc_type": "door", "button": 917, "name": "TR Crystaroller SW"},
        {"x": 127, "y": 51, "loc_type": "door", "button": 918, "name": "TR Crystaroller Down Stairs"},
    ],
    (5, 11): [
        {"x": 127, "y": 49, "loc_type": "door", "button": 920, "name": "TR Dark Ride Up Stairs"},
        {"x": 127, "y": 478, "loc_type": "door", "button": 921, "name": "TR Dark Ride SW"},
    ],
    (5, 12): [
        {"x": 127, "y": 48, "loc_type": "door", "button": 923, "name": "TR Dash Bridge NW"},
        {"x": 128, "y": 481, "loc_type": "door", "button": 924, "name": "TR Dash Bridge SW"},
        {"x": 33, "y": 392, "loc_type": "door", "button": 925, "name": "TR Dash Bridge WS"},
    ],
    (5, 13): [
        {"x": 127, "y": 48, "loc_type": "door", "button": 927, "name": "TR Eye Bridge NW"},
        {"x": 127, "y": 480, "loc_type": "door", "button": 928, "name": "TR Eye Bridge SW"},
    ],
    (4, 12): [
        {"x": 478, "y": 393, "loc_type": "door", "button": 930, "name": "TR Crystal Maze ES"},
        {"x": 256, "y": 49, "loc_type": "door", "button": 931, "name": "TR Crystal Maze North Stairs"},
    ],
    (4, 11): [
        {"x": 255, "y": 480, "loc_type": "door", "button": 933, "name": "TR Final Abyss South Stairs"},
        {"x": 128, "y": 50, "loc_type": "door", "button": 934, "name": "TR Final Abyss NW"},
    ],
    (4, 10): [{"x": 127, "y": 479, "loc_type": "door", "button": 936, "name": "TR Boss SW"}],
    (12, 0): [
        {"x": 255, "y": 479, "loc_type": "door", "button": 938, "name": "GT Lobby S"},
        {"x": 127, "y": 72, "loc_type": "door", "button": 939, "name": "GT Lobby Left Down Stairs"},
        {"x": 256, "y": 47, "loc_type": "door", "button": 940, "name": "GT Lobby Up Stairs"},
        {"x": 382, "y": 72, "loc_type": "door", "button": 941, "name": "GT Lobby Right Down Stairs"},
    ],
    (12, 8): [
        {"x": 127, "y": 46, "loc_type": "door", "button": 943, "name": "GT Torch Up Stairs"},
        {"x": 33, "y": 137, "loc_type": "door", "button": 944, "name": "GT Torch WN"},
        {"x": 383, "y": 48, "loc_type": "door", "button": 945, "name": "GT Hope Room Up Stairs"},
        {"x": 477, "y": 137, "loc_type": "door", "button": 946, "name": "GT Hope Room EN"},
        {"x": 222, "y": 136, "loc_type": "door", "button": 947, "name": "GT Torch EN"},
        {"x": 289, "y": 135, "loc_type": "door", "button": 948, "name": "GT Hope Room WN"},
        {"x": 127, "y": 222, "loc_type": "door", "button": 949, "name": "GT Torch SW"},
        {"x": 127, "y": 305, "loc_type": "door", "button": 950, "name": "GT Big Chest NW"},
        {"x": 64, "y": 305, "loc_type": "door", "button": 951, "name": "GT Blocked Stairs Down Stairs"},
        {"x": 127, "y": 478, "loc_type": "door", "button": 952, "name": "GT Big Chest SW"},
        {"x": 383, "y": 479, "loc_type": "door", "button": 953, "name": "GT Bob's Room SE"},
        {"x": 448, "y": 448, "loc_type": "door", "button": 1001, "name": "GT Bob's Room Hole"},
    ],
    (13, 8): [
        {"x": 33, "y": 137, "loc_type": "door", "button": 955, "name": "GT Tile Room WN"},
        {"x": 221, "y": 136, "loc_type": "door", "button": 956, "name": "GT Tile Room EN"},
        {"x": 290, "y": 136, "loc_type": "door", "button": 957, "name": "GT Speed Torch WN"},
        {"x": 384, "y": 49, "loc_type": "door", "button": 958, "name": "GT Speed Torch NE"},
        {"x": 289, "y": 391, "loc_type": "door", "button": 959, "name": "GT Speed Torch WS"},
        {"x": 222, "y": 392, "loc_type": "door", "button": 960, "name": "GT Pots n Blocks ES"},
        {"x": 383, "y": 478, "loc_type": "door", "button": 961, "name": "GT Speed Torch SE"},
    ],
    (13, 9): [
        {"x": 383, "y": 49, "loc_type": "door", "button": 963, "name": "GT Crystal Conveyor NE"},
        {"x": 289, "y": 137, "loc_type": "door", "button": 964, "name": "GT Crystal Conveyor WN"},
        {"x": 223, "y": 136, "loc_type": "door", "button": 965, "name": "GT Compass Room EN"},
        {"x": 32, "y": 392, "loc_type": "door", "button": 966, "name": "GT Invisible Bridges WS"},
    ],
    (12, 9): [
        {"x": 478, "y": 392, "loc_type": "door", "button": 968, "name": "GT Invisible Catwalk ES"},
        {"x": 34, "y": 392, "loc_type": "door", "button": 969, "name": "GT Invisible Catwalk WS"},
        {"x": 128, "y": 49, "loc_type": "door", "button": 970, "name": "GT Invisible Catwalk NW"},
        {"x": 383, "y": 49, "loc_type": "door", "button": 971, "name": "GT Invisible Catwalk NE"},
    ],
    (11, 8): [
        {"x": 478, "y": 137, "loc_type": "door", "button": 973, "name": "GT Conveyor Cross EN"},
        {"x": 290, "y": 135, "loc_type": "door", "button": 974, "name": "GT Conveyor Cross WN"},
        {"x": 221, "y": 136, "loc_type": "door", "button": 975, "name": "GT Hookshot EN"},
        {"x": 127, "y": 50, "loc_type": "door", "button": 976, "name": "GT Hookshot NW"},
        {"x": 219, "y": 392, "loc_type": "door", "button": 977, "name": "GT Hookshot ES"},
        {"x": 289, "y": 391, "loc_type": "door", "button": 978, "name": "GT Map Room WS"},
        {"x": 127, "y": 478, "loc_type": "door", "button": 979, "name": "GT Hookshot SW"},
    ],
    (11, 9): [
        {"x": 127, "y": 50, "loc_type": "door", "button": 981, "name": "GT Double Switch NW"},
        {"x": 222, "y": 135, "loc_type": "door", "button": 982, "name": "GT Double Switch EN"},
        {"x": 289, "y": 136, "loc_type": "door", "button": 983, "name": "GT Spike Crystals WN"},
        {"x": 477, "y": 393, "loc_type": "door", "button": 984, "name": "GT Warp Maze (Pits) ES"},
    ],
    (13, 7): [
        {"x": 128, "y": 222, "loc_type": "door", "button": 986, "name": "GT Firesnake Room SW"},
        {"x": 127, "y": 306, "loc_type": "door", "button": 987, "name": "GT Warp Maze (Rails) NW"},
        {"x": 36, "y": 392, "loc_type": "door", "button": 988, "name": "GT Warp Maze (Rails) WS"},
        {"x": 383, "y": 480, "loc_type": "door", "button": 989, "name": "GT Petting Zoo SE"},
    ],
    (11, 7): [
        {"x": 478, "y": 136, "loc_type": "door", "button": 991, "name": "GT Conveyor Star Pits EN"},
        {"x": 479, "y": 393, "loc_type": "door", "button": 992, "name": "GT Hidden Star ES"},
        {"x": 128, "y": 480, "loc_type": "door", "button": 993, "name": "GT DMs Room SW"},
    ],
    (12, 7): [
        {"x": 34, "y": 136, "loc_type": "door", "button": 995, "name": "GT Falling Bridge WN"},
        {"x": 34, "y": 392, "loc_type": "door", "button": 996, "name": "GT Falling Bridge WS"},
        {"x": 481, "y": 394, "loc_type": "door", "button": 997, "name": "GT Randomizer Room ES"},
    ],
    (12, 1): [
        {"x": 384, "y": 304, "loc_type": "door", "button": 999, "name": "GT Ice Armos NE"},
        {"x": 383, "y": 223, "loc_type": "door", "button": 1000, "name": "GT Big Key Room SE"},
        {"x": 288, "y": 391, "loc_type": "door", "button": 1001, "name": "GT Ice Armos WS"},
        {"x": 448, "y": 448, "loc_type": "door", "button": 1001, "name": "GT Ice Armos Drop Entrance"},
        {"x": 223, "y": 392, "loc_type": "door", "button": 1002, "name": "GT Four Torches ES"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 1003, "name": "GT Four Torches NW"},
        {"x": 127, "y": 223, "loc_type": "door", "button": 1004, "name": "GT Fairy Abyss SW"},
        {"x": 64, "y": 303, "loc_type": "door", "button": 1005, "name": "GT Four Torches Up Stairs"},
    ],
    (11, 6): [
        {"x": 255, "y": 50, "loc_type": "door", "button": 1007, "name": "GT Crystal Paths Down Stairs"},
        {"x": 127, "y": 224, "loc_type": "door", "button": 1008, "name": "GT Crystal Paths SW"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 1009, "name": "GT Mimics 1 NW"},
        {"x": 223, "y": 392, "loc_type": "door", "button": 1010, "name": "GT Mimics 1 ES"},
        {"x": 287, "y": 392, "loc_type": "door", "button": 1011, "name": "GT Mimics 2 WS"},
        {"x": 383, "y": 304, "loc_type": "door", "button": 1012, "name": "GT Mimics 2 NE"},
        {"x": 383, "y": 223, "loc_type": "door", "button": 1013, "name": "GT Dash Hall SE"},
        {"x": 384, "y": 49, "loc_type": "door", "button": 1014, "name": "GT Dash Hall NE"},
    ],
    (11, 5): [
        {"x": 384, "y": 478, "loc_type": "door", "button": 1016, "name": "GT Hidden Spikes SE"},
        {"x": 479, "y": 136, "loc_type": "door", "button": 1017, "name": "GT Hidden Spikes EN"},
    ],
    (12, 5): [
        {"x": 33, "y": 136, "loc_type": "door", "button": 1019, "name": "GT Cannonball Bridge WN"},
        {"x": 384, "y": 223, "loc_type": "door", "button": 1020, "name": "GT Cannonball Bridge SE"},
        {"x": 385, "y": 303, "loc_type": "door", "button": 1021, "name": "GT Refill NE"},
        {"x": 384, "y": 48, "loc_type": "door", "button": 1022, "name": "GT Cannonball Bridge Up Stairs"},
    ],
    (13, 5): [
        {"x": 383, "y": 47, "loc_type": "door", "button": 1024, "name": "GT Gauntlet 1 Down Stairs"},
        {"x": 289, "y": 136, "loc_type": "door", "button": 1025, "name": "GT Gauntlet 1 WN"},
        {"x": 224, "y": 135, "loc_type": "door", "button": 1026, "name": "GT Gauntlet 2 EN"},
        {"x": 127, "y": 224, "loc_type": "door", "button": 1027, "name": "GT Gauntlet 2 SW"},
        {"x": 127, "y": 305, "loc_type": "door", "button": 1028, "name": "GT Gauntlet 3 NW"},
        {"x": 127, "y": 481, "loc_type": "door", "button": 1029, "name": "GT Gauntlet 3 SW"},
    ],
    (13, 6): [
        {"x": 127, "y": 48, "loc_type": "door", "button": 1031, "name": "GT Gauntlet 4 NW"},
        {"x": 127, "y": 224, "loc_type": "door", "button": 1032, "name": "GT Gauntlet 4 SW"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 1033, "name": "GT Gauntlet 5 NW"},
        {"x": 32, "y": 392, "loc_type": "door", "button": 1034, "name": "GT Gauntlet 5 WS"},
    ],
    (12, 6): [
        {"x": 480, "y": 392, "loc_type": "door", "button": 1036, "name": "GT Beam Dash ES"},
        {"x": 289, "y": 393, "loc_type": "door", "button": 1037, "name": "GT Beam Dash WS"},
        {"x": 224, "y": 392, "loc_type": "door", "button": 1038, "name": "GT Lanmolas 2 ES"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 1039, "name": "GT Lanmolas 2 NW"},
        {"x": 128, "y": 223, "loc_type": "door", "button": 1040, "name": "GT Quad Pot SW"},
        {"x": 128, "y": 47, "loc_type": "door", "button": 1041, "name": "GT Quad Pot Up Stairs"},
    ],
    (5, 10): [
        {"x": 128, "y": 49, "loc_type": "door", "button": 1043, "name": "GT Wizzrobes 1 Down Stairs"},
        {"x": 127, "y": 223, "loc_type": "door", "button": 1044, "name": "GT Wizzrobes 1 SW"},
        {"x": 127, "y": 304, "loc_type": "door", "button": 1045, "name": "GT Dashing Bridge NW"},
        {"x": 383, "y": 304, "loc_type": "door", "button": 1046, "name": "GT Dashing Bridge NE"},
        {"x": 383, "y": 223, "loc_type": "door", "button": 1047, "name": "GT Wizzrobes 2 SE"},
        {"x": 384, "y": 48, "loc_type": "door", "button": 1048, "name": "GT Wizzrobes 2 NE"},
    ],
    (5, 9): [
        {"x": 383, "y": 481, "loc_type": "door", "button": 1050, "name": "GT Conveyor Bridge SE"},
        {"x": 479, "y": 136, "loc_type": "door", "button": 1051, "name": "GT Conveyor Bridge EN"},
    ],
    (6, 9): [
        {"x": 33, "y": 136, "loc_type": "door", "button": 1053, "name": "GT Torch Cross WN"},
        {"x": 223, "y": 394, "loc_type": "door", "button": 1054, "name": "GT Torch Cross ES"},
        {"x": 289, "y": 392, "loc_type": "door", "button": 1055, "name": "GT Staredown WS"},
        {"x": 384, "y": 421, "loc_type": "door", "button": 1056, "name": "GT Staredown Up Ladder"},
        {"x": 420, "y": 365, "loc_type": "door", "button": 1056, "name": "GT Staredown Drop Entrance"},
    ],
    (13, 3): [
        {"x": 384, "y": 417, "loc_type": "door", "button": 1058, "name": "GT Falling Torches Down Ladder"},
        {"x": 420, "y": 365, "loc_type": "door", "button": 1056, "name": "GT Falling Torches Hole"},
        {"x": 383, "y": 305, "loc_type": "door", "button": 1059, "name": "GT Falling Torches NE"},
        {"x": 384, "y": 223, "loc_type": "door", "button": 1060, "name": "GT Mini Helmasaur Room SE"},
        {"x": 291, "y": 137, "loc_type": "door", "button": 1061, "name": "GT Mini Helmasaur Room WN"},
        {"x": 221, "y": 135, "loc_type": "door", "button": 1062, "name": "GT Bomb Conveyor EN"},
        {"x": 128, "y": 226, "loc_type": "door", "button": 1063, "name": "GT Bomb Conveyor SW"},
        {"x": 128, "y": 304, "loc_type": "door", "button": 1064, "name": "GT Crystal Circles NW"},
        {"x": 127, "y": 478, "loc_type": "door", "button": 1065, "name": "GT Crystal Circles SW"},
    ],
    (13, 4): [
        {"x": 128, "y": 50, "loc_type": "door", "button": 1067, "name": "GT Left Moldorm Ledge NW"},
        {"x": 256, "y": 323, "loc_type": "door", "button": 1067, "name": "GT Moldorm Hole"},
        {"x": 34, "y": 393, "loc_type": "door", "button": 1068, "name": "GT Validation WS"},
        {"x": 384, "y": 49, "loc_type": "door", "button": 1069, "name": "GT Right Moldorm Ledge Down Stairs"},
    ],
    (6, 10): [
        {"x": 384, "y": 47, "loc_type": "door", "button": 1071, "name": "GT Moldorm Pit Up Stairs"},
        {"x": 256, "y": 323, "loc_type": "door", "button": 1067, "name": "GT Moldorm Pit Drop Entrance"},
    ],
    (12, 4): [
        {"x": 480, "y": 392, "loc_type": "door", "button": 1073, "name": "GT Frozen Over ES"},
        {"x": 384, "y": 47, "loc_type": "door", "button": 1074, "name": "GT Frozen Over Up Stairs"},
    ],
    (13, 1): [
        {"x": 383, "y": 49, "loc_type": "door", "button": 1076, "name": "GT Brightly Lit Hall Down Stairs"},
        {"x": 127, "y": 50, "loc_type": "door", "button": 1077, "name": "GT Brightly Lit Hall NW"},
    ],
    (13, 0): [{"x": 127, "y": 478, "loc_type": "door", "button": 1079, "name": "GT Agahnim 2 SW"}],
}

regions_to_doors = {}
doors_to_regions = {}
with open("Regions.py", "r") as fh:
    while True:
        line = fh.readline()
        if not line:
            break
        line = line.strip()
        # print(line)
        if not line.startswith("create_dungeon_region(player, "):
            continue
        while not line.rstrip().endswith("),"):
            line = f"{line.rstrip()}{fh.readline().lstrip()}"
        data = line.split("#")[0].strip().split("[")
        if len(data) < 2:
            continue
        doors = data[-1].rstrip("]), ").split(",")
        data = data[0].strip().split(",")
        region = data[1].strip(" '\"").replace("\\", "")
        dungeon = data[2]
        doors = [door.strip().strip(" '\"").replace("\\", "") for door in doors]

        # If a door is in door_fix_map, replace it with the key from that dict
        for i, door in enumerate(doors):
            if door in door_fix_map:
                doors[i] = door_fix_map[door]

        regions_to_doors[region] = doors

        for door in doors:
            doors_to_regions[door] = region

# To add a manual entry, like a drop, it has to be added in all three structure
add_manual_drop("Ice Bomb Drop Hole", 0x1E, 0x3E)
add_manual_drop("Ice Crystal Block Hole", 0x9E, 0xBE)
add_manual_drop("Ice Falling Square Hole", 0x5E, 0x7E)
add_manual_drop("Ice Freezors Hole", 0x7E, 0x9E)
add_manual_drop("Ice Antechamber Hole", 0xCE, 0xDE)
add_manual_drop("PoD Pit Room Bomb Hole", 0x3A, 0x0A)
add_manual_drop("PoD Pit Room Freefall", 0x3A, 0x0A)
add_manual_drop("Swamp Attic Left Pit", 0x54, 0x34)
add_manual_drop("Swamp Attic Right Pit", 0x54, 0x34)
add_manual_drop("Skull Final Drop Hole", 0x39, 0x29)
add_manual_drop("Mire Torches Bottom Holes", 0x97, 0xD1)
add_manual_drop("Mire Torches Top Holes", 0x97, 0xD1)
add_manual_drop("Mire Attic Hint Hole", 0x97, 0xD1)
add_manual_drop("GT Bob's Room Hole", 0x8C, 0x1C)
add_manual_drop("GT Falling Torches Hole", 0x3D, 0x96)
add_manual_drop("GT Moldorm Hole", 0x4D, 0xA6)


dungeon_lobbies = {
    World.CastleTower: ["Agahnims Tower"],
    World.DesertPalace: ["Desert South", "Desert East", "Desert West", "Desert Back"],
    World.EasternPalace: ["Eastern"],
    World.GanonsTower: ["Ganons Tower"],
    World.TowerOfHera: ["Hera"],
    World.HyruleCastle: ["Hyrule Castle South", "Hyrule Castle East", "Hyrule Castle West", "Sanctuary"],
    World.IcePalace: ["Ice"],
    World.MiseryMire: ["Mire"],
    World.PalaceOfDarkness: ["Palace of Darkness"],
    # World.Sanctuary: ['Sanctuary'],
    World.SkullWoods: ["Skull 1", "Skull 2 East", "Skull 2 West", "Skull 3"],
    World.SwampPalace: ["Swamp"],
    World.ThievesTown: ["Thieves Town"],
    World.TurtleRock: [
        "Turtle Rock Main",
        "Turtle Rock Lazy Eyes",
        "Turtle Rock Chest",
        "Turtle Rock Eye Bridge",
    ],
}

#     (13, 0): [{"x": 127, "y": 478, "loc_type": "door", "button": 1079, "name": "GT Agahnim 2 SW"}],
# }

dungeon_tiles = defaultdict(list)

# We could potentially just use a vanilla customizer layout to get the maps as people expect to see them
# Use the same doors code currently used, but don't add arrows and make tiles clickable
for tile, doors in door_coordinates.items():
    dungeon = doors[0]["name"].split(" ")[0]
    dungeon_tiles[dungeon].append(tile)

door_coordinates_key = {
    door_data["name"]: (eg_tuple, list_pos)
    for eg_tuple, door_datas in door_coordinates.items()
    for list_pos, door_data in enumerate(door_datas)
}

#  First make a list of each EG tile and 1 use
eg_tile_multiuse = {tile: 1 for tile in door_coordinates.keys()}

# Override EG tiles that are used more than once - i.e. have multiple, isolated paths
eg_tile_multiuse_override = {
    (0, 9): 2,  # PoD shooter
    (4, 1): 3,  # TR pipes
    (10, 1): 2,  # PoD Hammerjump
    (10, 2): 2,  # PoD Area
    (5, 3): 2,  # Swamp right side chest
    (6, 3): 2,  # Swamp isolated pots
    (7, 3): 2,  # Swamp map chest
    (15, 4): 2,  # Ice refill & faries
    (7, 5): 2,  # Skull pot prison
    (10, 6): 2,  # PoD boss catwalk
    (5, 7): 2,  # Desert right side chest
    (4, 7): 2,  # Desert lobby upper
    (11, 7): 3,  # GT Stalfos + right side
    (12, 7): 2,  # GT rando room + falling bridge
    (13, 7): 2,  # GT right side portal room
    (2, 8): 2,  # HC guards + catwalk
    (7, 8): 2,  # Hera basement cage
    (12, 8): 2,  # GT Bobs room
    (11, 9): 2,  # GT Left side portals
    (13, 9): 2,  # GT invisible bridge
    (2, 10): 2,  # Mire left right bridge
    (9, 10): 2,  # Eastern Big Chest Overlook
    (2, 11): 2,  # BK door overlook
    (6, 11): 2,  # TR trap room
    (9, 11): 2,  # Eastern cannonball room
    (12, 11): 2,  # Thieves pots
    (15, 11): 2,  # Ice pots 2?
    (7, 12): 2,  # TR fire puzzle overlook
    (1, 13): 2,  # Mire BK chest overlook
    (6, 13): 2,  # TR entrance
    (11, 13): 2,  # TT BK chest
}

eg_tile_multiuse.update(eg_tile_multiuse_override)
