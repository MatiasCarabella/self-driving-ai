# Session parameters
SESSION_CONFIG = {
    "MANUAL_CONTROL": True,  # Allows controlling the vehicle with the arrow keys
    "NUM_EPISODES": 200,  # Number of episodes
    "EPISODE_DURATION": 15  # Duration of each episode in seconds
}

# General window configuration
WINDOW_CONFIG = {
    "WIDTH": 800,
    "HEIGHT": 600
}

# Vehicle parameters
VEHICLE_CONFIG = {
    "WIDTH": 20,
    "HEIGHT": 10,
    "MAX_SPEED": 6,  # Maximum speed on the track
    "MAX_SPEED_PARTIALLY_OFF": 3,  # Max speed when partially off the track
    "MAX_SPEED_COMPLETELY_OFF": 1,  # Max speed when completely off the track
    "ACCELERATION": 0.2,
    "DESACCELERATION": 0.95,  # Natural deceleration
    "ROTATION_SPEED": 5  # Rotation speed
}

# Q-learning agent parameters
QL_CONFIG = {
    "LEARNING_RATE": 0.1,  # Alpha: learning rate for Q-learning updates
    "DISCOUNT_FACTOR": 0.95,  # Gamma: how much to discount future rewards
    "EXPLORATION_RATE": 1.0,  # Epsilon: initial exploration rate
    "EXPLORATION_DECAY": 0.995,  # How fast to decay epsilon over episodes
    "MIN_EXPLORATION_RATE": 0.1  # Minimum exploration rate (to always explore a little)
}

# Colors used in the environment
COLOR_CONFIG = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "GRAY": (128, 128, 128),
    "YELLOW": (255, 255, 0)
}

# Font settings
FONT_CONFIG = {
    "BIG": 36,  # Font size for larger text
    "SMALL": 20  # Font size for smaller text
}
