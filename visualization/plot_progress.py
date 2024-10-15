import os
from grapher import Grapher

def main():
    # Get the absolute path of the "logs" directory
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(parent_directory, "logs/q_learning/v1.txt")
    
    # Create a Grapher instance and plot progress
    grapher = Grapher(log_file)
    grapher.read_log()  # Read log data
    grapher.plot_progress()  # Plot the data

if __name__ == "__main__":
    main()
