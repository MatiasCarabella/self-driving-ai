import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Agrega el directorio padre al path
from grapher import Grapher
from config import QL_CONFIG

def main():
    # You might want to use a dummy log file or adjust this part
    grapher = Grapher()
    target_epsilon = 0.2  # Puedes cambiar este valor según lo que necesites
    # grapher.plot_exploration_decay(QL_CONFIG["EXPLORATION_DECAY"], target_epsilon)
    grapher.plot_exploration_rate_decay(target_epsilon, QL_CONFIG["EXPLORATION_DECAY"])

if __name__ == "__main__":
    main()
