# Cooldown duration for the checkpoint in seconds
CHECKPOINT_COOLDOWN = 5

class Checkpoint:
    def __init__(self, position):
        self.position = position
        self.last_crossed = 0  # Time when the checkpoint was last crossed

    def is_active(self, current_time):
        """Check if the checkpoint is active based on the current time."""
        return current_time - self.last_crossed >= CHECKPOINT_COOLDOWN
