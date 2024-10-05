import os
import pygame
import math
import time

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
GRAY = (128, 128, 128)  # Color que representa el checkpoint
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
            pass  # El agente no puede frenar
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
        """Actualiza los sensores y devuelve la distancia al obstáculo o carretera"""
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

# Función para verificar si el vehículo ha cruzado un checkpoint gris
def check_checkpoint(vehicle):
    """Verifica si el vehículo ha cruzado un checkpoint gris."""
    radius = 1  # Radio de detección
    for dx in range(-radius, radius + 1):  # Búsqueda en un área alrededor del vehículo
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy <= radius * radius:  # Área circular
                check_x = int(vehicle.x + dx)
                check_y = int(vehicle.y + dy)
                if 0 <= check_x < WIDTH and 0 <= check_y < HEIGHT:
                    color_at_position = circuit_image.get_at((check_x, check_y))
                    if color_at_position == GRAY:  # Comprobar si es gris
                        return (check_x, check_y)  # Devolver la posición del checkpoint
    return None

def check_off_track(vehicle):
    """Verifica si el vehículo está fuera del circuito y aplica penalizaciones"""
    current_time = time.time()
    if current_time - vehicle.last_penalty_time >= 0.25:  # Delay de 0.1 segundos
        road_status = vehicle.check_road_status(vehicle.x, vehicle.y)
        
        if road_status != "on_road":
            penalty = -1 if road_status == "partially_off" else -2  # -1 para salida parcial, -2 para total
            vehicle.score += penalty
            vehicle.last_penalty_time = current_time
            print(f"Penalización: {penalty}. Puntuación total: {vehicle.score}")

# Inicializar el vehículo
start_position = find_start_position(circuit_image, START_COLOR)
if start_position is None:
    raise ValueError("No se encontró un punto de inicio en el circuito.")
vehicle = Vehicle(start_position[0], start_position[1], 20, 10, start_position[2])

# Bucle principal
def main():
    clock = pygame.time.Clock()
    run = True
    crossed_checkpoints = set()  # Usar un conjunto para almacenar checkpoints cruzados
    start_ticks = pygame.time.get_ticks()  # Iniciar el temporizador
    vehicle.last_penalty_time = time.time()  # Inicializar el tiempo de la última penalización
    vehicle.score = 0  # Inicializar la puntuación del vehículo

    while run:
        clock.tick(60)
        window.fill((255, 255, 255))  # Limpiar la pantalla con blanco
        
        # Obtener el tiempo transcurrido
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Tiempo en segundos
        if seconds > 15:  # Si han pasado 15 segundos
            print(f"Fin del episodio. Recompensas totales: {len(crossed_checkpoints)}, Puntuación final: {vehicle.score}")
            run = False  # Terminar el episodio

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Dibujar el circuito
        window.blit(circuit_image, (0, 0))

        # Actualizar y dibujar el vehículo
        vehicle.update()
        vehicle.draw(window)

        # Verificar si el vehículo cruzó un checkpoint
        checkpoint = check_checkpoint(vehicle)
        if checkpoint and checkpoint not in crossed_checkpoints:
            crossed_checkpoints.add(checkpoint)  # Agregar a los checkpoints cruzados
            vehicle.score += 5  # Añadir 10 puntos por cada checkpoint
            print(f"Checkpoint cruzado! Recompensa total: {len(crossed_checkpoints)}, Puntuación: {vehicle.score}")

        # Verificar si el vehículo está fuera del circuito
        check_off_track(vehicle)

        # Actualizar la pantalla
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()