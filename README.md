<div id="user-content-toc">
  <ul align="center" style="list-style: none;">
    <summary>
      <h1>2D Self-Driving Car Simulation</h1>
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

### Watch Trained Agent (Evaluation Mode)
```bash
python watch_agent.py
```
Watch your trained agent perform without any learning or logging. The agent uses its learned knowledge deterministically.

### Manual Control
Set `MANUAL_CONTROL = True` in config.py to drive the car yourself with arrow keys.

## Improving Agent Performance

If your agent gets stuck (e.g., only turns right, can't handle sharp corners):

```bash
python retrain_exploration.py
```

This boosts exploration to help the agent discover new strategies. See `TRAINING_TIPS.md` for detailed strategies on improving learning.

## Project Structure
```
self-driving-ai/
├── assets/
│   └── images/
│       ├── circuit_1.png
│       ├── circuit_2.png
│       └── circuit_3.png
├── logs/
│   ├── q_learning/
│   │   ├── .gitkeep
│   │   └── v1.txt
│   └── logger.py
├── machine_learning/
│   └── q_learning/
│       ├── q_tables/
│       │   ├── .gitkeep
│       │   └── v1.pkl
│       └── agent.py
├── models/
│   ├── checkpoint.py
│   ├── environment.py
│   ├── sensor.py
│   └── vehicle.py
├── visualization/
│   └── plot_training.py
├── .gitignore
├── config.py
├── LICENSE
├── main.py
└── README.md
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
    "FRAME_SKIP": 1           # Render every Nth frame (higher = faster)
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
The training results are logged within the `logs` folder:
- `v2.txt`: Records the final score for each episode
- `v2_metrics.json`: Detailed metrics including score, exploration rate, collision status, and distance traveled

These logs can be used for performance analysis and progress visualization.

## Visualizing Progress
Visualize your agent's training progress:

```bash
python visualization/plot_training.py
```

Shows distance traveled over episodes - the primary metric for learning progress. The visualization:
- Displays raw distance data with moving average
- Shows max distance achieved
- Includes comprehensive statistics (last 100, last 1000, overall averages)
- Automatically merges multiple training sessions into a continuous timeline

For detailed single-metric views:
```bash
python visualization/plot_training.py distance  # Same as default
python visualization/plot_training.py score     # Score-focused view
```

<p align="center">
  <img src="https://github.com/user-attachments/assets/f8bc373f-3271-44d0-b3a3-5409cae49b68" />
</p>

## Training Speed Optimization

### Performance Comparison (100 episodes)
| Mode | Time | Speedup |
|------|------|---------|
| Standard (with rendering) | ~35 minutes | 1x |
| Headless mode | ~4-6 minutes | 5-10x |
| Frame skip (skip=3) | ~12 minutes | 3x |

### Recommendations
- **Development/Testing**: Use standard mode to see what's happening
- **Large-Scale Training**: Use headless mode (`train_fast.py`)
- **Debugging**: Use frame skip to balance speed and visibility

## Recent Improvements (v2)

### Enhanced State Representation
- Added vehicle angle to state space for better directional awareness
- Improved state discretization for more effective learning

### Improved Reward System
- Configurable reward parameters in `config.py`
- Reduced collision penalty for better early-stage learning
- Added forward progress rewards
- Integrated checkpoint system into reward calculation
- Normalized rewards for consistent learning

### Better Metrics & Logging
- Comprehensive metrics tracking (exploration rate, collision rate, distance)
- JSON-based detailed logging for analysis
- New visualization script for multi-metric analysis
- Real-time exploration rate display during training

### Code Quality
- Removed unnecessary imports and path manipulations
- Fixed internationalization issues (Spanish comments)
- Added `requirements.txt` for easier setup
- Configurable reward parameters for experimentation

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- OpenAI for inspiring the use of AI and reinforcement learning concepts.
- Pygame for the graphics library used in this project.
