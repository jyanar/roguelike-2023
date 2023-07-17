""" Functions for adding systems to the ECS world, generating
the game map, and adding entities to it.
"""

import esper
import tcod
import random
from typing import Iterator

from processors import *
from components import *
import tile_types

from gamemap import GameMap



class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    @property
    def center(self) -> tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other) -> bool:
        return (self.x1 <= other.x2 
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1)


def tunnel_between(start: tuple[int,int], end: tuple[int,int]) -> Iterator[tuple[int,int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        corner_x, corner_y = x2, y1 # Move horizontally, then vertically.
    else:
        corner_x, corner_y = x1, y2 # Move vertically, then horizontally.
    # Generate coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def place_entities(room: RectangularRoom, world: esper.World, max_monsters: int) -> None:
    n_monsters = random.randint(0, max_monsters)
    locs: list[tuple[int,int]] = []
    for i in range(n_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        if not any(entity[0] == x and entity[1] == y for entity in locs):
            locs.append((x, y))
            if random.random() < 0.8:
                world.create_entity(
                    NameComponent("goblin"),
                    RenderComponent(glyph="g", fg_color=(139,69,19)),
                    PositionComponent(x, y),
                    HealthComponent(max_hp=10, hp=10),
                    PerceptiveComponent(),
                    HostileComponent(),
                    ObstructComponent(),
                    CreatureStateComponent(state=CreatureState.SLEEPING)
                )
            else:
                world.create_entity(
                    NameComponent("orc"),
                    RenderComponent(glyph="o", fg_color=(139,69,19)),
                    PositionComponent(x, y),
                    HealthComponent(max_hp=15, hp=15),
                    PerceptiveComponent(),
                    ObstructComponent(),
                    HostileComponent(),
                    CreatureStateComponent(state=CreatureState.SLEEPING)
                )


def generate_dungeon(
    map_width: int, 
    map_height: int,
    room_min_size: int,
    room_max_size: int,
    max_rooms: int,
    max_monsters_per_room: int,
    world: esper.World,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)
    rooms: list[RectangularRoom] = []
    for iroom in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
        room_x = random.randint(0, map_width - room_width - 1)
        room_y = random.randint(0, map_height - room_height - 1)

        new_room = RectangularRoom(room_x, room_y, room_width, room_height)

        ## Check that this room does not intersect with any rooms in rooms
        if any(new_room.intersects(existing_room) for existing_room in rooms):
            continue

        ## Dig out this room, add enemies, and add to list of rooms
        dungeon.tiles[new_room.inner] = tile_types.floor
        rooms.append(new_room)
        place_entities(new_room, world, max_monsters_per_room)

        if iroom == 0:
            # Place player!
            world.create_entity(
                NameComponent("player"),
                InputComponent(),
                FOVComponent(),
                RenderComponent(glyph="@"),
                PositionComponent(*rooms[iroom].center),
                HealthComponent(max_hp=10, hp=10),
                ObstructComponent(),
            )
        else:
            # Carve tunnels between rooms.
            for x, y in tunnel_between(rooms[-2].center, rooms[-1].center):
                dungeon.tiles[x, y] = tile_types.floor

    return dungeon

