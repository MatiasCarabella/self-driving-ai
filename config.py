# Session parameters
SESSION_CONFIG = {
    "TRAINING_MODE": True,    # Toggle between training and evaluation modes
    "NUM_EPISODES": 50,       # Number of episodes to run
    "EPISODE_DURATION": 20,   # Duration of each episode in seconds
    "MANUAL_CONTROL": False   # Enable manual control with arrow keys
}

# Q-learning agent parameters
QL_CONFIG = {
    "LEARNING_RATE": 0.1,  # Alpha: learning rate for Q-learning updates
    "DISCOUNT_FACTOR": 0.95,  # Gamma: how much to discount future rewards
    "EXPLORATION_RATE": 1.0,  # Epsilon: initial exploration rate
    "EXPLORATION_DECAY": 0.995,  # How fast to decay epsilon over episodes
    "MIN_EXPLORATION_RATE": 0.05,  # Minimum exploration rate (to always explore a little)
    "Q_TABLE_FILENAME": "v1.pkl"  # Agent 'knowledge' filename
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
    "ROTATION_SPEED": 5,  # Rotation speed
    "COLLISION_TYPE": "CIRCUIT" # "WINDOW" or "CIRCUIT"
}

# General window configuration
WINDOW_CONFIG = {
    "WIDTH": 850,
    "HEIGHT": 650
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
