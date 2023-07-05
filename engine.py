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


    # Let's assume that the user then just adds all the systems
    # via the world object.
    #
    # The question is, can we construct processors that can make reference to
    # the gamemap?

    # blugh duh you just need to make the different Processor classes init with
    # a reference to the gamemap.















    # def add_processors(self, processors: list[esper.Processor]) -> None:
    #     for p in processors:
    #         self.world.add_processor(p)






