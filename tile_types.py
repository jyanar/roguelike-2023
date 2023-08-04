import numpy as np


# Tile graphics structured type compatible with Console.tiles_rgb
graphic_dt = np.dtype(
	[
		("ch", np.int32), # unicode
		("fg", "3B"),     # 3 unsigned bytes for RGB
		("bg", "3B"),
	]
)

# Tile struct used for statically defined tile data
tile_dt = np.dtype(
	[
		("walkable", bool),    # True if can be walked over
		("transparent", bool), # True if this tile doesn't block FOV
		("dark", graphic_dt),  # Graphics for when this tile is not in FOV
		("light", graphic_dt), # Graphics for when the tile in FOV
	]
)

def new_tile(
	*,
	walkable: int,
	transparent: int,
	dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
	light: tuple[int, tuple[int, int, int], tuple[int, int, int]],
) -> np.ndarray:
	"""Helper function for defining individual tile types."""
	return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord("."), (255,255,255), (50,50,150)),
	light=(ord("."), (255,255,255), (200,180,50)),
)
wall = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord(" "), (255,255,255), (0,0,100)),
	light=(ord(" "), (255,255,255), (130,110,50)),
)


# floor = new_tile(
# 	walkable=True,
# 	transparent=True,
# 	dark=(ord("."), (120,120,120), (8,10,29)),
# 	light=(ord("."), (120,120,120), (16,20,59)),
# )

# wall = new_tile(
# 	walkable=False,
# 	transparent=False,
# 	dark=(ord(" "), (120,120,120), (0,0,100)),
# 	light=(ord(" "), (120,120,120), (255, 172, 28)),
# )