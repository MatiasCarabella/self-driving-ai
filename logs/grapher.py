import matplotlib.pyplot as plt
import numpy as np

class Grapher:
    def __init__(self, log_file=None):
        """Initialize the Grapher with the path to the log file."""
        self.log_file = log_file
        self.episodes = []  # List to store episode numbers
        self.scores = []    # List to store scores

    def read_log(self):
        """Read the log file and extract episode numbers and scores."""
        if self.log_file:
            with open(self.log_file, "r") as f:
                for line in f:
                    # Each line contains a score; append the score to the scores list
                    score = float(line.strip())
                    self.scores.append(score)
                    self.episodes.append(len(self.scores))  # Episode number is the index in the list

    def plot_progress(self):
        """Plot the agent's progress over the episodes."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.episodes, self.scores, marker='o', linestyle='-', color='b')
        plt.title("Agent progress (Score) over Episode number")
        plt.xlabel("Episode Number")
        plt.ylabel("Final Score")
        plt.axhline(0, color='red', linestyle='--', label='Score 0')  # Horizontal line at 0
        plt.legend()
        plt.grid()

        # Dynamic ticks for X axis
        num_data_points = len(self.episodes)
        num_ticks_x = min(15, max(5, num_data_points // 10))
        x_min, x_max = self.round_to_nearest_five(min(self.episodes)), self.round_to_nearest_five(max(self.episodes))
        tick_spacing_x = max(1, self.round_to_nearest_five((x_max - x_min) / num_ticks_x))
        x_ticks = range(x_min, x_max + 1, tick_spacing_x)
        plt.xticks(x_ticks)

        # Dynamic ticks for Y axis
        y_min, y_max = self.round_to_nearest_five(min(self.scores)), self.round_to_nearest_five(max(self.scores))
        if y_min == y_max:
            y_min -= 5
            y_max += 5
        num_ticks_y = min(10, max(5, (y_max - y_min) // 10))
        tick_spacing_y = max(1, self.round_to_nearest_five((y_max - y_min) / num_ticks_y))
        y_ticks = np.arange(y_min, y_max + tick_spacing_y, tick_spacing_y)
        plt.yticks(y_ticks)

        plt.show()

    def plot_exploration_rate_decay(self, target_epsilon, exploration_decay, initial_rate=1.0, extension_factor=1.2):
        def calculate_iterations(target_rate):
            if target_rate >= initial_rate:
                return 0
            if target_rate <= 0:
                return float('inf')
            return np.ceil(np.log(target_rate / initial_rate) / np.log(exploration_decay))

        # Calcular iteraciones hasta el target y extender
        iterations_to_target = int(calculate_iterations(target_epsilon))
        max_iterations = int(iterations_to_target * extension_factor)
        
        iterations = np.arange(max_iterations + 1)
        exploration_rates = initial_rate * (exploration_decay ** iterations)

        plt.figure(figsize=(12, 6))
        plt.plot(iterations, exploration_rates, label='Exploration Rate')
        plt.axhline(y=target_epsilon, color='r', linestyle='--', label='Target Epsilon')
        
        plt.title(f'Decaimiento del Exploration Rate (Target: {target_epsilon}, Decay: {exploration_decay})')
        plt.xlabel('Número de Iteraciones')
        plt.ylabel('Exploration Rate')
        plt.legend()
        plt.grid(True)
        
        plt.yscale('linear')
        plt.ylim(bottom=0, top=1.0)
        plt.xlim(left=0, right=max_iterations)  # Ajuste para que el eje X comience en 0
        
        y_ticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        plt.yticks(y_ticks, [f'{tick:.1f}' for tick in y_ticks])
        
        # Ajustar ticks del eje X
        x_ticks = list(range(0, max_iterations + 1, max(1, iterations_to_target // 5)))
        plt.xticks(x_ticks)
        
        # Añadir texto con el número de iteraciones
        plt.text(0.05, 0.95, f'Iteraciones para alcanzar el objetivo: {iterations_to_target}', 
                 transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8),
                 verticalalignment='top')
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def round_to_nearest_five(value):
        """Round the value to the nearest multiple of 5."""
        return int(np.round(value / 5) * 5)
