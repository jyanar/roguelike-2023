""" Set of systems that operate on entities.
"""

import tcod
import esper
from components import *


""" Let's query all units with HP, and decrease their HP.
"""
class HarmProcessor(esper.Processor):
    def process(self) -> None:
        for ent, (hc,) in self.world.get_components(HarmableComponent):
            hc.hp -= 1

class InputProcessor(esper.Processor):
    def process(self) -> None:
        for event in tcod.event.wait():
            match event:
                # Exit
                case tcod.event.Quit():
                    raise SystemExit()
                # Movement!
                case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        pc.x -= 1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        pc.x += 1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        pc.y += 1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        pc.y -= 1

class RenderProcessor(esper.Processor):
    def __init__(self, context: tcod.context.Context, console: tcod.console.Console):
        super().__init__()
        self.context = context
        self.console = console

    def process(self) -> None:
        self.console.clear()
        for ent, (rc,pc) in self.world.get_components(RenderComponent, PositionComponent):
            self.console.print(x=pc.x, y=pc.y, string=rc.glyph, fg=rc.fg_color)
        self.context.present(self.console, keep_aspect=True, integer_scaling=True)
