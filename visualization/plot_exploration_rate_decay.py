import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grapher import Grapher
from config import QL_CONFIG

def main():
    # Get the absolute path of the "logs" directory
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(parent_directory, "logs/training_log.txt")

    # Initialize the grapher with the correct log file
    grapher = Grapher(log_file)
    target_epsilon = 0.2
    grapher.plot_exploration_rate_decay(target_epsilon, QL_CONFIG["EXPLORATION_DECAY"])

if __name__ == "__main__":
    main()
