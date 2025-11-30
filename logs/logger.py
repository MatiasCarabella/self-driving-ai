import os
import json

class Logger:
    def __init__(self, log_file="training_log.txt"):
        """
        Initialize the Logger with a specified log file.

        Args:
            log_file (str): Name of the log file. Defaults to "training_log.txt".
        """
        self.log_directory = "logs"  # Define the base directory for logs
        self.log_file = os.path.join(self.log_directory, log_file)  # Construct the full path to the log file
        
        # Create a detailed metrics file
        base_name = os.path.splitext(log_file)[0]
        self.metrics_file = os.path.join(self.log_directory, f"{base_name}_metrics.json")

        # Ensure the log directory exists
        os.makedirs(self.log_directory, exist_ok=True)

    def get_last_score(self):
        """
        Read the last score from the log file.

        Returns:
            float: The last logged score. Returns 0.0 if the file is empty or doesn't exist.
        """
        try:
            with open(self.log_file, "r") as log_file:
                lines = log_file.readlines()
                if lines:
                    last_line = lines[-1]  # Get the last line
                    last_score = float(last_line.strip())  # Convert the score to float
                    return last_score
        except FileNotFoundError:
            return 0.0  # If the file doesn't exist, return 0.0
        return 0.0  # If the file is empty, return 0.0

    def log_score(self, score):
        """
        Log the given score to the log file.

        Args:
            score (float): The score to be logged.
        """
        with open(self.log_file, "a") as log_file:
            log_file.write(f"{score}\n")  # Write the score followed by a newline
    
    def log_metrics(self, episode, score, exploration_rate, collided, distance_traveled):
        """
        Log detailed metrics for an episode.

        Args:
            episode (int): Episode number
            score (float): Final score
            exploration_rate (float): Current exploration rate
            collided (bool): Whether the vehicle collided
            distance_traveled (float): Total distance traveled
        """
        metrics = {
            "episode": episode,
            "score": score,
            "exploration_rate": exploration_rate,
            "collided": collided,
            "distance_traveled": distance_traveled
        }
        
        # Append to metrics file
        with open(self.metrics_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")