import pygame
import math
import time
from checkpoint import Checkpoint
from environment import Environment
from config import VEHICLE_CONFIG

environment = Environment()

# Clase que representa el vehículo
class Vehicle:
    def __init__(self, x, y, initial_angle):
        self.x = x
        self.y = y
        self.angle = initial_angle
        self.initial_x = x  # Guardar la posición inicial
        self.initial_y = y  # Guardar la posición inicial
        self.initial_angle = initial_angle  # Guardar el ángulo inicial
        self.width = VEHICLE_CONFIG["WIDTH"]
        self.height = VEHICLE_CONFIG["HEIGHT"]
        self.speed = 0  # Velocidad inicial
        self.max_speed = VEHICLE_CONFIG["MAX_SPEED"]  
        self.max_speed_partially_off = VEHICLE_CONFIG["MAX_SPEED_PARTIALLY_OFF"]
        self.max_speed_completely_off = VEHICLE_CONFIG["MAX_SPEED_COMPLETELY_OFF"]
        self.acceleration = VEHICLE_CONFIG["ACCELERATION"]
        self.desacceleration = VEHICLE_CONFIG["DESACCELERATION"]
        self.rotation_speed = VEHICLE_CONFIG["ROTATION_SPEED"]
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(environment.VEHICLE_COLOR)
        self.sensors = []  # Lista de sensores (rayos) con distancia
        self.score = 0  # Puntuación inicial
        self.last_checkpoint = None  # Último checkpoint cruzado
        self.last_penalty_time = time.time()  # Tiempo de la última penalización
        self.last_speed_check_time = time.time()  # Tiempo de la última verificación de velocidad

    def reset(self):
        """Restablece el vehículo a su estado inicial."""
        self.x = self.initial_x  # Restablecer la posición inicial
        self.y = self.initial_y
        self.angle = self.initial_angle  # Restablecer el ángulo inicial
        self.speed = 0  # Restablecer la velocidad inicial
        self.sensors = []  # Limpiar los sensores
        self.score = 0  # Reiniciar la puntuación
        self.last_checkpoint = None  # Reiniciar el último checkpoint cruzado
        self.last_penalty_time = time.time()  # Reiniciar el tiempo de la última penalización

    def draw(self, window):
        # Rotar la imagen del vehículo sin cambiar sus dimensiones originales
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        window.blit(rotated_image, new_rect.topleft)

        # Dibujar los sensores
        for sensor, _ in self.sensors:
            pygame.draw.line(window, environment.SENSOR_COLOR, (self.x, self.y), sensor, 2)

    def update_manual(self):
        """Actualiza el vehículo basado en el control manual."""
        self.handle_input()
        self.update_position()
        self.update_sensors()

    def update_from_agent(self, action):
        """Actualiza el vehículo basado en la acción proporcionada por el agente."""
        self.handle_agent_action(action)
        self.update_position()
        self.update_sensors()

    def handle_input(self):
        """Maneja la entrada del usuario y actualiza velocidad y ángulo."""
        keys = pygame.key.get_pressed()

        # Manejar la aceleración
        if keys[pygame.K_UP]:
            if self.speed < self.max_speed:
                self.speed += self.acceleration
        elif keys[pygame.K_DOWN]:
            pass  # El agente no puede frenar
        else:
            self.speed *= self.desacceleration  # Desaceleración natural

        # Manejar la rotación
        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed * (self.speed / self.max_speed)
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed * (self.speed / self.max_speed)

    def handle_agent_action(self, action):
        """Interpreta la acción del agente."""
        if action == 0:  # Acelerar
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif action == 1:  # Girar izquierda
            self.angle += self.rotation_speed * (self.speed / self.max_speed)
        elif action == 2:  # Girar derecha
            self.angle -= self.rotation_speed * (self.speed / self.max_speed)
        elif action == 3:  # No hacer nada
            self.speed *= self.desacceleration

    def update_position(self):
        """Actualiza la posición del vehículo basada en su velocidad y ángulo."""
        rad_angle = math.radians(self.angle)
        new_x = self.x + self.speed * math.cos(rad_angle)
        new_y = self.y - self.speed * math.sin(rad_angle)

        # Comprobar el estado del vehículo en la carretera
        road_status = self.check_road_status(new_x, new_y)

        if road_status == "on_road":
            self.x = new_x
            self.y = new_y
            self.max_speed = 6  # Restablecer velocidad máxima al volver a la carretera
            self.speed = min(self.speed, self.max_speed)  # Asegurarse de que la velocidad no exceda el máximo
        elif road_status == "partially_off":
            self.max_speed = self.max_speed_partially_off
            if self.speed > self.max_speed_partially_off:
                self.speed *= self.desacceleration  # Mantener velocidad dentro de los límites
            self.x = new_x
            self.y = new_y
        elif road_status == "completely_off":
            self.max_speed = self.max_speed_completely_off
            if self.speed > self.max_speed_completely_off:
                self.speed *= self.desacceleration  # Mantener velocidad dentro de los límites
            self.x = new_x
            self.y = new_y

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
        if 0 <= x < environment.SCREEN_WIDTH and 0 <= y < environment.SCREEN_HEIGHT:
            color_at_position = environment.CIRCUIT_IMAGE.get_at((int(x), int(y)))
            return color_at_position in [environment.ROAD_COLOR, environment.CHECKPOINT_COLOR, environment.START_COLOR]
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

    def update_score(self, delta):
        """Actualiza el puntaje y lo redondea a un decimal."""
        self.score += delta
        self.score = round(self.score, 1)  # Redondear el score a un decimal
    
    # Función para verificar si el vehículo ha cruzado un checkpoint gris
    def check_checkpoint(self, current_time, checkpoints):
        """Verifica si el vehículo ha cruzado un checkpoint activo y devuelve la recompensa."""
        radius = 2  # Radio de detección
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:  # Área circular
                    check_x = int(self.x + dx)
                    check_y = int(self.y + dy)
                    if 0 <= check_x < environment.SCREEN_WIDTH and 0 <= check_y < environment.SCREEN_HEIGHT:
                        color_at_position = environment.CIRCUIT_IMAGE.get_at((check_x, check_y))
                        if color_at_position == environment.CHECKPOINT_COLOR:  # Comprobar si es gris
                            position = (check_x, check_y)
                            # Verificar que el checkpoint actual no sea el mismo que el último cruzado
                            if position in checkpoints and position == self.last_checkpoint:
                                return 0  # No recompensar si es el mismo checkpoint
                            
                            if position in checkpoints:
                                checkpoint = checkpoints[position]
                                if checkpoint.is_active(current_time):
                                    checkpoint.last_crossed = current_time
                                    self.last_checkpoint = position  # Actualizar el último checkpoint cruzado
                                    self.update_score(5)  # Aumentar la puntuación
                                    print(f"Checkpoint cruzado! Puntuación: {self.score}")
                                    return 5  # Devolver la recompensa
                            else:
                                checkpoints[position] = Checkpoint(position)
                                checkpoints[position].last_crossed = current_time
                                self.last_checkpoint = position  # Guardar nuevo checkpoint cruzado
                                self.update_score(5)  # Aumentar la puntuación
                                print(f"Nuevo checkpoint cruzado! Puntuación: {self.score}")
                                return 5  # Devolver la recompensa
        return 0  # No se cruzó ningún checkpoint

    def check_off_track(self):
        """Verifica si el vehículo está fuera del circuito y devuelve la penalización"""
        current_time = time.time()
        if current_time - self.last_penalty_time >= 0.25:  # Delay de 0.25 segundos
            road_status = self.check_road_status(self.x, self.y)
            
            if road_status != "on_road":
                penalty = -1 if road_status == "partially_off" else -2  # -1 para salida parcial, -2 para total
                self.update_score(penalty)
                self.last_penalty_time = current_time
                print(f"Penalización: {penalty}. Puntuación total: {self.score}")
                return penalty
        return 0  # No hay penalización si está en la carretera o si no ha pasado suficiente tiempo
    
    def check_speed(self):
        """Verifica la velocidad del vehículo y devuelve una recompensa proporcional a la velocidad, con delay."""
        current_time = time.time()
        
        # Comprobar si ha pasado el tiempo suficiente desde la última verificación
        if current_time - self.last_speed_check_time >= 0.25:
            self.last_speed_check_time = current_time  # Actualizar el tiempo de la última verificación
            
            if self.speed > 1:
                self.update_score(0.1)
                return 0.1 # Recompensa si la velocidad es mayor a 0.1
            else:
                self.update_score(-0.5)
                return -0.5  # Penalización si la velocidad es 0
        
        return 0  # Si no ha pasado el tiempo, devolver 0 como recompensa