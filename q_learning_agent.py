import numpy as np
import random
from collections import defaultdict
from config import QL_CONFIG

class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = defaultdict(self._default_q_values)
        self.learning_rate = QL_CONFIG["LEARNING_RATE"]
        self.discount_factor = QL_CONFIG["DISCOUNT_FACTOR"]
        self.exploration_rate = QL_CONFIG["EXPLORATION_RATE"]
        self.exploration_decay = QL_CONFIG["EXPLORATION_DECAY"]
        self.min_exploration_rate = QL_CONFIG["MIN_EXPLORATION_RATE"]

    def _default_q_values(self):
        """Función que devuelve un vector de ceros para la tabla Q."""
        return np.zeros(self.action_size)

    def get_action(self, state):
        """Elige una acción basado en la política epsilon-greedy."""
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)  # Acción aleatoria (exploración)
        else:
            return np.argmax(self.q_table[state])  # Mejor acción conocida (explotación)

    def update_q_value(self, state, action, reward, next_state):
        """Actualiza la tabla Q usando la fórmula de Q-learning."""
        best_next_action = np.argmax(self.q_table[next_state])  # Mejor acción en el próximo estado
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def decay_exploration(self):
        """Reduce gradualmente la tasa de exploración."""
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)