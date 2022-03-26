## New Features

## Pottery Lottery and Key Drop Shuffle Changes

### Pottery

New pottery option that control which pots (and large blocks) are in the locations pool:

* None: No pots are in the pool, like normal randomizer
* Key Pots: The pots that have keys are in the pool. This is about half of the old keydropshuffle option
* Cave Pots: The pots that are not found in dungeons are in the pool. (Includes the large block in Spike Cave). Does
not include key pots. 
* Dungeon Pots: The pots that are in dungeons are in the pool. (Includes serveral large blocks) 
* Lottery: All pots and large blocks are in the pool

By default, switches remain in their vanilla location (unless you turn on the legacy option below)

CLI `--pottery <option>` from `none, keys, lottery`

Note for multiworld: due to the design of the pottery lottery, only 256 items for other players can be under pots in your world.

### Shuffle key drops

Enemies that drop keys can have their drop shuffled into the pool. This is the other half of the keydropshuffle option.

CLI `--dropshuffle`

#### Legacy options

"Drop and Pot Keys" or `--keydropshuffle` is still availabe for use. This simply sets the pottery to keys and turns dropshuffle on as well to have the same behavior as the old setting.

The old "Pot Shuffle" option is still available under "Pot Shuffle (Legacy)" or `--shufflepots` and works the same by shuffling all pots on a supertile. It works with the lottery option as well to move the switches while having every pot in the pool.

#### Tracking Notes

The sram locations for pots and sprite drops are not yet final, please reach out for assistance or investigate the rom changes.

## Customizer

Please refer to [the documentation](docs/Customizer.md) and examples of customizer [here](docs/customizer_example.yaml) and [here](docs/multi_mystery_example.yaml)
note that entrance customization is only available with experimental features turned on.

## Experimental Entrance Shuffle

To support customizer and future entrance shuffle modes (perhaps even customizable ones), the entrance shuffle algorithm has been re-written. It is currently in an unstable state, and will use the old method unless you turn experimental features on. I'm currently in the process of evaluating most modes with different combinations of settings and checking the distribution of entrances. Entrance customization is only supported with this new experimental entrance shuffle. The experimental entrance shuffle includes prototypes of Lean and Lite entrance shuffles from the OWR branch.

## Restricted Item Placement Algorithm


The "Item Sorting" option or ```--algorithm``` has been updated with new placement algorithms. Older algorithms have been removed.
 
 When referenced below, Major Items include all Y items, all A items, all equipment (swords, shields, & armor) and Heart Containers. Dungeon items are considered major if shuffled outside of dungeons. Bomb and arrows upgrades are Major if shopsanity is turned on. The arrow quiver and universal small keys are Major if retro is turned on. Triforce Pieces are Major if that is the goal, and the Bomb Bag is Major if that is enabled.
 
 Here are the current fill options:

### Balanced 

This one stays the same as before and is recommended for the most random distribution of items.

### Vanilla Fill 

This fill attempts to place all items in their vanilla locations when possible. Obviously shuffling entrances or the dungeon interiors will often prevent items from being placed in their vanilla location. If the vanilla fill is not possible, then other locations are tried in sequence preferring "major" locations (see below), then heart piece locations, then the rest except for GT locations which are preferred last. Note the PoD small key that is normally found in the dark maze in vanilla is move to Harmless Hellway due to the placement algorithm limitation.

### Major Location Restriction

This fill attempts to place major items in major locations. Major locations are where the major items are found in the vanilla game. This includes the spot next to Uncle in the Sewers, and the Boomerang chest in Hyrule Castle.

This location pool is expanded to where dungeon items are locations if those dungeon items are shuffled. The Capacity Fairy locations are included if Shopsanity is on. If retro is enabled in addition to shopsanity, then the Old Man Sword Cave and one location in each retro cave is included. Key drop locations can be included if small or big key shuffle is on. This gives a very good balance between overworld and underworld locations though the dungeons ones will be on bosses and in big chests generally. Seeds do become more linear but usually easier to figure out.

### Dungeon Restriction

The fill attempts to place all major items in dungeons. It will overflow to the overworld if there are more items than locations (e.g. Triforce hunt.) This fill does attempt to run the GT trash fill when possible. Seeds are typically very linear but tend to be more difficult.

### District Restriction
 
The world is divided up into different regions or districts. Each dungeon is it's own district. The overworld consists of the following districts:

Light world:

* Kakariko (The main screen, blacksmith screen, and library/maze race screens)
* Northwest Hyrule (The lost woods and fortune teller all the way to the rive west of the potion shop)
* Central Hyrule (Hyrule castle, Link's House, the marsh, and the haunted grove)
* Desert (From the thief to the main desert screen)
* Lake Hylia (Around the lake)
* Eastern Hyrule (The eastern wild, the potion shop, and Zora's Domain)
* Death Mountain

Dark world:

* East Dark World (The pyramid, Palace of darkness, and Catfish)
* South Dark World (The dark lake, swamp area, to the dig game)
* Northwest Dark World (Village of Outcasts, to the Dark Sanctuary and screens in between)
* The Mire
* Dark Death Mountain

These districts are chosen at random and then filled with major items. If a location is part of a chosen district, but there are no more major items to place, a single green rupee is placed in the extra to indicate that as a placeholder. All other single green rupees are changed to be a blue rupee in order to not give false positives.

In entrance shuffle, what is shuffled to the entrances is considered instead of where the interior was originally. For example, if Blind's Hut is shuffled to the Dam, then the 5 chests in Blind's Hut are part of Central Hyrule instead of Kakariko.

Bombos Table, Lake Hylia Island, Bumper Cave Ledge, the Floating Island, Cave 45, the Graveyard Cave, Checkerboard Cave and Mimic Cave are considered part of the dark world region that you mirror from to get there (except in inverted where these are only accessible in the Light World). Note that Spectacle Rock is always part of light Death Mountain.

In multiworld, the districts chosen apply to all players.  

### CLI values:

```balanced, vanilla_fill, major_only, dungeon_only, district```

## New Hints

Based on the district algorithm above (whether it is enabled or not,) new hints can appear about that district or dungeon. For each district and dungeon, it is evaluated whether it contains vital items and how many. If it has not any vital item, items then it moves onto useful items. Useful items are generally safeties or convenience items: shields, mails, half magic, bottles, medallions that aren't required, etc. If it contains none of those and is an overworld district, then it check for a couple more things. First, if dungeons are shuffled, it looks to see if any are in the district, if so, one of those dungeons is picked for the hint. Then, if connectors are shuffled, it checks to see if you can get to unique region through a connector in that district. If none of the above apply, the district or dungeon is considered completely foolish. At least two "foolish" districts are chosen and the rest are random.


### Overworld Map shows dungeon location

Option to move indicators on overworld map to reference dungeon location. The non-default options include indicators for Hyrule Castle, Agahnim's Tower, and Ganon's Tower.

CLI ```--overworld_map```

#### Options

##### default

Status quo. Showing only the prize markers on the vanilla dungeon locations.

##### compass

The compass item controls whether the marker is moved to the dungeons locations. If you possess the compass but not the map, only a glowing X will be present regardless of dungeon prize type, if you only possess the map, the prizes will be shown in predicable locations at the bottom of the overworld map instead of the vanilla location. Light world dungeons on the light world map and dark world dungeons on the dark world map. If you posses both map and compass, then the prize of the dungeon and the location will be on the map.

If you do not shuffle the compass or map outside of the dungeon, the non-shuffled items are not needed to display the information. If a dungeon does not have a map or compass, it is not needed for the information. Talking to the bomb shop or Sahasrahla furnishes you with complete information as well as map information.

##### map

The map item plays double duty in this mode and only possession of the map will show both prize and location of the dungeon. If you do not shuffle maps or the dungeon does not have a map, the information will be displayed without needing to find any items.

## Restricted Dungeon Items on Bosses

You may now restrict the items that can appear on the boss, like the popular ambrosia preset does.

CLI: ```--restrict_boss_items <option>```

#### Options

##### none

As before, the boss may have any item including any dungeon item that could occur there.

##### mapcompass

The map and compass are logically required to defeat a boss. This prevents both of those from appearing on the dungeon boss. Note that this does affect item placement logic and the placement algorithm as maps and compasses are considered as required items to beat a boss.

##### dungeon

Same as above but both small keys and bigs keys of the dungeon are not allowed on a boss. (Note: this does not affect universal keys as they are not dungeon-specific)

## Notes and Bug Fixes

#### Volatile

* 1.0.1.12
	* Inverted bug
	* Fix for hammerdashing pots, if sprite limit is reached, items won't spawn, error beep won't play either because of other SFX
	* Killing enemies freeze + hammer results in the droppable item instead of the freeze prize
* 1.0.1.11
	* Separated Collection Rate counter from experimental
	* Added MSU Resume option
	* Ensured pots in TR Dark Ride need lamp
	* Fix for GT Crystal Conveyor not requiring Somaria/Bombs to get through
	* Fixes for Links House being at certain entrances (did not generate)
* 1.0.1.10
	* More location count fixes
	* Add major_only algorithm to code
	* Include 1.0.0.2 fixes
* 1.0.1.9
	* Every pot you pick up that wasn't part of the location pool does not count toward the location count
	* Fix for items spawning where a thrown pot was
	* Fix for vanilla_fill, it now prioritizes heart container placements
	* Fix for dungeon counter showing up in AT/HC in crossed dungeon mode
	* Fix for TR Dark Ride (again) and some ohko rules refinement
* 1.0.1.8
	* Every pot you pick up now counts toward the location count
	* A pot will de-spawn before the item under it does, error beep only plays if it still can't spawn 
	* Updated item counter & credits to support 4 digits
	* Updated compass counter to support 3 digits (up to 255)
	* Updated retro take-anys to not replace pot locations when pottery options are used
	* Updated mystery_example.yml
	* Fixed usestartinventory with mystery
	* Fixed a bug with the old pot shuffle (crashed when used)
* 1.0.1.7
	* Expanded Mystery logic options (e.g. owglitches)
	* Allowed Mystery.py to create BPS patches
	* Allow creation of BPS and SFC files (no longer mutually exclusive)
	* Pedestal goal + vanilla swords places a random sword in the pool
	* Rebalanced trash ditching algo for seeds with lots of triforce pieces
	* Added a few more places Links House shouldn't go when shuffled
	* Fixed a bug with shopsanity + district algorithm where pre-placed potions messed up the placeholder count
	* Fixed usestartinventory flag (can be use on a per player basis)
	* Fix for map indicators on keysanity menu not showing up
	* Potential sprite selector fix for systems with SSL issues
* 1.0.1.6
	* A couple new options for lighter pottery modes (Cave Pots and Dungeon Pots)
	* New option for Boss Shuffle: Unique (Prize bosses will be one of each, but GT bosses can be anything)
	* Support for BPS patch creation and applying patches during adjustment
	* Fix for SFX shuffle
	* Fix for Standard ER where locations in rain state could be in logic
	* Fix for Ice Refill room pots, require being able to hit a switch for bombbag mode
* 1.0.1.5
	* Fix for Hera Basement Cage item inheriting last pot checked
	* Update indicators on keysanity menu for overworld map option	
* 1.0.1.4
	* Reverted SRAM change (the underlying refactor isn't done yet)
* 1.0.1.3
	* Fixed inverted generation issues with pottery option
	* Moved SRAM according to SRAM standard
	* Removed equitable algorithm
	* Upped TFH goal limit to 254
	* Cuccos should no longer cause trap door rooms to not open
	* Added double click fix for install.py
	* Fix for pottery item palettes near bonkable torches
	* Fix for multiworld progression balancing would place Nothing or Arrow items
* 1.0.1.2
	* Fixed logic for pots in TR Hub and TR Dark Ride
	* Fix for districting + shopsanity
	* Hint typo correction
* 1.0.1.1
	* Fixed logic for pots in the Ice Hammer Block room (Glove + Hammer required)
	* Fixed logic for 2 pots in the Ice Antechamber (Glove required)
	* Fixed retro not saving keys when grabbed from under pots in caves
	* Fixed GUI not applying Drop shuffle when "Pot and Drops" are marked
	* Fixed dungeon counts when one of Pottery or Drops are disabled
	
#### Unstable

* 1.0.0.2
	* Include 1.0.1 fixes
	* District hint rework
* 1.0.0.1
	* Add Light Hype Fairy to bombbag mode as needing bombs
	
### From stable DoorDev

* 1.0.1
	* Fixed a bug with key doors not detecting one side of an interior door
	* Sprite selector fix for systems with SSL issues