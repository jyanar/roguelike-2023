""" A second attempt at the roguelike.
"""

import os

import esper
import tcod.console
import tcod.context
import tcod.event

from components import *
from processors import *
from worldgen import setup_world
# from engine import Engine

from constants import *

os.environ["SDL_RENDER_SCALE_QUALITY"] = "best"


def main() -> None:
    with tcod.context.new_terminal(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            tileset=TILESET,
            title="rogu2",
            vsync=True,
    ) as context:
        root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        world = setup_world(context, root_console, MAP_WIDTH, MAP_HEIGHT)
        # engine = Engine(context, root_console, SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT)
        while True:
            world.process()
            # engine.update()


if __name__ == "__main__":
    main()
