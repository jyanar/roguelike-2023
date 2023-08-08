import color

from tcod.console import Console

def render_bar(console: Console, current_value: int, max_value: int, total_width: int) -> None:
    bar_width = int(float(current_value) / max_value * total_width)

    console.draw_rect(x=0, y=28, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=28, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=28, string=f"HP: {current_value}/{max_value}", fg=color.bar_text
    )

