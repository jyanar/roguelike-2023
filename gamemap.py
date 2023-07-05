""" Generates and maintains the GameMap.
"""

import tcod
import numpy as np

import tile_types


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
	
    def is_walkable(self, x: int, y: int) -> bool:
        return self.tiles['walkable'][x][y]
    
    def render(self, console: tcod.console.Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't but is in the "explored" array, then draw it with the "dark" colors.
        Otherwise, default is "SHROUD"
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        # sorted_entities_for_rendering = sorted(
        #     self.entities, key=lambda x: x.render_order.value
        # )

        # for entity in sorted_entities_for_rendering:
        #     # Only print entities in the FOV.
        #     if self.visible[entity.x, entity.y]:
        #         console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
