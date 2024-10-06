import os
import pygame
import math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, RED, GREEN, GRAY, YELLOW, FONT_BIG, FONT_SMALL

class Environment:
    def __init__(self):
        # Atributos: Dimensiones
        self.SCREEN_WIDTH = WINDOW_WIDTH
        self.SCREEN_HEIGHT = WINDOW_HEIGHT

        # Atributos: Colores
        self.ROAD_COLOR = BLACK
        self.BACKGROUND_COLOR = WHITE
        self.VEHICLE_COLOR = RED
        self.SENSOR_COLOR = GREEN
        self.START_COLOR = YELLOW
        self.CHECKPOINT_COLOR = GRAY
        self.TEXT_COLOR =  WHITE
        self.TEXTBOX_COLOR = BLACK

        # Inicializamos PyGame
        pygame.init()

        # Fuente para el texto de puntuación y temporizador
        pygame.font.init()
        self.FONT_BIG = pygame.font.Font(None, FONT_BIG)
        self.FONT_SMALL = pygame.font.Font(None, FONT_SMALL)

        # Configurar la ventana de PyGame
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Self Driving AI")

        # Obtener la ruta absoluta del directorio donde se está ejecutando el archivo .py
        current_directory = os.path.dirname(os.path.abspath(__file__))
        circuit_image_path = os.path.join(current_directory, "assets/images/circuit.png")

        # Cargar la imagen del circuito desde la ruta relativa
        self.CIRCUIT_IMAGE = pygame.image.load(circuit_image_path).convert()
        self.CIRCUIT_IMAGE = pygame.transform.scale(self.CIRCUIT_IMAGE, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def find_start_position(self):
        """Busca el primer píxel con el color de inicio y determina la dirección inicial"""
        for y in range(self.CIRCUIT_IMAGE.get_height()):
            for x in range(self.CIRCUIT_IMAGE.get_width()):
                if self.CIRCUIT_IMAGE.get_at((x, y)) == self.START_COLOR:
                    # Buscar la dirección de la pista
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # izquierda, derecha, arriba, abajo
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.CIRCUIT_IMAGE.get_width() and 0 <= ny < self.CIRCUIT_IMAGE.get_height():
                            if self.CIRCUIT_IMAGE.get_at((nx, ny)) == self.ROAD_COLOR:
                                # Calcular el ángulo inicial
                                angle = math.degrees(math.atan2(-dy, dx))
                                return x, y, angle
        return None

    def draw_circuit(self):
        """Dibuja la imagen del circuito en la ventana"""
        self.window.blit(self.CIRCUIT_IMAGE, (0, 0))

    def clear_screen(self):
        """Limpia la pantalla con el color de fondo"""
        self.window.fill(self.BACKGROUND_COLOR)

    def draw_score(self, vehicle_score):
        """Dibuja la puntuación en la esquina superior izquierda"""
        score_text = self.FONT_BIG.render(f"Puntos: {vehicle_score}", True, self.TEXT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (score_rect.left - 5, score_rect.top - 5, 
                                         score_rect.width + 10, score_rect.height + 10))
        self.window.blit(score_text, score_rect)

    def draw_timer(self, remaining_time):
        """Dibuja el temporizador en la esquina superior derecha"""
        timer_text = self.FONT_BIG.render(f"Tiempo: {remaining_time:.1f}", True, self.TEXT_COLOR)
        timer_rect = timer_text.get_rect()
        timer_rect.topright = (self.SCREEN_WIDTH - 10, 10)
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (timer_rect.left - 5, timer_rect.top - 5, 
                                         timer_rect.width + 10, timer_rect.height + 10))
        self.window.blit(timer_text, timer_rect)

    def draw_speed(self, vehicle_speed):
        """Dibuja la velocidad actual del vehículo en la esquina inferior derecha"""
        speed_text = self.FONT_BIG.render(f"Velocidad: {vehicle_speed:.1f}", True, self.TEXT_COLOR)
        speed_rect = speed_text.get_rect()
        speed_rect.bottomright = (self.SCREEN_WIDTH - 10, self.SCREEN_HEIGHT - 10)
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (speed_rect.left - 5, speed_rect.top - 5, 
                                            speed_rect.width + 10, speed_rect.height + 10))
        self.window.blit(speed_text, speed_rect)

    def draw_sensor_values(self, vehicle_sensors):
        """Dibuja los valores de los sensores en la esquina inferior derecha, justo encima del indicador de velocidad."""
        sensor_texts = [f"Sensor {i+1}: {sensor.distance:.1f}" for i, sensor in enumerate(vehicle_sensors)]
        sensor_texts.reverse()  # Invertir el orden de los textos

        base_x = self.SCREEN_WIDTH - 10
        base_y = self.SCREEN_HEIGHT - 50  # Ubicado justo encima de la velocidad

        for i, sensor_text in enumerate(sensor_texts):
            text_surface = self.FONT_SMALL.render(sensor_text, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect()
            text_rect.bottomright = (base_x, base_y - i * 20)  # Colocar los textos en orden
            pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (text_rect.left - 5, text_rect.top - 5,
                                                            text_rect.width + 10, text_rect.height + 10))
            self.window.blit(text_surface, text_rect)

