from tcod.tileset import Tileset, load_tilesheet, CHARMAP_CP437

# Brogue defines a terminal window of size 34(rows) x 100(cols).
# The map size itself is 31 rows x 80 cols (or 30 rows?).
# https://github.com/search?q=repo%3Atmewett%2FBrogueCE+MESSAGE_LINES&type=code
SCREEN_WIDTH: int = 80
SCREEN_HEIGHT: int = 30
MAP_WIDTH: int = 80
MAP_HEIGHT: int = 30
TILESET: Tileset = load_tilesheet("assets/Taffer_20x20.png", 16, 16, CHARMAP_CP437)
