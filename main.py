""" A second attempt at the roguelike.
"""

import os
import tcod

from components import *
from processors import *
from engine import Engine

from constants import *

os.environ["SDL_RENDER_SCALE_QUALITY"] = "nearest"


def main() -> None:
    context = tcod.context.new_terminal(
        SCREEN_WIDTH*2, SCREEN_HEIGHT*2, tileset=TILESET, title="rogu2", vsync=True
    )
    root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
    engine = Engine(context, root_console)
    engine.setup(MAP_WIDTH, MAP_HEIGHT)
    while True:
        engine.update()


if __name__ == "__main__":
    main()
