""" Functions for adding systems to the ECS world, generating
the game map, and adding entities to it.
"""

import esper
import tcod

from processors import *
from components import *

from gamemap import GameMap


def setup_world(
        context: tcod.context.Context,
        console: tcod.console.Console,
        map_width: int,
        map_height: int,
    ) -> esper.World:

    gamemap = GameMap(map_width, map_height)

    world = esper.World()
    world.add_processor(InputProcessor())
    world.add_processor(RenderProcessor(context=context, console=console, gamemap=gamemap))
    world.add_processor(DirectionalActionProcessor(gamemap=gamemap))

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
        ObstructComponent(),
    )

    return world
