""" Set of systems that operate on entities.
"""

import tcod
import esper

from components import *
from constants import *
from gamemap import GameMap
from keymap import WAIT_KEYS, MOVE_KEYS
from render_functions import render_bar


class InputProcessor(esper.Processor):
    def process(self) -> None:
        for ent, (kp,) in self.world.get_components(KeyPressComponent):
            key = kp.key
            if key == tcod.event.KeySym.ESCAPE:
                raise SystemExit()
            elif key in WAIT_KEYS:
                return
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
            xn, yn = pc.x + dac.dx, pc.y + dac.dy

            if not self.gamemap.in_bounds(xn, yn):
                continue

            e_name = self.world.component_for_entity(ent, NameComponent).name
            if not self.gamemap.is_walkable(xn, yn):
                print(f"{e_name} bumps against the wall!")
                continue

            target = self._get_entity_at(xn, yn)
            if target and self.world.has_component(target, ObstructComponent):
                t_name   = self.world.component_for_entity(target, NameComponent).name
                t_health = self.world.component_for_entity(target, HealthComponent)
                e_attack = self.world.component_for_entity(ent,    DamageComponent)
                print(f"{e_name} attacks {t_name} for {e_attack.atk} damage!")
                t_health.hp -= e_attack.atk
                if t_health.hp <= 0:
                    t_health.hp = 0
                    self.world.add_component(target, DieComponent())

            else:
                pc.x = xn
                pc.y = yn


class DeathProcessor(esper.Processor):
    def process(self) -> None:
        for ent, (dc,) in self.world.get_components(DieComponent):
            self.world.remove_component(ent, DieComponent)
            self.world.remove_component(ent, ObstructComponent)
            if self.world.has_component(ent, PerceptiveComponent):
                self.world.remove_component(ent, PerceptiveComponent)
            if self.world.has_component(ent, InputComponent):
                self.world.remove_component(ent, InputComponent)
            name = self.world.component_for_entity(ent, NameComponent).name
            self.world.add_component(ent, NameComponent(f"Remains of {name}"))
            self.world.add_component(ent, RenderComponent(glyph="%", fg_color=(191,0,0), order=RenderOrder.CORPSE))
            print(f"{name} has died.")


# TODO Issue with having multiple entities w/ FOV. Fine if just one.
class FOVProcessor(esper.Processor):
    def __init__(self, gamemap: GameMap):
        self.gamemap = gamemap

    def process(self) -> None:
        for ent, (fc,pc) in self.world.get_components(FOVComponent, PositionComponent):
            self.gamemap.visible[:] = tcod.map.compute_fov(
                self.gamemap.tiles["transparent"],
                (pc.x, pc.y),
                radius=fc.radius,
            )
            # If a tile is "visible" it should be added to "explored"
            self.gamemap.explored |= self.gamemap.visible


# Checks entities that are within radius specified by PerceptionComponent, and
# add them to a list of perceived entitites.
class PerceptionProcessor(esper.Processor):
    def __init__(self, gamemap: GameMap):
        self.gamemap = gamemap

    def _get_entity_at(self, x: int, y: int) -> int | None:
        for (ent, pc) in self.world.get_component(PositionComponent):
            if pc.x == x and pc.y == y:
                return ent
        return None
    
    def process(self) -> None:
        for ent, (pos,per) in self.world.get_components(PositionComponent, PerceptiveComponent):
            per.perceived_entities = []
            x, y = pos.x, pos.y # current entity position
            # Now let's add all entities that are within perceptible radius
            # NOTE: This does not scale!
            for otherentity, (pos,) in self.world.get_components(PositionComponent):
                if ent != otherentity and self.gamemap.chebyshev((x, y), (pos.x, pos.y)) <= per.radius:
                    per.perceived_entities.append(otherentity)


# Entities with Hostile component are processed here and will begin pathing towards 
# the player, assuming the player is perceived. Longer-term it might be better to be able
# to specify which types of entities a given creature is hostile to, not just the player.
class HostileProcessor(esper.Processor):
    def __init__(self, gamemap: GameMap):
        self.gamemap = gamemap

    def process(self) -> None:
        for ent, (hostile,percept,pos) in self.world.get_components(HostileComponent, PerceptiveComponent, PositionComponent):
            if len(percept.perceived_entities) > 0:
                # Check through perceived entities. If any are the player, move towards them
                for percieved_ent in percept.perceived_entities:
                    name = self.world.component_for_entity(percieved_ent, NameComponent).name
                    if name == "player":
                        # Compute path to player
                        playerpos = self.world.component_for_entity(percieved_ent, PositionComponent)
                        path = self.gamemap.get_path((pos.x, pos.y), (playerpos.x, playerpos.y))
                        if path:
                            dest_x, dest_y = path.pop(0)
                            self.world.add_component(ent, DirectionalActionComponent(dest_x - pos.x, dest_y - pos.y))


class StateProcessor(esper.Processor):
    def process(self) -> None:
        for ent, (nc, csc) in self.world.get_components(NameComponent, CreatureStateComponent):
            name = nc.name
            current_state = csc.state
            print(f"{name} is currently: {current_state}")


class RenderProcessor(esper.Processor):
    def __init__(self, context: tcod.context.Context, console: tcod.console.Console, gamemap: GameMap):
        self.context = context
        self.console = console
        self.gamemap = gamemap

    def process(self) -> None:
        self.console.clear()
        # Render the game map
        self.gamemap.render(self.console)
        # Render entities
        entities_to_draw = []
        for ent, (rc,pc) in self.world.get_components(RenderComponent, PositionComponent):
            if self.gamemap.visible[pc.x, pc.y]:
                entities_to_draw.append((ent, rc, pc))
        entities_to_draw.sort(key=lambda x: x[1].order.value)
        for ent, rc, pc in entities_to_draw:
            self.console.print(x=pc.x, y=pc.y, string=rc.glyph, fg=rc.fg_color)
        # Render HP bars, menus, etc
        # We know that the player is the first entity, by convention.
        hpc = self.world.component_for_entity(1, HealthComponent)
        # self.console.print(x=10, y=10, string=f"HP: {hpc.hp}/{hpc.max_hp}")
        render_bar(self.console, hpc.hp, hpc.max_hp, 20)
        self.context.present(self.console, keep_aspect=True, integer_scaling=True)


# Prints out components and their data for each entity
class DebugProcessor(esper.Processor):
    def process(self) -> None:
        print('\n=========================================')
        print('=========== Next tick ===================')
        print('=========================================\n')
        for ent in self.world._entities:
            comps = self.world.components_for_entity(ent)
            print("-------------")
            print(f"Entity {ent}:")
            for c in comps:
                print(c)
            


