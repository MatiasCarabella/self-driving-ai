import numpy as np
import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = defaultdict(lambda: np.zeros(action_size))  # Inicializar tabla Q con 0
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate

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