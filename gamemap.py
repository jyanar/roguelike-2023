""" Generates and maintains the GameMap.
"""

import tcod
import esper
import numpy as np

import tile_types


class GameMap:

    world: esper.World

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def chebyshev(self, pt1: tuple[int,int], pt2: tuple[int,int]) -> int:
        return np.max([np.abs(pt1[0] - pt2[0]), np.abs(pt1[1] - pt2[1])])
    
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
	
    def is_walkable(self, x: int, y: int) -> bool:
        return self.tiles['walkable'][x][y]
    
    def get_path(self, start: tuple[int,int], target: tuple[int,int]) -> list[tuple[int,int]]:
        """
        Compute and return a path from start to target.
        If there is no valid path then returns an empty list.
        """
        cost = np.array(self.tiles["walkable"], dtype=np.int8)
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root(start)
        # Compute the path to the destination and remove the starting point.
        path: list[list[int]] = pathfinder.path_to(target)[1:].tolist()
        return [(index[0], index[1]) for index in path]
    
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
