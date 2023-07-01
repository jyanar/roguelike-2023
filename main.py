""" A second attempt at the roguelike.
"""
import os
import tcod
from globals import Globals

os.environ["SDL_RENDER_SCALE_QUALITY"] = "best"


def main():
    g = Globals
    with tcod.context.new_terminal(
            g.SCREEN_WIDTH,
            g.SCREEN_HEIGHT,
            tileset=g.TILESET,
            title="rogu2",
            vsync=True,
    ) as context:
        root_console = tcod.console.Console(g.SCREEN_WIDTH, g.SCREEN_HEIGHT, order="F")
        while True:
            context.present(root_console, keep_aspect=True, integer_scaling=True)
            root_console.clear()


if __name__ == "__main__":

    main()
