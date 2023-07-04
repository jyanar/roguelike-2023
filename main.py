""" A second attempt at the roguelike.
"""

import os

import esper
from components import *
from processors import *

import tcod.console
import tcod.context
import tcod.event

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

        world = esper.World()
        world.add_processor(InputProcessor())
        world.add_processor(RenderProcessor(context=context, console=root_console))
        world.add_processor(HarmProcessor())
        world.add_processor(DirectionalActionProcessor())

        player = world.create_entity(
            NameComponent("player"),
            InputComponent(),
            RenderComponent(glyph="@"),
            PositionComponent(10,10),
            HarmableComponent(max_hp=10, hp=10),
            ObstructComponent(),
        )

        enemy = world.create_entity(
            NameComponent("goblin"),
            RenderComponent(glyph="g", fg_color=(139,69,19)),
            PositionComponent(25, 25),
            ObstructComponent()
        )

        while True:
            world.process()


if __name__ == "__main__":
    main()
