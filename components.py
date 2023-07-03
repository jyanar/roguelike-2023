""" A list of components that an entity can have.

Some ideas from Jumpdrive:
    sys := ecs.NewSystem(
        InputComponent,
        WorldComponent,
        WeatherComponent,
        ShootComponent,
        HarmableComponent,
        PlayerComponent,
        WanderComponent,
        PositionComponent,
        InventoryComponent,
        CollectableComponent,
        PerceptiveComponent,
        BlockingComponent,
    )
"""

from entity import Entity
from dataclasses import dataclass
from typing import List

# Entities with this component are processed by the input system.
@dataclass
class InputComponent:
    pass

# Entities with this component have FOV computed on them. Might consider
# changing this to be an "FOVComponent" and a "NameComponent".
@dataclass
class PlayerComponent:
    name: str = "adventurer"

# Is renderable. Most entities do not have a bg_color. Walls do.
@dataclass
class RenderComponent:
    glyph: str = "?"
    fg_color: tuple[int,int,int] = (255,255,255)
    bg_color: tuple[int,int,int] | None = None

@dataclass
class PositionComponent:
    x: int = 0
    y: int = 0

# Is steered by AI. Could have paths here, or type of pathing, etc.
@dataclass
class AIComponent:
    pass

# Entity has an inventory. Can hold other entities that have the
# CollectibleComponent.
@dataclass
class InventoryComponent:
    contents: list

# Entities with this component can be placed in inventory.
@dataclass
class CollectableComponent:
    pass

# Entities with this component cannot be walked through. e.g. walls.
@dataclass
class ObstructComponent:
    pass

# Entities with this component have HP, and can be killed.
@dataclass
class HarmableComponent:
    max_hp: int = 10
    hp: int = 10

# Can be worn. Provides some defense. Note that entities with this should
# also have a CollectibleComponent, to allow them to be placed in inventory.
# Not clear yet how the system should be structured to ensure this.
@dataclass
class WearableComponent:
    defense: int = 3

# Can perceive other entities around it.
@dataclass
class PerceptiveComponent:
    dist: int = 10

