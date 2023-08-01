""" Game engine.

Note: currently, world updating is completely dependent on user input.
"""

import esper
import tcod.context
import tcod.console

from processors import *
from gamemap import GameMap
from worldgen import generate_dungeon
from components import KeyPressComponent


class Engine:

    def __init__(self, context: tcod.context.Context, console: tcod.console.Console):
        self.context = context
        self.console = console
        self.world = esper.World()
        self.gamemap: None | GameMap = None

    def setup(self, map_width: int, map_height: int) -> None:
        """
        Generates a gamemap, populates it with entities, and registers systems.
        """
        self.gamemap = generate_dungeon(
            map_width=map_width,
            map_height=map_height,
            room_min_size=5,
            room_max_size=10,
            max_rooms=10,
            max_monsters_per_room=2,
            world=self.world,
        )
        self.world.add_processor(InputProcessor())
        self.world.add_processor(DirectionalActionProcessor(gamemap=self.gamemap))
        self.world.add_processor(DeathProcessor())
        # world.add_processor(StateProcessor())
        self.world.add_processor(FOVProcessor(gamemap=self.gamemap))
        self.world.add_processor(HostileProcessor(gamemap=self.gamemap))
        self.world.add_processor(PerceptionProcessor(gamemap=self.gamemap))
        self.world.add_processor(RenderProcessor(context=self.context, console=self.console, gamemap=self.gamemap))
        # world.add_processor(DebugProcessor())
        self.world.process() # Kick-start everything

    def update(self) -> None:
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.KeyDown):
                kp = self.world.create_entity(KeyPressComponent(key=event.sym))
                self.world.process()
                self.world.delete_entity(kp)

