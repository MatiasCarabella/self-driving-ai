import os
import pygame
import math

# Inicializamos PyGame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de vehículo en 2D con circuito de imagen")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
START_COLOR = YELLOW  # Color que representa el punto de inicio

# Obtener la ruta absoluta del directorio donde se está ejecutando el archivo .py
current_directory = os.path.dirname(os.path.abspath(__file__))
circuit_image_path = os.path.join(current_directory, "circuito.png")

# Cargar la imagen del circuito desde la ruta relativa
circuit_image = pygame.image.load(circuit_image_path).convert()
circuit_image = pygame.transform.scale(circuit_image, (WIDTH, HEIGHT))

# Función para buscar el punto de inicio en la imagen basada en el color
def find_start_position(image, start_color):
    """Busca el primer píxel con el color de inicio y determina la dirección inicial"""
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            if image.get_at((x, y)) == start_color:
                # Buscar la dirección de la pista
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # izquierda, derecha, arriba, abajo
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < image.get_width() and 0 <= ny < image.get_height():
                        if image.get_at((nx, ny)) == BLACK:
                            # Calcular el ángulo inicial
                            angle = math.degrees(math.atan2(-dy, dx))
                            return x, y, angle
    return None

# Configuración del vehículo
class Vehicle:
    def __init__(self, x, y, width, height, initial_angle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = initial_angle  # Usar el ángulo inicial proporcionado
        self.speed = 0  # Velocidad
        self.max_speed = 6
        self.acceleration = 0.2
        self.rotation_speed = 4  # Velocidad de rotación
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(RED)
        self.sensors = []  # Lista de sensores (rayos) con distancia

    def draw(self, window):
        # Rotar la imagen del vehículo sin cambiar sus dimensiones originales
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        window.blit(rotated_image, new_rect.topleft)

        # Dibujar los sensores
        for sensor, _ in self.sensors:
            pygame.draw.line(window, GREEN, (self.x, self.y), sensor, 2)

    def update(self):
        # Movimiento del vehículo
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if self.speed < self.max_speed:
                self.speed += self.acceleration
        elif keys[pygame.K_DOWN]:
            if self.speed > -self.max_speed:
                self.speed -= self.acceleration
        else:
            self.speed *= 0.98  # Desaceleración natural

        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed * (self.speed / self.max_speed)  # Girar más rápido a más velocidad
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed * (self.speed / self.max_speed)

        # Actualizar la posición basada en el ángulo y velocidad
        rad_angle = math.radians(self.angle)
        new_x = self.x + self.speed * math.cos(rad_angle)
        new_y = self.y - self.speed * math.sin(rad_angle)

        # Comprobar colisiones con el circuito (imagen)
        if self.is_on_road(new_x, new_y):
            self.x = new_x
            self.y = new_y

        # Actualizar sensores
        self.update_sensors()

    def is_on_road(self, x, y):
        """Comprueba si el vehículo está sobre la carretera (color negro)"""
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            color_at_position = circuit_image.get_at((int(x), int(y)))
            return color_at_position == BLACK or color_at_position == YELLOW  # Solo es carretera si el color es negro o amarillo (inicio)
        return False

    def update_sensors(self):
        """ Actualiza los sensores y devuelve la distancia al obstáculo o carretera """
        self.sensors = []
        sensor_angles = [-90, -45, 0, 45, 90]  # Ángulos relativos al frente del vehículo
        sensor_length = 150  # Longitud máxima de los sensores

        for angle_offset in sensor_angles:
            sensor_angle = math.radians(self.angle + angle_offset)
            end_x = self.x + sensor_length * math.cos(sensor_angle)
            end_y = self.y - sensor_length * math.sin(sensor_angle)
            sensor_end = (end_x, end_y)

            # Calcular la distancia hasta colisión
            distance = sensor_length
            if not self.is_on_road(end_x, end_y):
                distance = math.sqrt((self.x - end_x) ** 2 + (self.y - end_y) ** 2)

            # Guardar la posición final del sensor y la distancia
            self.sensors.append((sensor_end, distance))

# Bucle principal
def main():
    clock = pygame.time.Clock()
    run = True

    # Buscar la posición y dirección inicial basada en el color del circuito
    start_info = find_start_position(circuit_image, START_COLOR)
    if start_info:
        x, y, angle = start_info
        vehicle = Vehicle(x, y, 40, 20, angle)
    else:
        vehicle = Vehicle(WIDTH // 2, HEIGHT // 2, 40, 20, 0)  # Posición y ángulo por defecto si no se encuentra

    while run:
        clock.tick(60)
        window.fill((255, 255, 255))  # Limpiar la pantalla con blanco

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Dibujar el circuito
        window.blit(circuit_image, (0, 0))

        # Actualizar y dibujar el vehículo
        vehicle.update()
        vehicle.draw(window)

        # Actualizar la pantalla
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()