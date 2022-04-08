from enum import Enum
from pathlib import Path
import source.gui.customizer.location_data as location_data


class World(Enum):
    LightWorld = 0
    DarkWorld = 1
    UnderWorld = 2
    HyruleCastle = 3
    EasternPalace = 4
    DesertPalace = 5
    TowerOfHera = 6
    CastleTower = 7
    PalaceOfDarkness = 8
    SwampPalace = 9
    SkullWoods = 10
    ThievesTown = 11
    IcePalace = 12
    MiseryMire = 13
    TurtleRock = 14
    GanonsTower = 15
    OverWorld = 16


MAPS_DIR = Path("resources") / "app" / "gui" / "plandomizer" / "maps"


worlds_data = {
    World.LightWorld: {
        "entrances": location_data.lightworld_coordinates,
        "locations": location_data.lightworld_items,
        "map_file": MAPS_DIR / "lightworld512.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.DarkWorld: {
        "entrances": location_data.darkworld_coordinates,
        "locations": location_data.darkworld_items,
        "map_file": MAPS_DIR / "darkworld512.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.OverWorld: {
        "entrances": {**location_data.lightworld_coordinates, **location_data.darkworld_coordinates},
        "locations": {
            **{k: {"x": v["x"] / 2, "y": v["y"] / 2} for k, v in location_data.lightworld_items.items()},
            **{k: {"x": (v["x"] / 2) + 256, "y": v["y"] / 2} for k, v in location_data.darkworld_items.items()},
        },
        "map_file": MAPS_DIR / "overworld.png",
    },
    World.UnderWorld: {
        "locations": location_data.underworld_coordinates,
        "map_file": MAPS_DIR / "Underworld_Items_Trimmed_512.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.HyruleCastle: {
        "locations": location_data.dungeon_coordinates["Hyrule_Castle"],
        "map_file": MAPS_DIR / "Dungeons" / "Hyrule_Castle.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.EasternPalace: {
        "locations": location_data.dungeon_coordinates["Eastern_Palace"],
        "map_file": MAPS_DIR / "Dungeons" / "Eastern_Palace.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.DesertPalace: {
        "locations": location_data.dungeon_coordinates["Desert_Palace"],
        "map_file": MAPS_DIR / "Dungeons" / "Desert_Palace.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.TowerOfHera: {
        "locations": location_data.dungeon_coordinates["Tower_of_Hera"],
        "map_file": MAPS_DIR / "Dungeons" / "Tower_of_Hera.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.CastleTower: {
        "locations": location_data.dungeon_coordinates["Castle_Tower"],
        "map_file": MAPS_DIR / "Dungeons" / "Castle_Tower.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.PalaceOfDarkness: {
        "locations": location_data.dungeon_coordinates["Palace_of_Darkness"],
        "map_file": MAPS_DIR / "Dungeons" / "Palace_of_Darkness.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.SwampPalace: {
        "locations": location_data.dungeon_coordinates["Swamp_Palace"],
        "map_file": MAPS_DIR / "Dungeons" / "Swamp_Palace.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.SkullWoods: {
        "locations": location_data.dungeon_coordinates["Skull_Woods"],
        "map_file": MAPS_DIR / "Dungeons" / "Skull_Woods.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.ThievesTown: {
        "locations": location_data.dungeon_coordinates["Thieves_Town"],
        "map_file": MAPS_DIR / "Dungeons" / "Thieves_Town.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.IcePalace: {
        "locations": location_data.dungeon_coordinates["Ice_Palace"],
        "map_file": MAPS_DIR / "Dungeons" / "Ice_Palace.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.MiseryMire: {
        "locations": location_data.dungeon_coordinates["Misery_Mire"],
        "map_file": MAPS_DIR / "Dungeons" / "Misery_Mire.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.TurtleRock: {
        "locations": location_data.dungeon_coordinates["Turtle_Rock"],
        "map_file": MAPS_DIR / "Dungeons" / "Turtle_Rock.png",
        "map_image": None,
        "canvas_image": None,
    },
    World.GanonsTower: {
        "locations": location_data.dungeon_coordinates["Ganons_Tower"],
        "map_file": MAPS_DIR / "Dungeons" / "Ganons_Tower.png",
        "map_image": None,
        "canvas_image": None,
    },
}
