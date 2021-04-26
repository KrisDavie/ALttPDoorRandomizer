# Overworld Randomizer

This is a overworld randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES
based on the Door Randomizer found at [Aerinon's Github Project.](https://github.com/Aerinon/ALttPDoorRandomizer)
See https://alttpr.com/ for more details on the normal randomizer.

### Trackers & Guides

This is a very new mode of LTTPR so the tools and info is very limited. There is a [OW Rando Cheat Sheet](https://zelda.codemann8.com/images/shared/ow-rando-reference-sheet.png) that shows all the transitions that exist and are candidates for shuffle.  There is a rumor that some OW tracking capability will be coming to CodeTracker, an EmoTracker package for LTTPR.

# Known Issues
(Updated 2021-04-24)

### If you want to playtest this, know these things:
- Camera unlocking issues, which opens up the possibility of a hardlock. The workaround is to move Link around until the camera locks in place. DO NOT try to transition where there is a visible line.
- Big Red Bomb may require bomb duping as ledge drops may be in the way of your path to the Pyramid Fairy crack
- Do NOT grab the Frogsmith until you have seen the Blacksmith location. Doing so may prevent you from continuing in your save file.
- Inverted regions/rules/logic is NOT implemented yet. Generation should fail 100%.
- If you fake flipper, beware of transitioning south. You could end up at the top of the waterfall in the southeast of either world. If you mistakenly drop down, it is important to NOT make any other movements and S+Q immediately or there will be a hardlock. Falling from the waterfall is avoidable but it is super easy to do as it is super close the the transition.

### Known bugs:
- Camera unlocks, this is a known issue and will eventually be fixed at a later time
- ~~When generating, there is a message about one location that remains unfilled. You will find a Nothing item at that location.~~ _(Fixed with 0.1.0.3)_
- There may be an issue with progression being front-loaded in the seed in some scenarios, due to an unsophisticated shuffle algorithm that could make varying-sized parts of each world unreachable
- ~~Some rare instances of vanilla transitions occur when they should not, you can tell when this bug occurs because it doesn't re-center you within the gap. These cases are seemingly unreproducable, so you can re-navigate to see where it was supposed to lead. Video proof of these occurances are helpful.~~ _(Fixed with 0.1.0.4)_

# Feedback and Bug Reports

All feedback and dev conversation happens in the #ow-rando channel on the [ALTTP Randomizer discord](https://discordapp.com/invite/alttprandomizer).

# Installation

Install Python 3

Run ```pip install python-bps-continued```.  On Linux, you should use pip3.  On Windows, you may need to run ```python -m pip install python-bps-continued``` or ```py -m pip install python-bps-continued```.

Clone this repository then run ```DungeonRandomizer.py```.

Alternatively, run ```Gui.py``` for a simple graphical user interface. (WIP)

# Settings

Only extra settings are found here. All door and entrance randomizer settings are supported. See their [readme](https://github.com/Aerinon/ALttPDoorRandomizer/blob/master/README.md)

## Overworld Shuffle (--ow_shuffle)

### Full

OW Transitions are shuffled within each world separately.

### Vanilla

OW is not shuffled.

## Keep Similar Edges Together (--ow_keepsimilar)

This keeps similar edge transitions together. ie. The 2 west edges will be paired to another set of two similar edges


# Command Line Options

```
-h, --help            
```

Show the help message and exit.

```
--ow_shuffle <mode>     
```

For specifying the overworld shuffle you want as above. (default: vanilla)

```
--ow_keepsimilar     
```

This keeps similar edge transitions paired together with other pairs of transitions
