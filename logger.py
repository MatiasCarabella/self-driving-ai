class Logger:
    def __init__(self, log_file="logs/training_log.txt"):
        self.log_file = log_file

    def get_last_score(self):
        """Reads the last score from the log file."""
        try:
            with open(self.log_file, "r") as log_file:
                lines = log_file.readlines()
                if lines:
                    last_line = lines[-1]  # Get the last line
                    last_score = float(last_line.split(', ')[1])  # Read the score
                    return last_score
        except FileNotFoundError:
            return 0.0  # If the file doesn't exist, return 0.0

    def log_score(self, score):
        """Logs the score in the log file."""
        with open(self.log_file, "a") as log_file:
            log_file.write(f"{score}\n")  # Simple format: just the score
