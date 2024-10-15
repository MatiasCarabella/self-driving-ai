import os
import pygame
from config import SESSION_CONFIG
from models.vehicle import Vehicle
from models.environment import Environment
from machine_learning.q_learning.agent import QLearningAgent
from logs.logger import Logger

def run_episode(environment, vehicle, agent, manual_control):
    """
    Run a single episode of the simulation.

    Args:
        environment (Environment): The game environment.
        vehicle (Vehicle): The vehicle object.
        agent (QLearningAgent): The Q-learning agent.
        manual_control (bool): Whether the vehicle is manually controlled.

    Returns:
        tuple: (score, window_closed) - The final score and whether the window was closed.
    """
    start_ticks = pygame.time.get_ticks()
    run = True
    window_closed = False

    while run:
        clock = pygame.time.Clock()
        clock.tick(60)  # Limit the frame rate to 60 FPS
        environment.clear_screen()

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, SESSION_CONFIG["EPISODE_DURATION"] - elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                window_closed = True
                break

        if remaining_time == 0:
            run = False
            continue

        environment.draw_circuit()

        if manual_control:
            vehicle.handle_manual_input()
            vehicle.calculate_reward()
        else:
            state = vehicle.get_state()
            action = agent.get_action(state)
            vehicle.handle_agent_action(action)
            reward = vehicle.calculate_reward()
            next_state = vehicle.get_state()

            if SESSION_CONFIG["LEARNING_MODE"]:  # Only update Q-values if in learning mode
                agent.update_q_value(state, action, round(reward, 1), next_state)
                agent.decay_exploration()

        if vehicle.collided:
            run = False

        vehicle.draw(environment.window)
        environment.draw_hud(vehicle, remaining_time)
        pygame.display.update()

    return vehicle.score, window_closed

def main():
    """
    Main function to run the simulation.
    """
    environment = Environment()
    vehicle = Vehicle(environment)
    state_size, action_size = 6, 4
    agent = QLearningAgent(state_size, action_size)
    agent.load_q_table()  # Load the Q-table if it exists

    # Get the Q-table filename directly from the agent's 'q_table_path' attribute
    q_table_filename = os.path.basename(agent.q_table_path)  # Extract only the filename (e.g., "v1.pkl")
    log_filename = q_table_filename.replace(".pkl", ".txt")  # Change the extension to ".txt"
    logger = Logger(os.path.join("q_learning", log_filename))

    num_episodes = 1 if SESSION_CONFIG["MANUAL_CONTROL"] else SESSION_CONFIG["NUM_EPISODES"]

    for episode in range(num_episodes):
        print(f"Starting episode {episode + 1}/{num_episodes}")
        vehicle.reset()
        score, window_closed = run_episode(environment, vehicle, agent, SESSION_CONFIG["MANUAL_CONTROL"])

        if window_closed:
            print("Window closed. Ending training session.")
            break

        # Save the Q-table and log the progress only if in learning mode
        if not SESSION_CONFIG["MANUAL_CONTROL"] and SESSION_CONFIG["LEARNING_MODE"]:
            agent.save_q_table()
            logger.log_score(score)

        print(f"Episode {episode + 1} completed. Final score: {score}")

    pygame.quit()

if __name__ == "__main__":
    main()