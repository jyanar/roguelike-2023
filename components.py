""" A list of components that an entity can have.
"""

import tcod
from enum import Enum
from dataclasses import dataclass, field


# This component simply represents a keypress.
@dataclass
class KeyPressComponent:
    key: tcod.event.KeySym

# Entities with this component are processed by the input system.
@dataclass
class InputComponent:
    pass

# Provides a name for the entity.
@dataclass
class NameComponent:
    name: str

# Entities with this component have FOV computed on them.
@dataclass
class FOVComponent:
    radius: int = 8

# Can perceive other entities around it.
@dataclass
class PerceptiveComponent:
    radius: int = 4
    perceived_entities: list[int] = field(default_factory=list)

# Is renderable. Most entities do not have a bg_color.
@dataclass
class RenderComponent:
    glyph: str = "?"
    fg_color: tuple[int,int,int] = (255,255,255)
    bg_color: tuple[int,int,int] | None = None

@dataclass
class PositionComponent:
    x: int = 0
    y: int = 0

# Entities with this component will perform a directional action.
@dataclass
class DirectionalActionComponent:
    dx: int = 0
    dy: int = 0

# Is steered by AI. Could have paths here, or type of pathing, etc.
@dataclass
class AIComponent:
    pass

# Entity has an inventory. Can hold other entities that have the
# CollectibleComponent.
@dataclass
class InventoryComponent:
    contents: list[int] = field(default_factory=list)

# Entities with this component can be placed in inventory.
@dataclass
class CollectableComponent:
    pass

# Entities with this component have HP, and can be harmed/killed.
@dataclass
class HealthComponent:
    max_hp: int = 10
    hp: int = 10

# Entities with this component can damage entities with a health component.
@dataclass
class DamageComponent:
    atk: int = 3

# Entities with this component have been marked for death.
@dataclass
class DieComponent:
    pass

# Can be worn. Provides some defense. Note that entities with this should
# also have a CollectibleComponent, to allow them to be placed in inventory.
# Not clear yet how the system should be structured to ensure this.
@dataclass
class WearableComponent:
    defense: int = 3

# The states a given entity can be in. For now let's go with:
# wandering, sleeping, or hunting.
class CreatureState(Enum):
    WANDERING = 1
    SLEEPING = 2
    HUNTING = 3

@dataclass
class CreatureStateComponent:
    state: CreatureState

# Entities with this component will pursue and attack the "player" entity.
@dataclass
class HostileComponent:
    pass
