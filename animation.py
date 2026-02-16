import time
import random
from blessed import Terminal


class Animation:
    def __init__(self, terminal: Terminal, config: dict):
        self.term = terminal
        self.config = config
        self.animation_speed = config["pet"]["animation_speed"]
        self.movement_speed = config["pet"]["movement_speed"]
        self.screen_wrap = config["pet"]["screen_wrap"]

        self.frame_index = 0
        self.rainbow_offset = 0
        self.last_frame_time = time.time()

        self.cat_x = 35
        self.cat_y = 8
        self.direction = 1

    def update(self, dt):
        self._update_frame(dt)
        self._update_rainbow(dt)
        self._update_position(dt)

    def _update_frame(self, dt):
        self.last_frame_time += dt
        if self.last_frame_time >= self.animation_speed:
            self.frame_index += 1
            self.last_frame_time = 0

    def _update_rainbow(self, dt):
        self.rainbow_offset = int(time.time() * 3) % 100

    def _update_position(self, dt):
        distance = self.movement_speed * dt
        self.cat_x += distance * self.direction

        screen_width = self.term.width
        cat_width = 15

        if self.screen_wrap:
            if self.cat_x > screen_width:
                self.cat_x = -cat_width
            elif self.cat_x < -cat_width:
                self.cat_x = screen_width
        else:
            if self.cat_x > screen_width - cat_width or self.cat_x < 0:
                self.direction *= -1
                self.cat_x += distance * self.direction * 2

    def get_frame_index(self):
        return self.frame_index

    def get_rainbow_offset(self):
        return self.rainbow_offset

    def get_position(self):
        return int(self.cat_x), self.cat_y

    def set_position(self, x, y):
        self.cat_x = x
        self.cat_y = y
