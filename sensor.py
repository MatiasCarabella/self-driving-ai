import pygame
import math
from config import COLOR_CONFIG

class Sensor:
    def __init__(self, vehicle, angle_offset, length):
        self.vehicle = vehicle
        self.angle_offset = angle_offset
        self.length = length
        self.end_x = 0
        self.end_y = 0
        self.distance = 0
        self.is_on_road = False

    def update(self, environment):
        sensor_angle = math.radians(self.vehicle.angle + self.angle_offset)
        self.end_x = self.vehicle.x + self.length * math.cos(sensor_angle)
        self.end_y = self.vehicle.y - self.length * math.sin(sensor_angle)

        self.is_on_road = self.vehicle.is_on_road(self.vehicle.x, self.vehicle.y)
        self.distance = self._calculate_distance(environment)

    def _calculate_distance(self, environment):
        sensor_angle = math.radians(self.vehicle.angle + self.angle_offset)
        for d in range(int(self.length)):
            check_x = int(self.vehicle.x + d * math.cos(sensor_angle))
            check_y = int(self.vehicle.y - d * math.sin(sensor_angle))

            if 0 <= check_x < environment.SCREEN_WIDTH and 0 <= check_y < environment.SCREEN_HEIGHT:
                color_at_position = environment.CIRCUIT_IMAGE.get_at((check_x, check_y))
                
                if self.is_on_road:
                    if color_at_position not in [environment.ROAD_COLOR, environment.CHECKPOINT_COLOR, environment.START_COLOR]:
                        return d
                else:
                    if color_at_position in [environment.ROAD_COLOR, environment.CHECKPOINT_COLOR, environment.START_COLOR]:
                        return -d

        # Si el vehículo está en el circuito y no se encontraron colisiones, devolver la longitud máxima
        return self.length if self.is_on_road else 0

    def draw(self, window):
        pygame.draw.line(window, COLOR_CONFIG["GREEN"], (self.vehicle.x, self.vehicle.y), (self.end_x, self.end_y), 2)
        
        if self.distance != 0:
            obstacle_x = int(self.vehicle.x + abs(self.distance) * math.cos(math.radians(self.vehicle.angle + self.angle_offset)))
            obstacle_y = int(self.vehicle.y - abs(self.distance) * math.sin(math.radians(self.vehicle.angle + self.angle_offset)))
            color = COLOR_CONFIG["BLUE"] if self.is_on_road else COLOR_CONFIG["RED"]
            pygame.draw.circle(window, color, (obstacle_x, obstacle_y), 5)