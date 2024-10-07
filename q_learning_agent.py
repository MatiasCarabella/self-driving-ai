import numpy as np
import random
from collections import defaultdict
from config import QL_CONFIG

class QLearningAgent:
    def __init__(self, state_size, action_size):
        """Initialize the Q-learning agent with state and action sizes, and load the Q-learning parameters from config."""
        self.state_size = state_size  # The number of possible states
        self.action_size = action_size  # The number of possible actions
        self.q_table = defaultdict(self._default_q_values)  # Initialize Q-table with default values for unseen states
        self.learning_rate = QL_CONFIG["LEARNING_RATE"]  # Alpha: how much to update the Q-values on each step
        self.discount_factor = QL_CONFIG["DISCOUNT_FACTOR"]  # Gamma: how much future rewards are considered
        self.exploration_rate = QL_CONFIG["EXPLORATION_RATE"]  # Epsilon: the initial exploration rate for epsilon-greedy
        self.exploration_decay = QL_CONFIG["EXPLORATION_DECAY"]  # How fast epsilon decays after each episode
        self.min_exploration_rate = QL_CONFIG["MIN_EXPLORATION_RATE"]  # The minimum epsilon to avoid stopping exploration completely

    def _default_q_values(self):
        """Return a zero-initialized vector for the Q-table. Called when a new state is encountered."""
        return np.zeros(self.action_size)  # Start with all Q-values for each action in this state as 0

    def get_action(self, state):
        """
        Select an action using epsilon-greedy policy.
        With probability `exploration_rate`, a random action is chosen (exploration).
        Otherwise, the action with the highest Q-value is chosen (exploitation).
        """
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)  # Choose a random action (exploration)
        else:
            return np.argmax(self.q_table[state])  # Choose the best action based on the current Q-table (exploitation)

    def update_q_value(self, state, action, reward, next_state):
        """
        Update the Q-value for a state-action pair using the Q-learning formula:
        Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
        where:
        - alpha is the learning rate
        - gamma is the discount factor
        - max(Q(s', a')) is the maximum Q-value of the next state
        """
        # Get the best action for the next state
        best_next_action = np.argmax(self.q_table[next_state])

        # Calculate the target value: immediate reward + discounted future reward
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]

        # Calculate the temporal difference error: how far off the current Q-value is from the target
        td_error = td_target - self.q_table[state][action]

        # Update the Q-value using the learning rate
        self.q_table[state][action] += self.learning_rate * td_error

    def decay_exploration(self):
        """
        Gradually decay the exploration rate (epsilon) to reduce exploration over time.
        This makes the agent explore less and exploit more as training progresses.
        """
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
