from blessed import Terminal
import random


class Graphics:
    def __init__(self, terminal: Terminal, config: dict):
        self.term = terminal
        self.config = config
        self.colors = config["colors"]

        self.cat_frames = self._generate_cat_frames()
        self.stars = []
        self._init_stars()

    def _generate_cat_frames(self):
        frames = []

        frame1 = [
            "      /\\_/\\      ",
            "     ( o.o )     ",
            "      > ^ <      ",
            "     /      \\    ",
            "    /        \\   ",
            "   /          \\  ",
            "  /____________\\ ",
        ]

        frame2 = [
            "      /\\_/\\      ",
            "     ( -.- )     ",
            "      > o <      ",
            "     /      \\    ",
            "    /        \\   ",
            "   /          \\  ",
            "  /____________\\ ",
        ]

        frame3 = [
            "      /\\_/\\      ",
            "     ( o.o )     ",
            "      > o <      ",
            "     /      \\    ",
            "    /        \\   ",
            "   /          \\  ",
            "  /____________\\ ",
        ]

        max_len = max(len(line) for line in frame1)
        for frame in [frame1, frame2, frame3]:
            for i in range(len(frame)):
                frame[i] = frame[i].ljust(max_len)

        frames.extend([frame1, frame2, frame3, frame2])
        return frames

    def _init_stars(self):
        num_stars = self.config["display"]["background_stars"]
        for _ in range(num_stars):
            self.stars.append(
                {
                    "x": random.randint(0, 80),
                    "y": random.randint(0, 20),
                    "color": random.choice(self.colors["star_colors"]),
                    "twinkle_speed": random.uniform(0.5, 2.0),
                }
            )

    def get_rainbow_color(self, position, offset):
        rainbow_colors = self.colors["rainbow_gradient"]
        color_index = (position + offset) % len(rainbow_colors)
        return rainbow_colors[color_index]

    def render_cat(self, x, y, frame_index, rainbow_offset):
        frame = self.cat_frames[frame_index % len(self.cat_frames)]
        return frame

    def colorize_char(self, char, line_index, char_index, rainbow_offset):
        if char == " ":
            return char
        elif char in ["\\", "/", "|", "_", "~"]:
            rainbow_pos = line_index + char_index
            color_num = self.get_rainbow_color(rainbow_pos, rainbow_offset)
            return self.term.color(color_num) + char + self.term.normal
        elif line_index < 3:
            return self.term.color(self.colors["face_color"]) + char + self.term.normal
        else:
            return self.term.color(self.colors["body_color"]) + char + self.term.normal

    def render_stars(self):
        rendered = []
        for star in self.stars:
            brightness = int(random.uniform(0, 1) > 0.5)
            if brightness:
                color_num = star["color"]
                rendered.append(
                    (
                        star["y"],
                        star["x"],
                        self.term.color(color_num) + "✧" + self.term.normal,
                    )
                )
        return rendered

    def render_rainbow_tail(self, x, y, length, rainbow_offset):
        tail_segments = []
        for i in range(length):
            tail_x = x - i - 18
            color_num = self.get_rainbow_color(i, rainbow_offset)
            segment = self.term.color(color_num) + "▄" + self.term.normal
            tail_segments.append((y + 5, tail_x, segment))
        return tail_segments

    def render_stats(self, hunger, mood, energy):
        colors = self.colors

        def render_bar(label, value, color):
            filled = int(value / 10)
            bar = (
                self.term.color(color)
                + "█" * filled
                + self.term.dim
                + "░" * (10 - filled)
                + self.term.normal
            )
            return f"{label}: {bar} {value}%"

        stats_lines = [
            self.term.bold + "NYAN CAT STATUS" + self.term.normal,
            render_bar("Hunger", hunger, colors["rainbow_gradient"][0]),
            render_bar("Mood", mood, colors["rainbow_gradient"][3]),
            render_bar("Energy", energy, colors["rainbow_gradient"][5]),
            self.term.dim + "Press [h] for help" + self.term.normal,
        ]

        return stats_lines

    def render_help(self):
        controls = self.config["controls"]
        help_lines = [
            self.term.bold + "CONTROLS:" + self.term.normal,
            f"[{controls['feed_key']}] Feed  - Decrease hunger",
            f"[{controls['play_key']}] Play  - Increase mood, decrease energy",
            f"[{controls['pet_key']}] Pet   - Increase mood",
            f"[{controls['sleep_key']}] Sleep - Restore energy",
            f"[{controls['help_key']}] Help  - Show this menu",
            f"[{controls['quit_key']}] Quit  - Exit",
        ]
        return help_lines

    def render_message(self, message, duration):
        return self.term.bold + self.term.center(message) + self.term.normal
