from src.soldier import Soldier
from src.soldier import Climber


def tile_has_soldier(tile):
    if tile and hasattr(tile, 'units') and isinstance(tile.units, list):
        for unit in tile.units:
            if issubclass(type(unit), Soldier):
                return True
    return False


def tile_count_soldier(tile):
    sum = 0
    if tile and hasattr(tile, 'units') and isinstance(tile.units, list):
        for unit in tile.units:
            if issubclass(type(unit), Soldier):
                sum += 1
    return sum


def tile_all_climber(tile):
    all_unit = True
    if tile and hasattr(tile, 'units') and isinstance(tile.units, list):
        for unit in tile.units:
            if issubclass(type(unit), Soldier):
                all_unit = all_unit and issubclass(type(unit), Climber)
    return all_unit


def tile_can_be_selected(tile):
    return tile_has_soldier(tile)


def tile_can_be_added_as_waypoint(cur_tile, sel_tile):
    sum = True
    for unit in sel_tile.units:
         if issubclass(type(unit), Soldier):
             sum = sum and hasattr(unit, 'waypoints') and isinstance(unit.waypoints, list) and cur_tile and (cur_tile.type == "PLAIN" or tile_all_climber(sel_tile))
    print(sum)
    return sum



