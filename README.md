<h1 align="center">2D Self-Driving Car Simulation</h1>

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

## Installation
To run this project, you will need to have Python 3.x installed along with the Pygame library. You can install the required libraries using pip:
```bash
pip install pygame
```

## Usage
1. Clone the repository to your local machine:
```bash
git clone https://github.com/matiascarabella/self-driving-ai.git
```

2. Navigate to the project directory:
```bash
cd self-driving-ai
```

3. Run the simulation:
```bash
python main.py
```

4. Let the AI agent learn through Q-learning  
   <sup>Or control the vehicle yourself by setting `MANUAL_CONTROL = True` in the config.py file</sup>

## Configuration
The project includes a `config.py` file where you can adjust various parameters:

### Session Configuration
```python
SESSION_CONFIG = {
    "TRAINING_MODE": True,    # Toggle between training and evaluation modes
    "NUM_EPISODES": 50,       # Number of episodes to run
    "EPISODE_DURATION": 20,   # Duration of each episode in seconds
    "MANUAL_CONTROL": False   # Enable manual control with arrow keys
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
The training results are logged within the `logs` folder in a file named `v1.txt`, which records the episode number and the final score. This log can be used for performance analysis and progress visualization.

## Visualizing Progress
To visualize the agent's progress, use the `visualization/plot_progress.py` script:
```bash
python visualization/plot_progress.py
```

This will generate a graph of the scores over episodes, allowing you to see how the agent is improving over time:
<p align="center">
  <img src="https://github.com/user-attachments/assets/3dd718fe-2712-4cbc-8b63-2d82a52b8cf6" />
</p>

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- OpenAI for inspiring the use of AI and reinforcement learning concepts.
- Pygame for the graphics library used in this project.
