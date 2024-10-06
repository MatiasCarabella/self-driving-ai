# Duración de la inactividad del checkpoint en segundos
CHECKPOINT_COOLDOWN = 5

class Checkpoint:
    def __init__(self, position):
        self.position = position
        self.last_crossed = 0  # Tiempo en que se cruzó por última vez

    def is_active(self, current_time):
        return current_time - self.last_crossed >= CHECKPOINT_COOLDOWN