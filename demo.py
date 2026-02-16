#!/usr/bin/env python3
"""
Visual demo of the Nyan Cat Terminal Pet
Shows cat, rainbow tail, and star background for 3 seconds
"""

import time
import yaml
import sys
from blessed import Terminal
from graphics import Graphics
from animation import Animation


def visual_demo():
    """Run a visual demo of the Nyan cat"""

    print("\n" + "=" * 50)
    print("NYAN CAT VISUAL DEMO")
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
            sys.stdout.write(term.clear())
            frame_count = 0

            while time.time() - start_time < 3:
                sys.stdout.write(term.home + term.clear_eos())

                cat_x, cat_y = animation.get_position()
                frame_index = animation.get_frame_index()
                rainbow_offset = animation.get_rainbow_offset()

                output = []

                stars = graphics.render_stars()
                for y, x, star in stars:
                    output.append(term.move(y, x) + star)

                rainbow_tail = graphics.render_rainbow_tail(
                    cat_x, cat_y, 10, rainbow_offset
                )
                for y, x, segment in rainbow_tail:
                    if x >= 0:
                        output.append(term.move(y, x) + segment)

                cat_lines = graphics.render_cat(
                    cat_x, cat_y, frame_index, rainbow_offset
                )
                for line_index, line in enumerate(cat_lines):
                    output.append(term.move(cat_y + line_index, cat_x) + line)

                sys.stdout.write("".join(output))
                sys.stdout.flush()

                animation.update(0.016)
                frame_count += 1

                time.sleep(0.016)

        except KeyboardInterrupt:
            pass

        sys.stdout.write(term.clear())
        sys.stdout.write(f"\nDemo complete! Rendered {frame_count} frames.\n")
        sys.stdout.write(
            "\nRun 'python main.py' for the full interactive experience!\n"
        )
        sys.stdout.write("Press 'h' for help when running the full version.\n")
        sys.stdout.flush()


if __name__ == "__main__":
    visual_demo()
