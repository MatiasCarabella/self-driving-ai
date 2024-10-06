# Parámetros de la sesión
SESSION_CONFIG = {
    "MANUAL_CONTROL": True, # Permite controlar el vehículo con las flechas del teclado
    "NUM_EPISODES": 200, # Cantidad de episodios
    "EPISODE_DURATION": 15 # Duración del episodio en segundos
}

# Configuración general de la ventana
WINDOW_CONFIG = {
    "WIDTH": 800,
    "HEIGHT": 600
}

# Parámetros del vehículo
VEHICLE_CONFIG = {
    "WIDTH": 20,
    "HEIGHT": 10,
    "MAX_SPEED": 6,
    "MAX_SPEED_PARTIALLY_OFF": 3,
    "MAX_SPEED_COMPLETELY_OFF": 1,
    "ACCELERATION": 0.2,
    "DESACCELERATION": 0.95,
    "ROTATION_SPEED": 5
}


# Parámetros del agente Q-learning
QL_CONFIG = {
    "LEARNING_RATE": 0.1,
    "DISCOUNT_FACTOR": 0.95,
    "EXPLORATION_RATE": 1.0,
    "EXPLORATION_DECAY": 0.995,
    "MIN_EXPLORATION_RATE": 0.01
}

# Colores
COLOR_CONFIG = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "GRAY": (128, 128, 128),
    "YELLOW": (255, 255, 0)
}
 
FONT_CONFIG = {
    "BIG": 36,  # Tamaño de la fuente grande
    "SMALL": 20  # Tamaño de la fuente chica
}