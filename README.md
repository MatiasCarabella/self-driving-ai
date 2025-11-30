<div id="user-content-toc">
  <ul align="center" style="list-style: none;">
    <summary>
      <h1>Self-Driving AI 🧬</h1>
    </summary>
  </ul>
</div>
<div align="center">
   <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=fff" alt="Python" /></a>
</div>
<h1></h1>

This project is a 2D self-driving car simulation developed in Python using Pygame. It features a Q-learning agent that learns to navigate a circuit by interacting with its environment and optimizing its actions through a reward system. 

<p align="center">
  <img src="https://i.imgur.com/XMouIzG.gif" alt="Self-Driving AI gif">
</p>

## Features
- **Reinforcement Learning**: Implements Q-learning to train an AI agent to navigate a circuit.
- **Sensor System**: The vehicle is equipped with sensors that provide information about its surroundings, allowing for informed decision-making.
- **Visual Feedback**: Real-time visualization of the vehicle's performance, including speed, scores, and sensor values.
- **Logging**: Tracks the performance of the agent across episodes and stores it for further analysis.
- **Dual Mode Operation**: Supports both training and simulation modes through the LEARNING_MODE configuration.

## Setup Instructions

### Prerequisites
To run this project, you'll need Python 3.x along with the required libraries. You can install them using pip:
```bash
pip install -r requirements.txt
```
### Installation

1. Clone the repository:
```bash
git clone https://github.com/matiascarabella/self-driving-ai.git
cd self-driving-ai
```

## Usage

### Standard Training (with visualization)
```bash
python main.py
```

### Fast Training (headless mode - 5-10x faster)
```bash
python train_fast.py
```
Runs without rendering for much faster training. Perfect for overnight training sessions.

### Command Line Options
Override config settings from the command line:
```bash
python main.py --circuit circuit_1 --episodes 100 --headless
python main.py --eval                    # Evaluation mode (no training)
python main.py --manual                  # Manual control with arrow keys
```

### Watch Trained Agent (Evaluation Mode)
```bash
python watch_agent.py
```
Watch your trained agent perform without any learning or logging. The agent uses its learned knowledge deterministically.

## Improving Agent Performance

If your agent gets stuck or isn't learning well:

1. **Increase exploration**: Lower `MIN_EXPLORATION_RATE` in config.py
2. **Train longer**: Use `--episodes 10000` or more
3. **Try different circuits**: Each circuit teaches different skills
4. **Adjust rewards**: Tune `REWARD_CONFIG` values in config.py

## Project Structure
```
self-driving-ai/
├── assets/
│   └── images/
│       ├── circuit_1.png          # Horizontal circuit (1893x493)
│       └── circuit_2.png          # Square circuit (801x601)
├── logs/
│   ├── q_learning/
│   │   ├── circuit1_v1.txt        # Episode scores for circuit 1
│   │   ├── circuit1_v1_metrics.json
│   │   ├── circuit2_v1.txt        # Episode scores for circuit 2
│   │   └── circuit2_v1_metrics.json
│   └── logger.py                  # Logging utilities
├── machine_learning/
│   └── q_learning/
│       ├── q_tables/
│       │   ├── circuit1_v1.pkl    # Learned Q-table for circuit 1
│       │   └── circuit2_v1.pkl    # Learned Q-table for circuit 2
│       └── agent.py               # Q-learning agent implementation
├── models/
│   ├── checkpoint.py              # Checkpoint detection system
│   ├── environment.py             # Game environment and rendering
│   ├── sensor.py                  # Vehicle sensor system
│   └── vehicle.py                 # Vehicle physics and state
├── visualization/
│   └── plot_training.py           # Training progress visualization
├── .gitignore
├── config.py                      # All configuration parameters
├── LICENSE
├── main.py                        # Main entry point with CLI support
├── README.md
├── requirements.txt               # Python dependencies (pinned versions)
├── train_fast.py                  # Headless training wrapper
└── watch_agent.py                 # Evaluation mode wrapper
```

## Configuration
The project includes a `config.py` file where you can adjust various parameters:

### Session Configuration
```python
SESSION_CONFIG = {
    "TRAINING_MODE": True,    # Toggle between training and evaluation modes
    "NUM_EPISODES": 50,       # Number of episodes to run
    "EPISODE_DURATION": 20,   # Duration of each episode in seconds
    "MANUAL_CONTROL": False,  # Enable manual control with arrow keys
    "HEADLESS": False,        # Run without rendering (5-10x faster)
    "FRAME_SKIP": 1,          # Render every Nth frame (higher = faster)
    "CIRCUIT": "circuit_2"    # Which circuit to use: "circuit_1" or "circuit_2"
}
```

### Circuit Configuration
```python
CIRCUIT_CONFIG = {
    "circuit_1": {
        "window_size": (1200, 400),
        "start_angle": 0,      # Point right
        "q_table": "circuit1_v1.pkl"
    },
    "circuit_2": {
        "window_size": (800, 600),
        "start_angle": 180,    # Point left
        "q_table": "circuit2_v1.pkl"
    }
}
```

#### Agent Modes
- **Training Mode** (`TRAINING_MODE = True`):
  - Used for training the agent
  - Agent explores new actions using epsilon-greedy strategy
  - Updates Q-table based on experiences
  - Behavior varies between runs due to exploration

- **Evaluation Mode** (`TRAINING_MODE = False`):
  - Used for testing or demonstrating learned behavior
  - Agent uses learned knowledge deterministically
  - No Q-table updates or exploration
  - Consistent behavior between runs

### Other Configuration Options
- Vehicle settings (dimensions, speed, acceleration)
- Q-learning parameters (learning rate, discount factor, exploration rate)
- Window and display settings

## Log Files
The training results are logged within the `logs/q_learning/` folder:
- `circuit1_v1.txt` / `circuit2_v1.txt`: Records the final score for each episode
- `circuit1_v1_metrics.json` / `circuit2_v1_metrics.json`: Detailed metrics including:
  - Episode number
  - Score and distance traveled
  - Exploration rate (epsilon)
  - Collision status
  - Finish line reached

These logs can be used for performance analysis and progress visualization. Each circuit maintains separate logs.

## Visualizing Progress
Visualize your agent's training progress:

```bash
python visualization/plot_training.py
```

Shows distance traveled over episodes - the primary metric for learning progress. The visualization:
- Displays raw distance data with moving average
- Shows max distance achieved with reference line
- Marks new records with star (★) indicators
- Includes key statistics (episodes, peak, avg last 100)
- Automatically merges multiple training sessions into a continuous timeline

The plot automatically uses the metrics file for the current circuit in config.py.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f8bc373f-3271-44d0-b3a3-5409cae49b68" />
</p>

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- OpenAI for inspiring the use of AI and reinforcement learning concepts.
- Pygame for the graphics library used in this project.
