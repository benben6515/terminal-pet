#!/usr/bin/env python3
"""
Working demo of Nyan Cat without fullscreen/cursor positioning
"""

import time
import yaml
from blessed import Terminal
from graphics import Graphics
from animation import Animation


def visual_demo():
    """Run a working visual demo"""

    print("\n" + "=" * 50)
    print("NYAN CAT VISUAL DEMO - WORKING VERSION")
    print("=" * 50)
    print("\nStarting demo... (3 seconds)")
    print("Press Ctrl+C to exit early\n")
    print("Note: Clearing screen and positioning via grid-based approach\n")

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    term = Terminal()
    graphics = Graphics(term, config)
    animation = Animation(term, config)

    start_time = time.time()
    frame_count = 0

    try:
        while time.time() - start_time < 3:
            cat_x, cat_y = animation.get_position()
            frame_index = animation.get_frame_index()
            rainbow_offset = animation.get_rainbow_offset()

            cat_lines = graphics.render_cat(cat_x, cat_y, frame_index, rainbow_offset)

            output_lines = []

            for y in range(20):
                line = " " * 80
                if cat_y <= y < cat_y + len(cat_lines):
                    line_index = y - cat_y
                    if 0 <= line_index < len(cat_lines):
                        line = cat_lines[line_index].ljust(80)

                output_lines.append(line)

            print("\x1b[2J\x1b[H", end="")  # Clear screen and home
            print("\n".join(output_lines), end="")
            sys.stdout.flush()

            animation.update(0.05)
            frame_count += 1
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    print("\x1b[2J\x1b[H")  # Clear screen
    print(f"\nDemo complete! Rendered {frame_count} frames.")
    print("\nThis version uses grid-based rendering without fullscreen mode.")


if __name__ == "__main__":
    import sys

    visual_demo()
