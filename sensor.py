import pygame
import math
from config import COLOR_CONFIG

class Sensor:
    def __init__(self, vehicle, angle_offset, length):
        """
        Initialize the sensor attached to a vehicle.
        :param vehicle: The vehicle that this sensor is attached to
        :param angle_offset: The angle offset relative to the vehicle's orientation
        :param length: The maximum length or range of the sensor
        """
        self.vehicle = vehicle
        self.angle_offset = angle_offset
        self.length = length
        self.end_x = 0  # The X-coordinate of the sensor's endpoint
        self.end_y = 0  # The Y-coordinate of the sensor's endpoint
        self.distance = 0  # The calculated distance to the first obstacle
        self.is_on_road = False  # Whether the vehicle is on the road

    def update(self, environment):
        """
        Update the sensor's position and calculate the distance to the first obstacle.
        :param environment: The environment in which the vehicle and sensor operate
        """
        # Calculate the sensor angle based on the vehicle's orientation and offset
        sensor_angle = math.radians(self.vehicle.angle + self.angle_offset)
        
        # Update the sensor's endpoint coordinates
        self.end_x = self.vehicle.x + self.length * math.cos(sensor_angle)
        self.end_y = self.vehicle.y - self.length * math.sin(sensor_angle)

        # Check if the vehicle is currently on the road
        self.is_on_road = self.vehicle.is_on_road(self.vehicle.x, self.vehicle.y)
        
        # Calculate the distance from the sensor to the first detected obstacle
        self.distance = self._calculate_distance(environment)

    def _calculate_distance(self, environment):
        """
        Calculate the distance to the first obstacle the sensor detects.
        If the vehicle is on the road, it measures the distance to a non-road object.
        If the vehicle is off-road, it measures the distance to the road.
        :param environment: The environment to check for obstacles
        :return: The distance to the obstacle (positive if on road, negative if off road)
        """
        sensor_angle = math.radians(self.vehicle.angle + self.angle_offset)
        
        # Loop through the range of the sensor's length to check for obstacles
        for d in range(int(self.length)):
            check_x = int(self.vehicle.x + d * math.cos(sensor_angle))
            check_y = int(self.vehicle.y - d * math.sin(sensor_angle))

            # Ensure the check is within the environment's boundaries
            if 0 <= check_x < environment.SCREEN_WIDTH and 0 <= check_y < environment.SCREEN_HEIGHT:
                color_at_position = environment.CIRCUIT_IMAGE.get_at((check_x, check_y))

                # If the vehicle is on the road, detect the first non-road object
                if self.is_on_road:
                    if color_at_position not in [environment.ROAD_COLOR, environment.CHECKPOINT_COLOR, environment.START_COLOR]:
                        return d
                # If the vehicle is off-road, detect the distance to the road
                else:
                    if color_at_position in [environment.ROAD_COLOR, environment.CHECKPOINT_COLOR, environment.START_COLOR]:
                        return -d

        # If the sensor detects no obstacles, return the max length or 0 if off-road
        return self.length if self.is_on_road else 0

    def draw(self, window):
        """
        Draw the sensor line and the detected obstacle (if any) on the window.
        :param window: The PyGame window to draw on
        """
        # Draw the sensor line from the vehicle to the sensor's endpoint
        pygame.draw.line(window, COLOR_CONFIG["GREEN"], (self.vehicle.x, self.vehicle.y), (self.end_x, self.end_y), 2)
        
        # If an obstacle was detected, draw a circle at the obstacle's location
        if self.distance != 0:
            obstacle_x = int(self.vehicle.x + abs(self.distance) * math.cos(math.radians(self.vehicle.angle + self.angle_offset)))
            obstacle_y = int(self.vehicle.y - abs(self.distance) * math.sin(math.radians(self.vehicle.angle + self.angle_offset)))
            
            # Draw the obstacle in blue if on-road, red if off-road
            color = COLOR_CONFIG["BLUE"] if self.is_on_road else COLOR_CONFIG["RED"]
            pygame.draw.circle(window, color, (obstacle_x, obstacle_y), 5)
