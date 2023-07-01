
from tcod.tileset import Tileset, CHARMAP_CP437, load_tilesheet
from dataclasses import dataclass

@dataclass
class Globals:
    SCREEN_WIDTH: int = 80
    SCREEN_HEIGHT: int = 50
    MAP_WIDTH: int = 80
    MAP_HEIGHT: int = 45
    TILESET: Tileset = load_tilesheet("assets/Taffer_20x20.png", 16, 16, CHARMAP_CP437)
    # ROOM_MAX_SIZE: int = 10
    # ROOM_MIN_SIZE: int = 6
    # MAX_ROOMS: int = 30
    # MAX_MONSTERS_PER_ROOM: int = 2
