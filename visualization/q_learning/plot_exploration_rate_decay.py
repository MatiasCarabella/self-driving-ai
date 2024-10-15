import sys
import os

# Add the grandparent directory to the path (for config.py)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# Add the parent directory (for grapher.py)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grapher import Grapher
from config import QL_CONFIG

def main():
    # Get the absolute path of the "logs" directory
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_file = os.path.join(grandparent_directory, "logs/q_learning/v1.txt")

    # Initialize the grapher with the correct log file
    grapher = Grapher(log_file)
    target_epsilon = QL_CONFIG["MIN_EXPLORATION_RATE"]
    grapher.plot_exploration_rate_decay(target_epsilon, QL_CONFIG["EXPLORATION_DECAY"])

if __name__ == "__main__":
    main()
