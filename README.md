# 2D Self-Driving Car Simulation

## About This Project
This project is a 2D self-driving car simulation developed in Python using Pygame. It features a Q-learning agent that learns to navigate a circuit by interacting with its environment and optimizing its actions through a reward system. This simulation serves as an educational tool for understanding reinforcement learning concepts and their practical applications in autonomous driving technology.

## Features
- **Reinforcement Learning**: Implements Q-learning to train an AI agent to navigate a circuit.
- **Sensor System**: The vehicle is equipped with sensors that provide information about its surroundings, allowing for informed decision-making.
- **Visual Feedback**: Real-time visualization of the vehicle's performance, including speed, scores, and sensor values.
- **Logging**: Tracks the performance of the agent across episodes and stores it for further analysis.

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
3. Run the simulation
```bash
python main.py
```
4. Let the AI agent learn through Q-learning, or control the vehicle yourself if you enabled MANUAL_CONTROL = True in the config.py file

## Configuration

The project includes a config.py file where you can adjust various parameters such as:
- Vehicle settings (dimensions, speed, acceleration)
- Q-learning agent parameters (learning rate, discount factor, exploration rate)
- Session parameters (number of episodes, duration)

## Log Files

The training results are logged in a file named training_log.txt, which records the episode number and the final score. This log can be used for performance analysis and progress visualization.
Visualizing Progress

To visualize the agent's progress, use the grapher.py script:
```bash
python grapher.py
```
This will generate a graph of the scores over episodes, allowing you to see how the agent is improving.
## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- OpenAI for inspiring the use of AI and reinforcement learning concepts.
- Pygame for the graphics library used in this project.
