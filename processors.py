""" Set of systems that operate on entities.
"""

import tcod
import esper

from components import *
from constants import *
from gamemap import GameMap
from keymap import WAIT_KEYS, MOVE_KEYS


# Docs: https://python-tcod.readthedocs.io/en/latest/tcod/event.html
class InputProcessor(esper.Processor):
    def process(self) -> None:
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key == tcod.event.KeySym.ESCAPE:
                    raise SystemExit()
                elif key in WAIT_KEYS:
                    continue
                elif key in MOVE_KEYS:
                    dx, dy = MOVE_KEYS[key]
                    for ent, (ic,pc) in self.world.get_components(InputComponent, PositionComponent):
                        self.world.add_component(ent, DirectionalActionComponent(dx, dy))


class DirectionalActionProcessor(esper.Processor):
    def __init__(self, gamemap: GameMap):
        self.gamemap = gamemap

    def _get_entity_at(self, x: int, y: int) -> int | None:
        for (ent, pc) in self.world.get_component(PositionComponent):
            if pc.x == x and pc.y == y:
                return ent
        return None

    def process(self) -> None:
        for ent, (pc,dac) in self.world.get_components(PositionComponent, DirectionalActionComponent):
            self.world.remove_component(ent, DirectionalActionComponent) # consume
            dx, dy = dac.dx, dac.dy
            xn, yn = pc.x + dx, pc.y + dy
            if not self.gamemap.in_bounds(xn, yn):
                continue
            if not self.gamemap.is_walkable(xn, yn):
                print("The wall is firm and unyielding!")
                continue
            target = self._get_entity_at(xn, yn)
            if target and self.world.has_component(target, ObstructComponent):
                name = self.world.component_for_entity(target, NameComponent).name
                print(f"You attack the {name}!")
            else:
                pc.x = xn
                pc.y = yn


class RenderProcessor(esper.Processor):
    def __init__(self, context: tcod.context.Context, console: tcod.console.Console, gamemap: GameMap):
        super().__init__()
        self.context = context
        self.console = console
        self.gamemap = gamemap

    def process(self) -> None:
        self.console.clear()
        self.gamemap.render(self.console)
        for ent, (rc,pc) in self.world.get_components(RenderComponent, PositionComponent):
            if rc.bg_color:
                self.console.print(x=pc.x, y=pc.y, string=rc.glyph, fg=rc.fg_color, bg=rc.bg_color)
            else:
                self.console.print(x=pc.x, y=pc.y, string=rc.glyph, fg=rc.fg_color)
        self.context.present(self.console, keep_aspect=True, integer_scaling=True)

