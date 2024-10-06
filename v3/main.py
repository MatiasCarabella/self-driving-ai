import pygame
import time
from vehicle import Vehicle
from environment import Environment

# Inicializamos PyGame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de vehículo en 2D con circuito de imagen")

# Fuente para el texto de puntuación y temporizador
FONT = pygame.font.Font(None, 36)

# Duración del episodio en segundos
EPISODE_DURATION = 15

enviroment = Environment()

# Inicializar el vehículo
start_position = enviroment.find_start_position()
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
        window.fill(enviroment.BACKGROUND_COLOR)  # Limpiar la pantalla con blanco
        
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
        enviroment.draw_circuit()

        # Actualizar y dibujar el vehículo
        vehicle.update()
        vehicle.draw(window)

        # Verificar si el vehículo cruzó un checkpoint
        if vehicle.check_checkpoint(current_time, checkpoints):
            vehicle.score += 5  # Añadir 5 puntos por cada checkpoint
            print(f"Checkpoint cruzado! Puntuación: {vehicle.score}")

        # Verificar si el vehículo está fuera del circuito
        vehicle.check_off_track()

        # Dibujar la puntuación en la pantalla (esquina superior izquierda)
        score_text = FONT.render(f"Puntos: {vehicle.score}", True, enviroment.TEXT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)
        pygame.draw.rect(window, enviroment.TEXTBOX_COLOR, (score_rect.left - 5, score_rect.top - 5, 
                                         score_rect.width + 10, score_rect.height + 10))
        window.blit(score_text, score_rect)

        # Dibujar el temporizador en la pantalla (esquina superior derecha)
        timer_text = FONT.render(f"Tiempo: {remaining_time:.1f}", True, enviroment.TEXT_COLOR)
        timer_rect = timer_text.get_rect()
        timer_rect.topright = (WIDTH - 10, 10)
        pygame.draw.rect(window, enviroment.TEXTBOX_COLOR, (timer_rect.left - 5, timer_rect.top - 5, 
                                         timer_rect.width + 10, timer_rect.height + 10))
        window.blit(timer_text, timer_rect)

        # Actualizar la pantalla
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()