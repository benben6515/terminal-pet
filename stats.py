import time


class Stats:
    def __init__(self, config: dict):
        self.config = config
        stats_config = config["stats"]

        self.max_value = stats_config["max_value"]
        self.min_value = stats_config["min_value"]

        self.hunger = stats_config["initial_hunger"]
        self.mood = stats_config["initial_mood"]
        self.energy = stats_config["initial_energy"]

        self.last_update = time.time()

    def update(self, dt):
        decay_rates = self.config["stats"]

        self.hunger = max(
            self.min_value, self.hunger - decay_rates["hunger_decay"] * dt
        )
        self.mood = max(self.min_value, self.mood - decay_rates["mood_decay"] * dt)
        self.energy = max(
            self.min_value, self.energy - decay_rates["energy_decay"] * dt
        )

        if self.hunger < 20:
            self.mood -= decay_rates["mood_decay"] * dt * 0.5

    def feed(self, amount=20):
        self.hunger = min(self.max_value, self.hunger + amount)
        return "Nyan eats a delicious treat! 😋"

    def play(self, amount=15):
        self.mood = min(self.max_value, self.mood + amount)
        self.energy = max(self.min_value, self.energy - amount * 0.5)
        self.hunger = max(self.min_value, self.hunger - 5)
        return "Nyan plays happily! 🎉"

    def pet(self, amount=10):
        self.mood = min(self.max_value, self.mood + amount)
        return "Nyan loves being petted! 💕"

    def sleep(self, amount=30):
        self.energy = min(self.max_value, self.energy + amount)
        self.hunger = max(self.min_value, self.hunger - 10)
        return "Nyan is sleeping... 😴"

    def get_stats(self):
        return {
            "hunger": int(self.hunger),
            "mood": int(self.mood),
            "energy": int(self.energy),
        }

    def get_status(self):
        stats = self.get_stats()
        if stats["energy"] < 20:
            return "exhausted"
        elif stats["hunger"] < 20:
            return "hungry"
        elif stats["mood"] < 20:
            return "sad"
        elif stats["mood"] > 80 and stats["energy"] > 60:
            return "happy"
        else:
            return "normal"
