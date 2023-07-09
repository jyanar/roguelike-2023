""" Game engine.
"""

import esper
import tcod.context
import tcod.console


class Engine:
    def __init__(
        self,
        context: tcod.context.Context,
        console: tcod.console.Console,
        screen_width: int,
        screen_height: int,
        map_width: int,
        map_height: int,
    ) -> None:
        self.context = context
        self.console = console
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.world = esper.World()





