class Logger:
    def __init__(self, log_file="logs/training_log.txt"):
        self.log_file = log_file

    def get_last_episode(self):
        """Reads the last episode number from the log file."""
        try:
            with open(self.log_file, "r") as log_file:
                lines = log_file.readlines()
                if lines:
                    last_line = lines[-1]  # Get the last line
                    last_episode = int(last_line.split(',')[0])  # Read the episode number
                    return last_episode
        except FileNotFoundError:
            return 0  # If the file doesn't exist, return 0

    def log_episode(self, episode_number, score):
        """Logs the episode number and score in the log file."""
        with open(self.log_file, "a") as log_file:
            log_file.write(f"{episode_number}, {score}\n")  # Simple format
