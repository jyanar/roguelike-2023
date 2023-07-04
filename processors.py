""" Set of systems that operate on entities.
"""

import tcod
import esper
from keymap import *
from components import *


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
                        self.world.add_component(ent, DirectionalActionComponent(-1, 0))
                case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        self.world.add_component(ent, DirectionalActionComponent(1, 0))
                case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        self.world.add_component(ent, DirectionalActionComponent(0, 1))
                case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        self.world.add_component(ent, DirectionalActionComponent(0, -1))


class DirectionalActionProcessor(esper.Processor):
    def _get_entity_at(self, x: int, y: int) -> int | None:
        for (ent, pc) in self.world.get_component(PositionComponent):
            if pc.x == x and pc.y == y:
                return ent
        return None

    def process(self) -> None:
        for ent, (pc,dac) in self.world.get_components(PositionComponent, DirectionalActionComponent):
            dx, dy = dac.dx, dac.dy
            xn, yn = pc.x + dx, pc.y + dy
            target = self._get_entity_at(xn, yn)
            if target and self.world.has_component(target, ObstructComponent):
                name = self.world.component_for_entity(target, NameComponent)
                print(f"path blocked by {name.name}")
            else:
                pc.x = xn
                pc.y = yn
            self.world.remove_component(ent, DirectionalActionComponent)


class RenderProcessor(esper.Processor):
    def __init__(self, context: tcod.context.Context, console: tcod.console.Console):
        super().__init__()
        self.context = context
        self.console = console

    def process(self) -> None:
        self.console.clear()
        for ent, (rc,pc) in self.world.get_components(RenderComponent, PositionComponent):
            if rc.bg_color:
                self.console.print(x=pc.x, y=pc.y, string=rc.glyph, fg=rc.fg_color, bg=rc.bg_color)
            else:
                self.console.print(x=pc.x, y=pc.y, string=rc.glyph, fg=rc.fg_color)
        self.context.present(self.console, keep_aspect=True, integer_scaling=True)
