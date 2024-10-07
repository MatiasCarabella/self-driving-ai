import os
import matplotlib.pyplot as plt
import numpy as np

class Grapher:
    def __init__(self, log_file):
        """Initialize the Grapher with the path to the log file."""
        self.log_file = log_file
        self.episodes = []  # List to store episode numbers
        self.scores = []    # List to store scores

    def read_log(self):
        """Read the log file and extract episode numbers and scores."""
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

        # Dynamically determine the number of ticks
        num_ticks_x = min(20, len(self.episodes))  # Number of ticks on the X axis (max 20)
        num_ticks_y = 15  # Fixed number of ticks on the Y axis

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
