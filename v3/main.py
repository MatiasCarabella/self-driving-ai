import pygame
import time
from vehicle import Vehicle
from environment import Environment

# Inicializamos PyGame
pygame.init()

# Duración del episodio en segundos
EPISODE_DURATION = 15

# Crear el entorno
environment = Environment()

# Inicializar el vehículo
start_position = environment.find_start_position()
if start_position is None:
    raise ValueError("No se encontró un punto de inicio en el circuito.")
vehicle = Vehicle(start_position[0], start_position[1], 20, 10, start_position[2])

# Bucle principal
def main():
    clock = pygame.time.Clock()
    run = True
    checkpoints = {}  # Diccionario para almacenar checkpoints y sus tiempos
    start_ticks = pygame.time.get_ticks()  # Iniciar el temporizador
    vehicle.last_penalty_time = time.time()  # Inicializar el tiempo de la última penalización
    vehicle.score = 0  # Inicializar la puntuación del vehículo
    vehicle.last_checkpoint = None  # Inicializar el último checkpoint cruzado

    while run:
        clock.tick(60)
        environment.clear_screen()  # Limpiar la pantalla con el color de fondo
        
        current_time = time.time()
        # Obtener el tiempo transcurrido y restante
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Tiempo transcurrido en segundos
        remaining_time = max(0, EPISODE_DURATION - elapsed_time)  # Tiempo restante en segundos

        if remaining_time == 0:  # Si se ha acabado el tiempo
            print(f"Fin del episodio. Puntuación final: {vehicle.score}")
            run = False  # Terminar el episodio

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Dibujar el circuito
        environment.draw_circuit()

        # Actualizar y dibujar el vehículo
        vehicle.update()
        vehicle.draw(environment.window)

        # Verificar si el vehículo cruzó un checkpoint
        if vehicle.check_checkpoint(current_time, checkpoints):
            vehicle.score += 5  # Añadir 5 puntos por cada checkpoint
            print(f"Checkpoint cruzado! Puntuación: {vehicle.score}")

        # Verificar si el vehículo está fuera del circuito
        vehicle.check_off_track()

        # Dibujar la puntuación y el temporizador
        environment.draw_score(vehicle.score)
        environment.draw_timer(remaining_time)

        # Actualizar la pantalla
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
