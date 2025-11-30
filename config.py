"""
Configuration file for Self-Driving AI training.

This file contains all hyperparameters and settings for the Q-learning agent,
vehicle physics, reward system, and training sessions.
"""

# Session parameters
SESSION_CONFIG = {
    "TRAINING_MODE": True,    # Toggle between training and evaluation modes
    "NUM_EPISODES": 50,       # Number of episodes to run
    "EPISODE_DURATION": 20,   # Duration of each episode in seconds
    "MANUAL_CONTROL": False,  # Enable manual control with arrow keys
    "HEADLESS": False,        # Run without rendering (much faster training)
    "FRAME_SKIP": 1,          # Process every Nth frame (higher = faster but less smooth)
    "CIRCUIT": "circuit_2"    # Which circuit to use: "circuit_1" or "circuit_2"
}

# Circuit-specific configurations
CIRCUIT_CONFIG = {
    "circuit_1": {
        "window_size": (1200, 400),
        "start_angle": 0,  # Point right
        "q_table": "circuit1_v1.pkl"
    },
    "circuit_2": {
        "window_size": (800, 600),
        "start_angle": 180,  # Point left
        "q_table": "circuit2_v1.pkl"
    }
}

# Q-learning agent parameters
QL_CONFIG = {
    "LEARNING_RATE": 0.1,  # Alpha: learning rate for Q-learning updates
    "DISCOUNT_FACTOR": 0.95,  # Gamma: how much to discount future rewards
    "EXPLORATION_RATE": 1.0,  # Epsilon: initial exploration rate
    "EXPLORATION_DECAY": 0.998,  # How fast to decay epsilon (slower = more exploration)
    "MIN_EXPLORATION_RATE": 0.05,  # Minimum exploration rate (lower = more exploitation)
    "SENSOR_DISCRETIZATION": 10  # Divide sensor distances by this value for state space
}

# Reward parameters
REWARD_CONFIG = {
    "SPEED_WEIGHT": 1.0,  # Weight for speed reward
    "DISTANCE_WEIGHT": 1.0,  # Weight for distance from edges
    "CHECKPOINT_REWARD": 10.0,  # Reward for passing checkpoint
    "FINISH_LINE_REWARD": 100.0,  # Reward for reaching finish line
    "ON_ROAD_REWARD": 0.5,  # Reward for staying on road (per check)
    "PARTIALLY_OFF_PENALTY": -0.5,  # Penalty for being partially off road
    "COMPLETELY_OFF_PENALTY": -1.0,  # Penalty for being completely off road
    "COLLISION_PENALTY": -10.0,  # Penalty for collision (reduced from -25)
    "FORWARD_PROGRESS_WEIGHT": 1.5  # Weight for forward progress reward
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

# General window configuration (auto-set based on circuit)
def get_window_config():
    """Get window configuration based on selected circuit."""
    circuit = SESSION_CONFIG.get("CIRCUIT", "circuit_1")
    width, height = CIRCUIT_CONFIG[circuit]["window_size"]
    return {"WIDTH": width, "HEIGHT": height}

WINDOW_CONFIG = get_window_config()

# Colors used in the environment
COLOR_CONFIG = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "GRAY": (128, 128, 128),
    "YELLOW": (255, 255, 0),
    "FINISH_LINE": (0, 162, 232)  # #00A2E8
}

# Font settings
FONT_CONFIG = {
    "BIG": 36,  # Font size for larger text
    "SMALL": 20  # Font size for smaller text
}
