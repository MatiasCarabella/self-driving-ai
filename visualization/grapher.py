import matplotlib.pyplot as plt
import numpy as np

class Grapher:
    def __init__(self, log_file=None):
        """
        Initialize the Grapher with the path to the log file.
        
        Args:
            log_file (str): Path to the log file containing episode scores.
        """
        self.log_file = log_file
        self.episodes = []  # List to store episode numbers
        self.scores = []    # List to store scores

    def read_log(self):
        """
        Read the log file and extract episode numbers and scores.
        Each line in the log file is expected to contain a single score.
        """
        if self.log_file:
            with open(self.log_file, "r") as f:
                for line in f:
                    score = float(line.strip())
                    self.scores.append(score)
                    self.episodes.append(len(self.scores))  # Episode number is the index in the list

    def plot_progress(self):
        """
        Plot the agent's progress (scores) over episodes with improved readability.
        This method creates a line plot of scores vs. episode numbers, including a moving average.
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot raw data with reduced opacity
        ax.plot(self.episodes, self.scores, color='lightblue', alpha=0.3, label='Raw scores')

        # Calculate and plot moving average
        window_size = min(100, len(self.scores) // 20)  # Adjust window size based on data length
        moving_avg = np.convolve(self.scores, np.ones(window_size)/window_size, mode='valid')
        ax.plot(self.episodes[window_size-1:], moving_avg, color='blue', label=f'Moving average (window: {window_size})')

        # Add min and max score lines
        min_score = min(self.scores)
        max_score = max(self.scores)
        ax.axhline(min_score, color='red', linestyle='--', label=f'Min score: {min_score:.2f}')
        ax.axhline(max_score, color='green', linestyle='--', label=f'Max score: {max_score:.2f}')
        # ax.axhline(0, color='gray', linestyle=':', label='Score 0')

        # Improve labels
        ax.set_xlabel("Episode Number", fontsize=12)
        ax.set_ylabel("Score", fontsize=12)

        # Adjust x-axis ticks and remove whitespace
        num_ticks = 10
        step = max(1, len(self.episodes) // num_ticks)
        ax.set_xticks(range(0, len(self.episodes) + 1, step))
        ax.set_xlim(0, len(self.episodes))

        # Add grid for better readability
        ax.grid(True, linestyle=':', alpha=0.6)

        # Add legend
        ax.legend(loc='upper left', fontsize=10)

        # Add text box with statistics
        stats_text = f"Total Episodes: {len(self.episodes)}\n"
        stats_text += f"Avg Score (last 100): {np.mean(self.scores[-100:]):.2f}"
        ax.text(0.02, 0.02, stats_text, transform=ax.transAxes, 
                bbox=dict(facecolor='white', alpha=0.8), fontsize=10, 
                verticalalignment='bottom')

        # Remove title from plot and set as figure name
        fig.canvas.manager.set_window_title('Agent Progress: Score over Episodes')

        plt.tight_layout()
        plt.show()

    def plot_exploration_rate_decay(self, target_epsilon, exploration_decay, initial_rate=1.0, extension_factor=1.2):
        """
        Plot the exploration rate decay over iterations.
        
        Args:
            target_epsilon (float): The target exploration rate.
            exploration_decay (float): The decay rate for the exploration.
            initial_rate (float): The initial exploration rate (default: 1.0).
            extension_factor (float): Factor to extend the plot beyond the target (default: 1.2).
        """
        # Read log file if not already done
        if not self.episodes:
            self.read_log()
        
        total_episodes = len(self.episodes)

        def calculate_iterations(target_rate):
            """Calculate the number of iterations to reach the target rate."""
            if target_rate >= initial_rate:
                return 0
            if target_rate <= 0:
                return float('inf')
            return np.ceil(np.log(target_rate / initial_rate) / np.log(exploration_decay))

        # Calculate iterations to target and extend
        iterations_to_target = int(calculate_iterations(target_epsilon))
        max_iterations = max(int(iterations_to_target * extension_factor), total_episodes)
        
        iterations = np.arange(max_iterations + 1)
        exploration_rates = initial_rate * (exploration_decay ** iterations)

        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(iterations, exploration_rates, label='Exploration Rate')
        plt.axhline(y=target_epsilon, color='r', linestyle='--', label='Target Epsilon')
        
        # Mark the total number of episodes from the log
        plt.axvline(x=total_episodes, color='g', linestyle='--', label='Total Episodes')
        
        plt.title(f'Exploration Rate Decay (Target: {target_epsilon}, Decay: {exploration_decay})')
        plt.xlabel('Number of Iterations')
        plt.ylabel('Exploration Rate')
        plt.legend()
        plt.grid(True)
        
        plt.yscale('linear')
        plt.ylim(bottom=0, top=1.0)
        plt.xlim(left=0, right=max_iterations)
        
        # Set Y-axis ticks
        y_ticks = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        plt.yticks(y_ticks, [f'{tick:.1f}' for tick in y_ticks])
        
        # Adjust X-axis ticks
        x_ticks = list(range(0, max_iterations + 1, max(1, max_iterations // 10)))
        plt.xticks(x_ticks)
        
        # Add text with iteration count and total episodes
        plt.text(0.05, 0.95, f'Iterations to reach target: {iterations_to_target}\nTotal episodes: {total_episodes}', 
                 transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8),
                 verticalalignment='top')
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def round_to_nearest_five(value):
        """
        Round the given value to the nearest multiple of 5.
        
        Args:
            value (float): The value to round.
        
        Returns:
            int: The rounded value.
        """
        return int(np.round(value / 5) * 5)