import time
import random
from enum import Enum


class CatState(Enum):
    IDLE = "idle"
    WALKING = "walking"
    EATING = "eating"
    SLEEPING = "sleeping"
    GROOMING = "grooming"
    PLAYING = "playing"
    STRETCHING = "stretching"
    HUNGRY = "hungry"
    HAPPY = "happy"
    SAD = "sad"


class CatStateMachine:
    def __init__(self, config):
        self.config = config
        self.current_state = CatState.IDLE
        self.state_start_time = time.time()
        self.state_duration = 0
        self.min_state_duration = 2.0
        self.transition_timer = 0
        self.transition_duration = 0

        self.behavior_timers = {
            "grooming": 0,
            "stretching": 0,
            "zoomies": 0,
        }
        self.behavior_intervals = {
            "grooming": random.uniform(15, 25),
            "stretching": random.uniform(30, 45),
            "zoomies": random.uniform(20, 40),
        }

    def update(self, dt, stats):
        self._update_behavior_timers(dt)
        self._check_random_behaviors()
        self._update_state_from_stats(stats)
        self._update_state_duration(dt)

    def _update_behavior_timers(self, dt):
        for key in self.behavior_timers:
            self.behavior_timers[key] += dt

    def _check_random_behaviors(self):
        if self._can_change_state():
            for behavior, timer in self.behavior_timers.items():
                if timer >= self.behavior_intervals[behavior]:
                    self._trigger_behavior(behavior)
                    self.behavior_timers[behavior] = 0
                    self.behavior_intervals[behavior] = random.uniform(
                        15 if behavior == "grooming" else 30,
                        25 if behavior == "grooming" else 45,
                    )
                    break

    def _trigger_behavior(self, behavior):
        if behavior == "grooming":
            self.change_state(CatState.GROOMING, duration=3.0)
        elif behavior == "stretching":
            self.change_state(CatState.STRETCHING, duration=2.5)
        elif behavior == "zoomies":
            self.change_state(CatState.PLAYING, duration=4.0)

    def _update_state_from_stats(self, stats):
        if not self._can_change_state():
            return

        hunger = stats.get("hunger", 50)
        mood = stats.get("mood", 50)
        energy = stats.get("energy", 50)

        if energy < 20 and self.current_state != CatState.SLEEPING:
            self.change_state(CatState.SLEEPING, duration=5.0)
        elif hunger < 30 and self.current_state not in [
            CatState.EATING,
            CatState.HUNGRY,
        ]:
            self.change_state(CatState.HUNGRY)
        elif mood < 30 and self.current_state not in [CatState.SAD, CatState.SLEEPING]:
            self.change_state(CatState.SAD)
        elif mood > 80 and self.current_state == CatState.IDLE:
            self.change_state(CatState.HAPPY, duration=3.0)
        elif self.current_state == CatState.SLEEPING and energy > 60:
            self.change_state(CatState.IDLE)

    def _update_state_duration(self, dt):
        if self.state_duration > 0:
            elapsed = time.time() - self.state_start_time
            if elapsed >= self.state_duration:
                self._return_to_default_state()

    def _can_change_state(self):
        if self.state_duration > 0:
            elapsed = time.time() - self.state_start_time
            if elapsed < self.state_duration:
                return False

        elapsed = time.time() - self.state_start_time
        return elapsed >= self.min_state_duration

    def _return_to_default_state(self):
        self.state_duration = 0
        self.current_state = CatState.IDLE
        self.state_start_time = time.time()

    def change_state(self, new_state, duration=0):
        self.current_state = new_state
        self.state_start_time = time.time()
        self.state_duration = duration

    def get_state(self):
        return self.current_state

    def get_animation_speed(self):
        speeds = {
            CatState.IDLE: 0.5,
            CatState.WALKING: 0.4,
            CatState.EATING: 0.3,
            CatState.SLEEPING: 1.0,
            CatState.GROOMING: 0.25,
            CatState.PLAYING: 0.2,
            CatState.STRETCHING: 0.4,
            CatState.HUNGRY: 0.6,
            CatState.HAPPY: 0.35,
            CatState.SAD: 0.8,
        }
        return speeds.get(self.current_state, 0.5)

    def get_movement_speed(self):
        speeds = {
            CatState.IDLE: 0.5,
            CatState.WALKING: 0.7,
            CatState.EATING: 0.0,
            CatState.SLEEPING: 0.0,
            CatState.GROOMING: 0.0,
            CatState.PLAYING: 1.5,
            CatState.STRETCHING: 0.0,
            CatState.HUNGRY: 0.3,
            CatState.HAPPY: 0.6,
            CatState.SAD: 0.2,
        }
        return speeds.get(self.current_state, 0.5)

    def on_feed(self):
        self.change_state(CatState.EATING, duration=3.0)

    def on_play(self):
        self.change_state(CatState.PLAYING, duration=4.0)

    def on_pet(self):
        self.change_state(CatState.HAPPY, duration=2.0)

    def on_sleep(self):
        self.change_state(CatState.SLEEPING, duration=5.0)
