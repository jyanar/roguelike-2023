""" A second attempt at the roguelike.
"""

import os
import tcod.console
import tcod.context
import tcod.event
from tcod.tileset import Tileset, load_tilesheet, CHARMAP_CP437

os.environ["SDL_RENDER_SCALE_QUALITY"] = "best"

SCREEN_WIDTH: int = 80
SCREEN_HEIGHT: int = 50
MAP_WIDTH: int = 80
MAP_HEIGHT: int = 45
TILESET: Tileset = load_tilesheet("assets/Taffer_20x20.png", 16, 16, CHARMAP_CP437)

def main() -> None:
    player_x: int = 10
    player_y: int = 10
    tcod.tileset.procedural_block_elements(tileset=TILESET)


    with tcod.context.new_terminal(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            tileset=TILESET,
            title="rogu2",
            vsync=True,
    ) as context:
        root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            root_console.clear()
            root_console.print(x=player_x, y=player_y, string="@")
            context.present(root_console)#, keep_aspect=True, integer_scaling=True)
            for event in tcod.event.wait():
                match event:
                    case tcod.event.Quit():
                        raise SystemExit()
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                        player_x -= 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                        player_x += 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                        player_y += 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                        player_y -= 1



if __name__ == "__main__":
    main()


# def main() -> None:
#     """Entry point function."""
#     tileset = tcod.tileset.load_tilesheet(
#         "data/Alloy_curses_12x12.png", columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
#     )
#     tcod.tileset.procedural_block_elements(tileset=tileset)
#     console = tcod.console.Console(80, 50)
#     state = ExampleState(player_x=console.width // 2, player_y=console.height // 2)
#     with tcod.context.new(console=console, tileset=tileset) as context:
#         while True:  # Main loop
#             console.clear()  # Clear the console before any drawing
#             state.on_draw(console)  # Draw the current state
#             context.present(console)  # Render the console to the window and show it
#             for event in tcod.event.wait():  # Event loop, blocks until pending events exist
#                 print(event)
#                 state.on_event(event)  # Dispatch events to the state