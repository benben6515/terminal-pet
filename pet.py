import time
import random
import sys
from blessed import Terminal
from graphics import Graphics
from animation import Animation
from stats import Stats
from interaction import Interaction
from cat_state import CatStateMachine, CatState


class Pet:
    def __init__(self, terminal: Terminal, config: dict):
        self.term = terminal
        self.config = config

        self.graphics = Graphics(terminal, config)
        self.animation = Animation(terminal, config)
        self.stats = Stats(config)
        self.interaction = Interaction(terminal, config)
        self.state_machine = CatStateMachine(config)

        self.last_update = time.time()
        self.random_behavior_timer = 0
        self.random_behavior_interval = random.uniform(5, 10)
        self.first_render = True

    def update(self):
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time

        stats_data = self.stats.get_stats()
        self.state_machine.update(dt, stats_data)

        current_state = self.state_machine.get_state()
        self.animation.update(dt, current_state)

        self.stats.update(dt)
        self.interaction.update(dt)
        self._update_random_behavior(dt)

    def _update_random_behavior(self, dt):
        self.random_behavior_timer += dt

        if self.random_behavior_timer >= self.random_behavior_interval:
            self._trigger_random_behavior()
            self.random_behavior_timer = 0
            self.random_behavior_interval = random.uniform(5, 10)

    def _trigger_random_behavior(self):
        current_state = self.state_machine.get_state()

        if current_state in [CatState.SLEEPING, CatState.EATING]:
            return

        behavior = random.choice(["meow", "stretch", "wag", "blink", "twitch"])

        if behavior == "meow":
            messages = ["*meow*", "Nyan says: Meow~", "~purr purr~", "Mrrrow?"]
            self.interaction._show_message(random.choice(messages))
        elif behavior == "stretch":
            self.state_machine.change_state(CatState.STRETCHING, duration=2.0)
            self.interaction._show_message("Nyan stretches! 🐱")
        elif behavior == "wag":
            self.interaction._show_message("Nyan wags its tail! ✨")
        elif behavior == "blink":
            self.interaction._show_message("*blink*")
        elif behavior == "twitch":
            self.interaction._show_message("*ear twitch*")

    def handle_input(self, key):
        action = self.interaction.handle_key(key, self.stats)

        if action == "feed":
            self.state_machine.on_feed()
            self.interaction._show_message("Nyan is eating! Yummy! 🍽️")
        elif action == "play":
            self.state_machine.on_play()
            self.interaction._show_message("Nyan is playing! So fun! 🎮")
        elif action == "pet":
            self.state_machine.on_pet()
            self.interaction._show_message("Nyan purrs happily! 😺")
        elif action == "sleep":
            self.state_machine.on_sleep()
            self.interaction._show_message("Nyan curls up to sleep... 💤")
        elif action == "quit":
            return "quit"

        return None

    def render(self):
        cat_x, cat_y = self.animation.get_position()
        frame_index = self.animation.get_frame_index()
        rainbow_offset = self.animation.get_rainbow_offset()
        current_state = self.state_machine.get_state()

        screen_height = self.term.height
        screen_width = self.term.width

        sys.stdout.write("\x1b[2J\x1b[H")

        grid = []
        for y in range(screen_height):
            grid.append([" "] * screen_width)

        stars = self.graphics.render_stars()
        for y, x, star in stars:
            if 0 <= y < screen_height and 0 <= x < screen_width:
                grid[y][x] = star

        if current_state not in [CatState.SLEEPING, CatState.GROOMING, CatState.EATING]:
            rainbow_tail = self.graphics.render_rainbow_tail(
                cat_x, cat_y, 10, rainbow_offset
            )
            for y, x, segment in rainbow_tail:
                if 0 <= y < screen_height and 0 <= x < screen_width:
                    grid[y][x] = segment

        cat_lines = self.graphics.render_cat(
            cat_x, cat_y, frame_index, rainbow_offset, current_state
        )
        for line_index, line in enumerate(cat_lines):
            line_y = cat_y + line_index
            if 0 <= line_y < screen_height:
                for char_index, char in enumerate(line):
                    pos_x = cat_x + char_index
                    if 0 <= pos_x < screen_width and char != " ":
                        colored = self.graphics.colorize_char(
                            char, line_index, char_index, rainbow_offset
                        )
                        grid[line_y][pos_x] = colored

        stats_data = self.stats.get_stats()
        stats_lines = self.graphics.render_stats(
            stats_data["hunger"], stats_data["mood"], stats_data["energy"]
        )

        stats_height = len(stats_lines) + 1
        for i, line in enumerate(stats_lines):
            line_y = screen_height - stats_height + i
            if 0 <= line_y < screen_height:
                for char_index, char in enumerate(line):
                    if char_index < screen_width:
                        grid[line_y][char_index] = char

        state_indicator = self._get_state_indicator(current_state)
        if state_indicator:
            state_y = screen_height - stats_height - 2
            if 0 <= state_y < screen_height:
                for char_index, char in enumerate(state_indicator):
                    if char_index < screen_width:
                        grid[state_y][char_index] = char

        if self.interaction.is_help_visible():
            help_lines = self.graphics.render_help()
            for i, line in enumerate(help_lines):
                line_y = 2 + i
                if 0 <= line_y < screen_height:
                    for char_index, char in enumerate(line):
                        if char_index < screen_width:
                            grid[line_y][char_index] = char

        message = self.interaction.get_message()
        if message:
            message_line = self.graphics.render_message(
                message, self.interaction.message_duration
            )
            message_y = screen_height - stats_height - 3
            if 0 <= message_y < screen_height:
                for char_index, char in enumerate(message_line):
                    if char_index < screen_width:
                        grid[message_y][char_index] = char

        output = "\n".join("".join(row) for row in grid)
        sys.stdout.write(output)
        sys.stdout.flush()
        return True

    def _get_state_indicator(self, state):
        indicators = {
            CatState.IDLE: self.term.dim + "[IDLE]" + self.term.normal,
            CatState.WALKING: self.term.dim + "[WALKING]" + self.term.normal,
            CatState.EATING: self.term.color(220) + "[EATING 🍽️]" + self.term.normal,
            CatState.SLEEPING: self.term.color(27) + "[SLEEPING 💤]" + self.term.normal,
            CatState.GROOMING: self.term.color(201) + "[GROOMING]" + self.term.normal,
            CatState.PLAYING: self.term.color(46) + "[PLAYING 🎮]" + self.term.normal,
            CatState.STRETCHING: self.term.color(226)
            + "[STRETCHING]"
            + self.term.normal,
            CatState.HUNGRY: self.term.color(196) + "[HUNGRY 😿]" + self.term.normal,
            CatState.HAPPY: self.term.color(226) + "[HAPPY 😺]" + self.term.normal,
            CatState.SAD: self.term.color(27) + "[SAD 😿]" + self.term.normal,
        }
        return indicators.get(state, "")
