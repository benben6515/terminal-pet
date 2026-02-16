import time
import random
from blessed import Terminal


class Animation:
    def __init__(self, terminal: Terminal, config: dict):
        self.term = terminal
        self.config = config
        self.base_animation_speed = config["pet"]["animation_speed"]
        self.base_movement_speed = config["pet"]["movement_speed"]
        self.screen_wrap = config["pet"]["screen_wrap"]

        self.frame_index = 0
        self.rainbow_offset = 0
        self.last_frame_time = time.time()
        self.frame_accumulator = 0

        self.cat_x = 35
        self.cat_y = 8
        self.direction = 1

        self.current_animation_speed = self.base_animation_speed
        self.current_movement_speed = self.base_movement_speed

        self.pause_timer = 0
        self.is_paused = False

        self.zoomie_direction = 1
        self.zoomie_active = False

    def update(self, dt, cat_state=None):
        if cat_state:
            self._update_speeds_from_state(cat_state)
            self._handle_state_movement(cat_state)

        if self.is_paused:
            self.pause_timer -= dt
            if self.pause_timer <= 0:
                self.is_paused = False
            return

        self._update_frame(dt)
        self._update_rainbow(dt)
        self._update_position(dt)

    def _update_speeds_from_state(self, cat_state):
        from cat_state import CatState

        state_speeds = {
            CatState.IDLE: (0.5, 0.5),
            CatState.WALKING: (0.4, 0.7),
            CatState.EATING: (0.3, 0.0),
            CatState.SLEEPING: (1.0, 0.0),
            CatState.GROOMING: (0.25, 0.0),
            CatState.PLAYING: (0.2, 1.5),
            CatState.STRETCHING: (0.4, 0.0),
            CatState.HUNGRY: (0.6, 0.3),
            CatState.HAPPY: (0.35, 0.6),
            CatState.SAD: (0.8, 0.2),
        }

        speeds = state_speeds.get(
            cat_state, (self.base_animation_speed, self.base_movement_speed)
        )
        self.current_animation_speed = speeds[0]
        self.current_movement_speed = speeds[1]

    def _handle_state_movement(self, cat_state):
        from cat_state import CatState

        if cat_state == CatState.SLEEPING:
            if not self.is_paused:
                self.pause()
        elif cat_state == CatState.GROOMING:
            if not self.is_paused:
                self.pause()
        elif cat_state == CatState.EATING:
            pass
        elif cat_state == CatState.PLAYING:
            self.zoomie_active = True
            self.is_paused = False
        else:
            self.is_paused = False
            self.zoomie_active = False

    def pause(self, duration=None):
        self.is_paused = True
        self.pause_timer = duration if duration else float("inf")

    def resume(self):
        self.is_paused = False
        self.pause_timer = 0

    def _update_frame(self, dt):
        self.frame_accumulator += dt
        if self.frame_accumulator >= self.current_animation_speed:
            self.frame_index += 1
            self.frame_accumulator = 0

    def _update_rainbow(self, dt):
        self.rainbow_offset = int(time.time() * 3) % 100

    def _update_position(self, dt):
        if self.current_movement_speed == 0:
            return

        speed = self.current_movement_speed
        if self.zoomie_active:
            speed *= 2
            if random.random() < 0.02:
                self.direction *= -1

        distance = speed * dt
        self.cat_x += distance * self.direction

        screen_width = self.term.width
        cat_width = 20

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

    def get_movement_speed(self):
        return self.current_movement_speed
