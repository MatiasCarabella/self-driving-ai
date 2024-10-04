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
        self.angle = initial_angle
        self.speed = 0  # Velocidad inicial
        self.max_speed = 6  # Velocidad máxima en carretera
        self.max_speed_partially_off = 3  # Velocidad máxima cuando está parcialmente fuera
        self.max_speed_completely_off = 1  # Velocidad máxima cuando está completamente fuera
        self.acceleration = 0.2
        self.desacceleration = 0.95
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
            self.speed *= self.desacceleration  # Desaceleración natural

        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed * (self.speed / self.max_speed)  # Girar más rápido a más velocidad
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed * (self.speed / self.max_speed)

        # Actualizar la posición basada en el ángulo y velocidad
        rad_angle = math.radians(self.angle)
        new_x = self.x + self.speed * math.cos(rad_angle)
        new_y = self.y - self.speed * math.sin(rad_angle)

        # Comprobar si está completamente fuera o parcialmente fuera
        road_status = self.check_road_status(new_x, new_y)

        if road_status == "on_road":
            self.x = new_x
            self.y = new_y
            self.max_speed = 6  # Restablecer velocidad máxima al volver a la carretera
            self.speed = min(self.speed, self.max_speed)  # Asegurarse de que la velocidad no exceda el máximo
        elif road_status == "partially_off":
            self.max_speed = self.max_speed_partially_off  # Reducir velocidad máxima si está parcialmente fuera
            if self.speed > self.max_speed_partially_off:
                self.speed *= self.desacceleration  # Desaceleración natural  # Mantener velocidad dentro de los límites
            # Permitir el movimiento, pero con penalización de velocidad
            self.x = new_x
            self.y = new_y
        elif road_status == "completely_off":
            self.max_speed = self.max_speed_completely_off  # Reducir velocidad máxima si está completamente fuera
            if self.speed > self.max_speed_completely_off:
                self.speed *= self.desacceleration  # Desaceleración natural  # Mantener velocidad dentro de los límites
            # Permitir el movimiento, pero con penalización de velocidad
            self.x = new_x
            self.y = new_y

        # Actualizar sensores
        self.update_sensors()

    def check_road_status(self, x, y):
        """Determina si el vehículo está en la carretera, parcialmente fuera o completamente fuera"""
        rect = pygame.Rect(x - self.width / 2, y - self.height / 2, self.width, self.height)
        rotated_rect = self.get_rotated_vertices(rect)

        # Contador para las esquinas sobre la carretera
        on_road_count = 0
        total_corners = len(rotated_rect)

        for vertex in rotated_rect:
            if self.is_on_road(vertex[0], vertex[1]):
                on_road_count += 1

        # Determinar el estado del vehículo según las esquinas sobre la carretera
        if on_road_count == total_corners:
            return "on_road"  # Completamente en la carretera
        elif on_road_count > 0:
            return "partially_off"  # Parcialmente fuera
        else:
            return "completely_off"  # Completamente fuera

    def get_rotated_vertices(self, rect):
        """Obtiene los vértices del rectángulo del vehículo rotado"""
        rad_angle = math.radians(self.angle)
        cx, cy = rect.center

        corners = [
            (rect.topleft),
            (rect.topright),
            (rect.bottomright),
            (rect.bottomleft)
        ]

        rotated_corners = []
        for corner in corners:
            dx, dy = corner[0] - cx, corner[1] - cy
            rotated_x = cx + dx * math.cos(rad_angle) - dy * math.sin(rad_angle)
            rotated_y = cy + dx * math.sin(rad_angle) + dy * math.cos(rad_angle)
            rotated_corners.append((rotated_x, rotated_y))

        return rotated_corners

    def is_on_road(self, x, y):
        """Comprueba si una posición dada está sobre la carretera"""
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            color_at_position = circuit_image.get_at((int(x), int(y)))
            return color_at_position == BLACK or color_at_position == YELLOW
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