from blessed import Terminal
import time


class Interaction:
    def __init__(self, terminal: Terminal, config: dict):
        self.term = terminal
        self.config = config
        self.controls = config["controls"]

        self.message = ""
        self.message_time = 0
        self.message_duration = 2.0
        self.show_help = False

    def handle_key(self, key, pet_stats):
        if key is None:
            return None

        key_lower = str(key).lower()

        if key_lower == self.controls["feed_key"]:
            self._show_message(pet_stats.feed())
            return "feed"

        elif key_lower == self.controls["play_key"]:
            self._show_message(pet_stats.play())
            return "play"

        elif key_lower == self.controls["pet_key"]:
            self._show_message(pet_stats.pet())
            return "pet"

        elif key_lower == self.controls["sleep_key"]:
            self._show_message(pet_stats.sleep())
            return "sleep"

        elif key_lower == self.controls["help_key"]:
            self.show_help = not self.show_help
            self._show_message("Help toggled" if self.show_help else "Help hidden")
            return "help"

        elif key_lower == self.controls["quit_key"]:
            return "quit"

        return None

    def _show_message(self, message):
        self.message = message
        self.message_time = time.time()

    def update(self, dt):
        if time.time() - self.message_time > self.message_duration:
            self.message = ""

    def get_message(self):
        return self.message

    def is_help_visible(self):
        return self.show_help

    def get_controls(self):
        return self.controls
