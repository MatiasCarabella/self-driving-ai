import pygame
import time
import pickle  # To save the Q-table
from vehicle import Vehicle
from environment import Environment
from config import SESSION_CONFIG
from q_learning_agent import QLearningAgent
from logger import Logger

# Create the environment
environment = Environment()

# Initialize the vehicle
start_position = environment.find_start_position()
if start_position is None:
    raise ValueError("No starting point found on the circuit.")
vehicle = Vehicle(start_position[0], start_position[1], start_position[2])

# Initialize the Q-learning agent
state_size = 5  # Assuming there are 5 sensors
action_size = 4  # The actions are: accelerate, turn left, turn right, do nothing
agent = QLearningAgent(state_size, action_size)

# Define the number of training episodes if MANUAL_CONTROL is False
NUM_EPISODES = SESSION_CONFIG["NUM_EPISODES"] if not SESSION_CONFIG["MANUAL_CONTROL"] else 1

# Load the Q-table if it exists (this is optional)
try:
    with open("q_table.pkl", "rb") as f:
        agent.q_table = pickle.load(f)
    print("Q-table successfully loaded.")
except FileNotFoundError:
    print("No previous Q-table found. Starting from scratch.")

# Initialize the logger
logger = Logger()

# Main loop for episodes
def main():
    continue_training = True  # Flag to control training
    for episode in range(NUM_EPISODES):
        print(f"Starting episode {episode + 1}/{NUM_EPISODES}")

        # Reset the vehicle at the start of each episode
        vehicle.reset()
        start_ticks = pygame.time.get_ticks()  # Reset the timer
        run = True
        checkpoints = {}

        while run and continue_training:
            clock = pygame.time.Clock()
            clock.tick(60)  # Limit to 60 FPS
            environment.clear_screen()  # Clear the screen

            current_time = time.time()
            # Get elapsed time and remaining time
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Elapsed time in seconds
            remaining_time = max(0, SESSION_CONFIG["EPISODE_DURATION"] - elapsed_time)  # Remaining time in seconds

            if remaining_time == 0:  # If time runs out
                run = False  # End the episode

            # Handle quitting the game or stopping training
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # End the episode
                    continue_training = False  # Stop all training

            # Draw the circuit
            environment.draw_circuit()

            collision = False  # Track if there is a collision

            # Check if control is manual or by the agent
            if SESSION_CONFIG["MANUAL_CONTROL"]:
                reward = vehicle.update_manual()  # Manual control
                if reward != 0:
                    collision = True  # Mark as a collision if the reward is non-zero
                
                # Check additional rewards and penalties
                vehicle.check_checkpoint(current_time, checkpoints)  # Reward for checkpoints
                vehicle.check_off_track()  # Penalty for going off the track
                vehicle.check_speed()  # Reward based on speed
            else:
                # Get the discrete state of the vehicle (e.g., sensor distances)
                state = tuple(int(sensor.distance / 10) for sensor in vehicle.sensors)  # Convert distances to discrete state
                
                # Choose an action using the agent
                action = agent.get_action(state)
                
                # Update the vehicle based on the action chosen by the agent
                reward = vehicle.update_from_agent(action)
                if reward != 0:
                    collision = True  # Mark as a collision if the reward is non-zero

                # Get the next state after the action
                next_state = tuple(int(sensor.distance / 10) for sensor in vehicle.sensors)

                # Check additional rewards and penalties
                reward += vehicle.check_checkpoint(current_time, checkpoints)  # Reward for checkpoints
                reward += vehicle.check_off_track()  # Penalty for going off the track
                reward += vehicle.check_speed()  # Reward based on speed

                # Update the Q-table
                agent.update_q_value(state, action, round(reward, 1), next_state)

                # Decay exploration rate
                agent.decay_exploration()

            # If there was a collision, end the episode
            if collision:
                run = False

            # Draw the vehicle on the window
            vehicle.draw(environment.window)

            # HUD (Head-Up Display)
            environment.draw_score(vehicle.score)  # Show the score
            environment.draw_timer(remaining_time)  # Show the remaining time
            environment.draw_speed(vehicle.speed)  # Show the vehicle speed
            environment.draw_sensor_values(vehicle.sensors)  # Show the sensor values

            # Update the display
            pygame.display.update()

        # Save the Q-table after each episode if the agent is in control
        if not SESSION_CONFIG["MANUAL_CONTROL"]:
            with open("q_table.pkl", "wb") as f:
                pickle.dump(agent.q_table, f)
            print(f"Episode {episode + 1} completed. Final score: {vehicle.score}")

        # Log the episode data
        logger.log_episode(logger.get_last_episode() + 1, vehicle.score)

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
