import pygame
from config import SESSION_CONFIG
from models.vehicle import Vehicle
from models.environment import Environment
from machine_learning.q_learning.agent import QLearningAgent
from logs.logger import Logger

def run_episode(environment, vehicle, agent, manual_control):
    start_ticks = pygame.time.get_ticks()
    run = True
    window_closed = False

    while run:
        clock = pygame.time.Clock()
        clock.tick(60)
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
            vehicle.update_manual()
            vehicle.calculate_reward()
        else:
            state = vehicle.get_state()
            action = agent.get_action(state)
            vehicle.update_from_agent(action)
            reward = vehicle.calculate_reward()
            next_state = vehicle.get_state()
            agent.update_q_value(state, action, round(reward, 1), next_state)
            agent.decay_exploration()

        vehicle.draw(environment.window)
        environment.draw_hud(vehicle, remaining_time)
        pygame.display.update()

    return vehicle.score, window_closed

def main():
    environment = Environment()
    start_position = environment.find_start_position()
    if start_position is None:
        raise ValueError("No starting point found on the circuit.")

    vehicle = Vehicle(*start_position)
    state_size, action_size = 6, 4
    agent = QLearningAgent(state_size, action_size)
    agent.load_q_table()  # Cargar la Q-table si existe

    logger = Logger()
    num_episodes = 1 if SESSION_CONFIG["MANUAL_CONTROL"] else SESSION_CONFIG["NUM_EPISODES"]

    for episode in range(num_episodes):
        print(f"Starting episode {episode + 1}/{num_episodes}")
        vehicle.reset()
        score, window_closed = run_episode(environment, vehicle, agent, SESSION_CONFIG["MANUAL_CONTROL"])
        
        if window_closed:
            print("Window closed. Ending training session.")
            break

        if not SESSION_CONFIG["MANUAL_CONTROL"]:
            agent.save_q_table()  # Guardar la Q-table después de cada episodio
        print(f"Episode {episode + 1} completed. Final score: {score}")
        logger.log_score(score)

    pygame.quit()

if __name__ == "__main__":
    main()
