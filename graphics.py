from blessed import Terminal
import random
from cat_state import CatState


class Graphics:
    def __init__(self, terminal: Terminal, config: dict):
        self.term = terminal
        self.config = config
        self.colors = config["colors"]

        self.cat_frames = self._generate_all_cat_frames()
        self.stars = []
        self._init_stars()

    def _generate_all_cat_frames(self):
        return {
            CatState.IDLE: self._generate_idle_frames(),
            CatState.WALKING: self._generate_walking_frames(),
            CatState.EATING: self._generate_eating_frames(),
            CatState.SLEEPING: self._generate_sleeping_frames(),
            CatState.GROOMING: self._generate_grooming_frames(),
            CatState.PLAYING: self._generate_playing_frames(),
            CatState.STRETCHING: self._generate_stretching_frames(),
            CatState.HUNGRY: self._generate_hungry_frames(),
            CatState.HAPPY: self._generate_happy_frames(),
            CatState.SAD: self._generate_sad_frames(),
        }

    def _generate_idle_frames(self):
        frame1 = [
            "    /\\_/\\     ",
            "   ( o.o )    ",
            "    > ^ <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( -.- )    ",
            "    > o <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
        ]
        return self._normalize_frames([frame1, frame2, frame1, frame2])

    def _generate_walking_frames(self):
        frame1 = [
            "    /\\_/\\     ",
            "   ( o.o )    ",
            "    > ^ <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     / \\      ",
            "    /   \\     ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( o.o )    ",
            "    > ^ <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "    /   \\     ",
            "   /     \\    ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _generate_eating_frames(self):
        frame1 = [
            "    /\\_/\\     ",
            "   ( ^o^ )    ",
            "    > w <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
            "   [ FOOD ]   ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( owo )    ",
            "    > ~ <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
            "   [ FOOD ]   ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _generate_sleeping_frames(self):
        frame1 = [
            "   __.---.__  ",
            "  /   - -   \\ ",
            " (   -   -   )",
            "  \\___-___/   ",
            "   |     |    ",
        ]
        frame2 = [
            "   __.---.__  ",
            "  /   - -   \\ ",
            " (   -   -   )",
            "  \\___-___/   ",
            "   |  z  |    ",
        ]
        frame3 = [
            "   __.---.__  ",
            "  /   - -   \\ ",
            " (   -   -   )",
            "  \\___-___/   ",
            "   | z Z |    ",
        ]
        return self._normalize_frames([frame1, frame2, frame3, frame2])

    def _generate_grooming_frames(self):
        frame1 = [
            "    /\\_/\\     ",
            "   ( o.o )    ",
            "    > ^ <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_^^_ /    ",
            "    | |       ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( -.- )    ",
            "    > w <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_^^_ /    ",
            "    | |       ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _generate_playing_frames(self):
        frame1 = [
            "     /\\_/\\    ",
            "    ( ^o^ )   ",
            "     >  <     ",
            "    /    \\    ",
            "   (      )   ",
            "    \\____/    ",
            "      \\/     ",
            "      /\\      ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( >w< )    ",
            "    > ^^<     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     /\\      ",
            "    /  \\     ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _generate_stretching_frames(self):
        frame1 = [
            "       /\\_/\\     ",
            "      ( -.- )    ",
            "       >   <     ",
            "      /     \\    ",
            "     (       )   ",
            "      \\_____/    ",
            "       | |       ",
        ]
        frame2 = [
            "        /\\_/\\    ",
            "       ( o.o )   ",
            "        > ~ <    ",
            "       /     \\   ",
            "      (       )  ",
            "       \\_____/   ",
            "        | |      ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _generate_hungry_frames(self):
        frame1 = [
            "    /\\_/\\     ",
            "   ( . . )    ",
            "    > ~ <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( . . )    ",
            "    > - <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _generate_happy_frames(self):
        frame1 = [
            "    /\\_/\\     ",
            "   ( ^w^ )    ",
            "    > ^^<     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
            "   ~~~~~~~~   ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( >w< )    ",
            "    > ^^<     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
            "   ~~~~~~~~   ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _generate_sad_frames(self):
        frame1 = [
            "    /\\_/\\     ",
            "   ( T_T )    ",
            "    >   <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
        ]
        frame2 = [
            "    /\\_/\\     ",
            "   ( ;_; )    ",
            "    >   <     ",
            "   /     \\    ",
            "  (       )   ",
            "   \\_____/    ",
            "     | |      ",
        ]
        return self._normalize_frames([frame1, frame2])

    def _normalize_frames(self, frames):
        max_width = max(len(line) for frame in frames for line in frame)
        max_height = max(len(frame) for frame in frames)
        normalized = []
        for frame in frames:
            while len(frame) < max_height:
                frame.append(" " * max_width)
            normalized_frame = [line.ljust(max_width) for line in frame]
            normalized.append(normalized_frame)
        return normalized

    def _init_stars(self):
        num_stars = self.config["display"]["background_stars"]
        for _ in range(num_stars):
            self.stars.append(
                {
                    "x": random.randint(0, 100),
                    "y": random.randint(0, 30),
                    "color": random.choice(self.colors["star_colors"]),
                    "twinkle_speed": random.uniform(0.5, 2.0),
                    "type": random.choice([".", "+", "*"]),
                }
            )

    def get_rainbow_color(self, position, offset):
        rainbow_colors = self.colors["rainbow_gradient"]
        color_index = (position + offset) % len(rainbow_colors)
        return rainbow_colors[color_index]

    def render_cat(self, x, y, frame_index, rainbow_offset, cat_state=CatState.IDLE):
        state_frames = self.cat_frames.get(cat_state, self.cat_frames[CatState.IDLE])
        frame = state_frames[frame_index % len(state_frames)]
        return frame

    def colorize_char(self, char, line_index, char_index, rainbow_offset):
        if char == " ":
            return char
        elif char in [
            "\\",
            "/",
            "|",
            "_",
            "-",
            "~",
            "^",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            ".",
            "+",
            "*",
        ]:
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
            brightness = random.random() > 0.3
            if brightness:
                color_num = star["color"]
                star_char = star["type"]
                rendered.append(
                    (
                        star["y"],
                        star["x"],
                        self.term.color(color_num) + star_char + self.term.normal,
                    )
                )
        return rendered

    def render_rainbow_tail(self, x, y, length, rainbow_offset):
        tail_segments = []
        for i in range(length):
            tail_x = x - i - 16
            color_num = self.get_rainbow_color(i, rainbow_offset)
            wave = int(2 * (i % 3 - 1))
            segment = self.term.color(color_num) + "=" + self.term.normal
            tail_segments.append((y + 4 + wave, tail_x, segment))
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
