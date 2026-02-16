#!/usr/bin/env python3
"""
Simple working demo of Nyan Cat
"""

import time
import yaml
import sys
from blessed import Terminal
from graphics import Graphics
from animation import Animation


def visual_demo():
    """Run a visual demo of Nyan cat"""

    print("\n" + "=" * 50)
    print("NYAN CAT VISUAL DEMO - SIMPLE VERSION")
    print("=" * 50)
    print("\nStarting demo... (3 seconds)")
    print("Press Ctrl+C to exit early\n")

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    term = Terminal()

    with term.fullscreen(), term.hidden_cursor():
        graphics = Graphics(term, config)
        animation = Animation(term, config)

        start_time = time.time()
        frame_count = 0

        try:
            while time.time() - start_time < 3:
                print(term.clear(), end="")

                cat_x, cat_y = animation.get_position()
                frame_index = animation.get_frame_index()
                rainbow_offset = animation.get_rainbow_offset()

                stars = graphics.render_stars()
                for y, x, star in stars:
                    print(term.move(y, x) + star, end="", flush=True)

                rainbow_tail = graphics.render_rainbow_tail(
                    cat_x, cat_y, 10, rainbow_offset
                )
                for y, x, segment in rainbow_tail:
                    if x >= 0:
                        print(term.move(y, x) + segment, end="", flush=True)

                cat_lines = graphics.render_cat(
                    cat_x, cat_y, frame_index, rainbow_offset
                )
                for line_index, line in enumerate(cat_lines):
                    print(
                        term.move(cat_y + line_index, cat_x) + line, end="", flush=True
                    )

                print(term.move(term.height - 1, 0), end="", flush=True)

                animation.update(0.5)
                frame_count += 1
                time.sleep(0.5)

        except KeyboardInterrupt:
            pass

        print(term.clear())
        print(f"\nDemo complete! Rendered {frame_count} frames.")
        print("\nRun 'python main.py' for the full interactive experience!")
        print("Press 'h' for help when running the full version.")


if __name__ == "__main__":
    visual_demo()
