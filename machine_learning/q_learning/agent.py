import sys
import os
import pickle
import numpy as np
import random
from collections import defaultdict
from config import QL_CONFIG

# Add the grandparent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class QLearningAgent:
    def __init__(self, state_size, action_size):
        """Initialize the Q-learning agent with state and action sizes, and load the Q-learning parameters from config."""
        self.state_size = state_size  # The number of possible states
        self.action_size = action_size  # The number of possible actions
        self.q_table = defaultdict(self._default_q_values)  # Initialize Q-table with default values for unseen states
        self.q_table_path = os.path.join("machine_learning", "q_learning", "q_tables", QL_CONFIG["Q_TABLE_FILENAME"])
        self.learning_rate = QL_CONFIG["LEARNING_RATE"]  # Alpha
        self.discount_factor = QL_CONFIG["DISCOUNT_FACTOR"]  # Gamma
        self.exploration_rate = QL_CONFIG["EXPLORATION_RATE"]  # Epsilon
        self.exploration_decay = QL_CONFIG["EXPLORATION_DECAY"]  # Epsilon decay
        self.min_exploration_rate = QL_CONFIG["MIN_EXPLORATION_RATE"]  # Minimum epsilon

    def _default_q_values(self):
        """Return a zero-initialized vector for the Q-table."""
        return np.zeros(self.action_size)

    def get_action(self, state, use_epsilon=True):
        """
        Get an action based on the current state using epsilon-greedy strategy.
        
        Args:
            state: The current state tuple.
            use_epsilon (bool): Whether to use epsilon-greedy exploration. 
                            If False, always choose the best action.
        
        Returns:
            int: The chosen action index.
        """
        if len(state) != self.state_size:
            print(f"Warning: State has {len(state)} variables, but state_size is {self.state_size}")
        
        # Use epsilon-greedy only when use_epsilon is True (learning mode)
        if use_epsilon and random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        else:
            return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value for a state-action pair using the Q-learning formula."""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def decay_exploration(self):
        """Gradually decay the exploration rate (epsilon)."""
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

    def load_q_table(self):
        """Load the Q-table from a file. Returns True if successful, False if the file does not exist."""
        try:
            with open(self.q_table_path, "rb") as f:
                self.q_table = pickle.load(f)
                return True
        except FileNotFoundError:
            return False

    def save_q_table(self):
        """Guarda la Q-table en un archivo."""
        with open(self.q_table_path, "wb") as f:
            pickle.dump(self.q_table, f)