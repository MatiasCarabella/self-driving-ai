import os
import sys
import argparse
import pygame
from config import SESSION_CONFIG, CIRCUIT_CONFIG
from models.vehicle import Vehicle
from models.environment import Environment
from machine_learning.q_learning.agent import QLearningAgent
from logs.logger import Logger

def run_episode(environment, vehicle, agent, manual_control, headless=False, frame_skip=1):
    """
    Run a single episode of the simulation.

    Args:
        environment (Environment): The game environment.
        vehicle (Vehicle): The vehicle object.
        agent (QLearningAgent): The Q-learning agent.
        manual_control (bool): Whether the vehicle is manually controlled.
        headless (bool): Whether to run without rendering.
        frame_skip (int): Process every Nth frame.

    Returns:
        tuple: (score, window_closed) - The final score and whether the window was closed.
    """
    start_ticks = pygame.time.get_ticks()
    run = True
    window_closed = False
    frame_count = 0

    while run:
        if not headless:
            clock = pygame.time.Clock()
            clock.tick(60)  # Limit the frame rate to 60 FPS
        
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, SESSION_CONFIG["EPISODE_DURATION"] - elapsed_time)

        if not headless:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    window_closed = True
                    break

        if remaining_time == 0:
            run = False
            continue

        # Only render every Nth frame
        should_render = (frame_count % frame_skip == 0) and not headless
        
        if should_render:
            environment.clear_screen()
            environment.draw_circuit()

        if manual_control:
            vehicle.handle_manual_input()
            vehicle.calculate_reward()
        else:
            state = vehicle.get_state()
            # Use epsilon-greedy only in learning mode
            action = agent.get_action(state, use_epsilon=SESSION_CONFIG["TRAINING_MODE"])
            vehicle.handle_agent_action(action)
            reward = vehicle.calculate_reward()
            next_state = vehicle.get_state()

            if SESSION_CONFIG["TRAINING_MODE"]:
                agent.update_q_value(state, action, round(reward, 1), next_state)
                agent.decay_exploration()

        if vehicle.collided or vehicle.finished:
            run = False

        if should_render:
            vehicle.draw(environment.window)
            environment.draw_hud(vehicle, remaining_time)
            pygame.display.update()
        
        frame_count += 1

    return vehicle.score, window_closed

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Self-Driving AI Training')
    parser.add_argument('--circuit', choices=['circuit_1', 'circuit_2'], 
                       help='Which circuit to use')
    parser.add_argument('--episodes', type=int, 
                       help='Number of episodes to run')
    parser.add_argument('--headless', action='store_true',
                       help='Run without rendering (faster)')
    parser.add_argument('--eval', action='store_true',
                       help='Run in evaluation mode (no training)')
    parser.add_argument('--manual', action='store_true',
                       help='Enable manual control')
    return parser.parse_args()

def main():
    """
    Main function to run the simulation.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Override config with CLI arguments
    if args.circuit:
        SESSION_CONFIG["CIRCUIT"] = args.circuit
        # Reload window config
        from config import get_window_config
        globals()['WINDOW_CONFIG'] = get_window_config()
    if args.episodes:
        SESSION_CONFIG["NUM_EPISODES"] = args.episodes
    if args.headless:
        SESSION_CONFIG["HEADLESS"] = True
    if args.eval:
        SESSION_CONFIG["TRAINING_MODE"] = False
    if args.manual:
        SESSION_CONFIG["MANUAL_CONTROL"] = True
    
    headless = SESSION_CONFIG.get("HEADLESS", False)
    frame_skip = SESSION_CONFIG.get("FRAME_SKIP", 1)
    
    if headless:
        print("Running in HEADLESS mode (no rendering) - much faster!")
    if frame_skip > 1:
        print(f"Frame skip enabled: rendering every {frame_skip} frames")
    
    environment = Environment(headless=headless)
    vehicle = Vehicle(environment)
    # State: speed (1) + 5 sensors = 6 dimensions
    state_size, action_size = 6, 4
    agent = QLearningAgent(state_size, action_size)

    # Load Q-table based on mode
    if SESSION_CONFIG["TRAINING_MODE"]:
        if agent.load_q_table():
            print(f"Training mode: Q-table loaded from {agent.q_table_path}")
        else:
            print("Training mode: No previous Q-table found. Starting fresh.")
    else:
        if agent.load_q_table():
            print(f"Evaluation mode: Using saved Q-table from {agent.q_table_path}")
        else:
            print("Warning: No Q-table found for evaluation mode!")
            return

    # Setup logging
    q_table_filename = os.path.basename(agent.q_table_path)
    log_filename = q_table_filename.replace(".pkl", ".txt")
    logger = Logger(os.path.join("q_learning", log_filename))

    num_episodes = 1 if SESSION_CONFIG["MANUAL_CONTROL"] else SESSION_CONFIG["NUM_EPISODES"]

    import time
    start_time = time.time()

    for episode in range(num_episodes):
        episode_start = time.time()
        vehicle.reset()
        score, window_closed = run_episode(
            environment, vehicle, agent, SESSION_CONFIG["MANUAL_CONTROL"],
            headless=headless, frame_skip=frame_skip
        )

        if window_closed:
            print("Window closed. Ending session.")
            break

        # Save Q-table and log metrics only in training mode
        if not SESSION_CONFIG["MANUAL_CONTROL"] and SESSION_CONFIG["TRAINING_MODE"]:
            agent.save_q_table()
            logger.log_score(score)
            logger.log_metrics(
                episode=episode + 1,
                score=score,
                exploration_rate=agent.get_exploration_rate(),
                collided=vehicle.collided,
                distance_traveled=vehicle.total_distance
            )

        episode_time = time.time() - episode_start
        finish_status = "✓" if vehicle.finished else ("✗" if vehicle.collided else "⏱")
        print(f"Ep {episode + 1}/{num_episodes}: {finish_status} {score:.0f} pts | {vehicle.total_distance:.0f}m | ε={agent.get_exploration_rate():.2f} | {episode_time:.1f}s")

    total_time = time.time() - start_time
    print(f"\nTotal training time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"Average time per episode: {total_time/num_episodes:.1f}s")

    pygame.quit()

if __name__ == "__main__":
    main()