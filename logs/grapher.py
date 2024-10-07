import os
import matplotlib.pyplot as plt
import numpy as np

class Grapher:
    def __init__(self, log_file):
        """Initialize the Grapher with the log file path."""
        self.log_file = log_file
        self.episodes = []
        self.scores = []

    def read_log(self):
        """Read the log file and extract episode numbers and scores."""
        with open(self.log_file, "r") as f:
            for line in f:
                episode, score = line.strip().split(", ")
                self.episodes.append(int(episode))
                self.scores.append(float(score))

    def plot_progress(self):
        """Plot the agent's progress over the episodes."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.episodes, self.scores, marker='o', linestyle='-', color='b')
        plt.title("Agent Progress Over Episodes")
        plt.xlabel("Episode Number")
        plt.ylabel("Final Score")
        plt.axhline(0, color='red', linestyle='--', label='Score 0')  # Horizontal line at 0
        plt.legend()
        plt.grid()

        # Desired number of ticks
        num_ticks_x = 20  # Number of ticks on the X axis
        num_ticks_y = 15  # Number of ticks on the Y axis

        # Calculate tick spacing for the X axis
        x_min = round_to_nearest_five(min(self.episodes))  # Round the minimum to the nearest multiple of 5
        x_max = round_to_nearest_five(max(self.episodes))  # Round the maximum to the nearest multiple of 5
        tick_spacing_x = round_to_nearest_five((x_max - x_min) / num_ticks_x)  # Round to the nearest multiple of 5
        x_ticks = range(x_min, x_max + 1, tick_spacing_x)  # Generate ticks
        plt.xticks(x_ticks)  # Apply ticks to the X axis

        # Calculate tick spacing for the Y axis
        y_min = round_to_nearest_five(min(self.scores))  # Round the minimum to the nearest multiple of 5
        y_max = round_to_nearest_five(max(self.scores))  # Round the maximum to the nearest multiple of 5
        tick_spacing_y = round_to_nearest_five((y_max - y_min) / num_ticks_y)  # Round to the nearest multiple of 5
        y_ticks = np.arange(y_min, y_max + tick_spacing_y, tick_spacing_y)  # Generate ticks
        plt.yticks(y_ticks)  # Apply ticks to the Y axis

        plt.show()

def round_to_nearest_five(value):
    """Round the value to the nearest multiple of 5."""
    return int(np.round(value / 5) * 5)

def main():
    # Get the absolute path of the current directory where the .py file is running
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(current_directory, "training_log.txt")
    
    # Create a Grapher instance and plot progress
    grapher = Grapher(log_file)
    grapher.read_log()  # Read log data
    grapher.plot_progress()  # Plot the data

if __name__ == "__main__":
    main()
