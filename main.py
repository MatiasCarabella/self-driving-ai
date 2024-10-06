import pygame
import time
import pickle  # Para guardar la Q-table
from vehicle import Vehicle
from environment import Environment
from config import SESSION_CONFIG
from q_learning_agent import QLearningAgent

# Crear el entorno
environment = Environment()

# Inicializar el vehículo
start_position = environment.find_start_position()
if start_position is None:
    raise ValueError("No se encontró un punto de inicio en el circuito.")
vehicle = Vehicle(start_position[0], start_position[1], start_position[2])

# Inicializar el agente de Q-learning
state_size = 5  # Suponiendo que hay 5 sensores
action_size = 4  # Las acciones son: acelerar, girar izquierda, girar derecha, no hacer nada
agent = QLearningAgent(state_size, action_size)

# Definir el número de episodios de entrenamiento si MANUAL_CONTROL es False
NUM_EPISODES = SESSION_CONFIG["NUM_EPISODES"] if not SESSION_CONFIG["MANUAL_CONTROL"] else 1

# Cargar la Q-table si ya existe (esto es opcional)
try:
    with open("q_table.pkl", "rb") as f:
        agent.q_table = pickle.load(f)
    print("Q-table cargada correctamente.")
except FileNotFoundError:
    print("No se encontró una Q-table previa. Se empezará desde cero.")

# Bucle de episodios
def main():
    continue_training = True  # Flag para continuar el entrenamiento
    for episode in range(NUM_EPISODES):
        print(f"Iniciando episodio {episode + 1}/{NUM_EPISODES}")

        # Resetear el vehículo al inicio de cada episodio
        vehicle.reset()
        start_ticks = pygame.time.get_ticks()  # Reiniciar el temporizador
        run = True
        checkpoints = {}

        while run and continue_training:
            clock = pygame.time.Clock()
            clock.tick(60)
            environment.clear_screen()  # Limpiar la pantalla con el color de fondo

            current_time = time.time()
            # Obtener el tiempo transcurrido y restante
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Tiempo transcurrido en segundos
            remaining_time = max(0, SESSION_CONFIG["EPISODE_DURATION"] - elapsed_time)  # Tiempo restante en segundos

            if remaining_time == 0:  # Si se ha acabado el tiempo
                print(f"Fin del episodio. Puntuación final: {vehicle.score}")
                run = False  # Terminar el episodio

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # Terminar la ejecución
                    continue_training = False  # Detener todo el entrenamiento
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Presionar "Esc" para detener el entrenamiento
                        run = False  # Terminar la ejecución
                        continue_training = False  # Detener todo el entrenamiento

            # Dibujar el circuito
            environment.draw_circuit()

            # Verificar si el control es manual o del agente
            if SESSION_CONFIG["MANUAL_CONTROL"]:
                collision = vehicle.update_manual()  # Control manual

                vehicle.check_checkpoint(current_time, checkpoints)  # Recompensa por checkpoints
                vehicle.check_off_track()  # Penalización por salirse del circuito
                vehicle.check_speed()  # Recompensa basada en la velocidad
            else:
                # Obtener el estado discreto del vehículo (por ejemplo, distancias de los sensores)
                state = tuple(int(sensor[1] / 10) for sensor in vehicle.sensors)  # Convertir distancias a estado discreto
                
                # Elegir una acción usando el agente
                action = agent.get_action(state)
                
                # Actualizar el vehículo basado en la acción elegida por el agente
                collision = vehicle.update_from_agent(action)

                # Obtener el siguiente estado después de la acción
                next_state = tuple(int(sensor[1] / 10) for sensor in vehicle.sensors)

                # Obtener la recompensa utilizando las funciones check_checkpoint, check_off_track y check_speed
                reward = 0
                reward += vehicle.check_checkpoint(current_time, checkpoints)  # Recompensa por checkpoints
                reward += vehicle.check_off_track()  # Penalización por salirse del circuito
                reward += vehicle.check_speed()  # Recompensa basada en la velocidad

                # Actualizar la Q-table
                agent.update_q_value(state, action, round(reward,1), next_state)

                # Decaer la tasa de exploración
                agent.decay_exploration()

            # Si hay colisión con los límites, detener el episodio
            if collision:
                print("Colisión con los límites de la ventana. Fin del episodio.")
                run = False

            # Dibujar el vehículo
            vehicle.draw(environment.window)

            # HUD
            environment.draw_score(vehicle.score)
            environment.draw_timer(remaining_time)
            environment.draw_speed(vehicle.speed)
            environment.draw_sensor_values(vehicle.sensors)

            # Actualizar la pantalla
            pygame.display.update()

        # Almacenar la Q-table después de cada episodio si el agente está en control
        if not SESSION_CONFIG["MANUAL_CONTROL"]:
            with open("q_table.pkl", "wb") as f:
                pickle.dump(agent.q_table, f)
            print(f"Episodio {episode + 1} completado. Puntuación: {vehicle.score}")

    pygame.quit()

if __name__ == "__main__":
    main()