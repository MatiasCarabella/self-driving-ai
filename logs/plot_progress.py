import os
from grapher import Grapher

def main():
    # Get the absolute path of the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(current_directory, "training_log.txt")
    
    # Create a Grapher instance and plot progress
    grapher = Grapher(log_file)
    grapher.read_log()  # Read log data
    grapher.plot_progress()  # Plot the data

if __name__ == "__main__":
    main()
