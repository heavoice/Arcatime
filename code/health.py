# health.py
class Health:
    def __init__(self, initial_health=100):
        self.health = initial_health
        self.target_health = initial_health

    def update_health(self):
        if self.health > self.target_health:
            self.health -= 0.5
        if self.target_health <= 0:
            self.health = 0

    def take_damage(self, amount):
        self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def is_dead(self):
        return self.health <= 0

    def get_health(self):
        return self.health

    def get_target_health(self):
        return self.target_health
