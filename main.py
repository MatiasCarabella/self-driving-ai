import pygame
import time
import pickle
from vehicle import Vehicle
from environment import Environment
from config import SESSION_CONFIG
from q_learning_agent import QLearningAgent
from logger import Logger

def load_q_table():
    try:
        with open("q_table.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("No previous Q-table found. Starting from scratch.")
        return None

def save_q_table(q_table):
    with open("q_table.pkl", "wb") as f:
        pickle.dump(q_table, f)

def get_state(vehicle):
    road_status = vehicle.check_road_status(vehicle.x, vehicle.y)
    return (
        1 if road_status != "completely_off" else 0,
        int(vehicle.speed),
        int(vehicle.angle),
    ) + tuple(int(sensor.distance / 10) for sensor in vehicle.sensors)

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
            reward = vehicle.update_manual()
            if reward != 0:
                run = False
            reward += vehicle.check_off_track() + vehicle.check_speed()
        else:
            state = get_state(vehicle)
            action = agent.get_action(state)
            reward = vehicle.update_from_agent(action)
            if reward != 0:
                run = False
            next_state = get_state(vehicle)
            reward += vehicle.check_off_track() + vehicle.check_speed()
            agent.update_q_value(state, action, round(reward, 1), next_state)
            agent.decay_exploration()

        vehicle.draw(environment.window)
        draw_hud(environment, vehicle, remaining_time)
        pygame.display.update()

    return vehicle.score, window_closed

def draw_hud(environment, vehicle, remaining_time):
    environment.draw_score(vehicle.score)
    environment.draw_timer(remaining_time)
    environment.draw_speed(vehicle.speed)
    environment.draw_sensor_values(vehicle.sensors)
    is_on_track = vehicle.check_road_status(vehicle.x, vehicle.y) != "completely_off"
    environment.draw_vehicle_status(is_on_track, vehicle.angle)

def main():
    environment = Environment()
    start_position = environment.find_start_position()
    if start_position is None:
        raise ValueError("No starting point found on the circuit.")

    vehicle = Vehicle(*start_position)
    state_size, action_size = 8, 4
    agent = QLearningAgent(state_size, action_size)
    agent.q_table = load_q_table() or agent.q_table

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
            save_q_table(agent.q_table)
        print(f"Episode {episode + 1} completed. Final score: {score}")
        logger.log_score(score)

    pygame.quit()

if __name__ == "__main__":
    main()