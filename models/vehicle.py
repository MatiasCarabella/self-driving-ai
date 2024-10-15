import math
import time
import pygame
from models.sensor import Sensor
from models.checkpoint import Checkpoint
from config import VEHICLE_CONFIG

class Vehicle:
    def __init__(self, environment):
        self.environment = environment
        start_info = self.environment.find_start_position()
        if start_info is None:
            raise ValueError("Could not find a valid starting position on the circuit.")
        
        self.initial_position = (start_info[0], start_info[1])
        self.initial_angle = self.normalize_angle(start_info[2])
        
        self.width = VEHICLE_CONFIG["WIDTH"]
        self.height = VEHICLE_CONFIG["HEIGHT"]
        self.max_speed = VEHICLE_CONFIG["MAX_SPEED"]
        self.max_speed_partially_off = VEHICLE_CONFIG["MAX_SPEED_PARTIALLY_OFF"]
        self.max_speed_completely_off = VEHICLE_CONFIG["MAX_SPEED_COMPLETELY_OFF"]
        self.acceleration = VEHICLE_CONFIG["ACCELERATION"]
        self.deceleration = VEHICLE_CONFIG["DESACCELERATION"]
        self.rotation_speed = VEHICLE_CONFIG["ROTATION_SPEED"]
        
        self.image = self._create_image()
        self.sensors = self._create_sensors()
        
        self.reset()

    def reset(self):
        """Reset the vehicle to its initial state."""
        self.x, self.y = self.initial_position
        self.angle = self.initial_angle
        self.speed = 0
        self.score = 0
        self.collided = False
        self.last_checkpoint = None
        self.last_road_check_time = time.time()
        self.last_speed_check_time = time.time()

    def _create_image(self):
        """Create the vehicle's image."""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        image.fill(self.environment.VEHICLE_COLOR)
        return image

    def _create_sensors(self):
        """Create the vehicle's sensors."""
        return [
            Sensor(self, -90, 100),
            Sensor(self, -45, 150),
            Sensor(self, 0, 200),
            Sensor(self, 45, 150),
            Sensor(self, 90, 100)
        ]

    def draw(self, window):
        """Draw the vehicle and its sensors on the window."""
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        window.blit(rotated_image, new_rect.topleft)
        for sensor in self.sensors:
            sensor.draw(window)

    def get_state(self):
        """Get the current state of the vehicle."""
        return (
            int(self.speed),
        ) + tuple(int(sensor.distance / 10) for sensor in self.sensors)

    @staticmethod
    def normalize_angle(angle):
        """Normalize the angle to be between 0 and 359."""
        return angle % 360

    def update_angle(self, delta):
        """Update the vehicle's angle."""
        self.angle = self.normalize_angle(self.angle + delta)

    @staticmethod
    def discretize_angle(angle):
        """Discretize the angle into 8 directions."""
        return int(angle // 45)

    def handle_manual_input(self):
        """Handle manual input for the vehicle."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.accelerate()
        else:
            self.decelerate()
        
        if keys[pygame.K_LEFT]:
            self.rotate(self.rotation_speed)
        elif keys[pygame.K_RIGHT]:
            self.rotate(-self.rotation_speed)
        
        self.update()

    def handle_agent_action(self, action):
        """Handle agent's action for the vehicle."""
        if action == 0:
            self.accelerate()
        elif action == 1:
            self.rotate(self.rotation_speed)
        elif action == 2:
            self.rotate(-self.rotation_speed)
        else:
            self.decelerate()
        
        self.update()

    def update(self):
        """Update the vehicle's state."""
        self.update_position()
        self.update_sensors()
        self.check_collision(VEHICLE_CONFIG["COLLISION_TYPE"])

    def accelerate(self):
        """Accelerate the vehicle."""
        self.speed = min(self.speed + self.acceleration, self.max_speed)

    def decelerate(self):
        """Decelerate the vehicle."""
        self.speed *= self.deceleration

    def rotate(self, rotation):
        """Rotate the vehicle."""
        self.update_angle(rotation * (self.speed / self.max_speed))

    def update_position(self):
        """Update the vehicle's position based on its speed and angle."""
        rad_angle = math.radians(self.angle)
        new_x = self.x + self.speed * math.cos(rad_angle)
        new_y = self.y - self.speed * math.sin(rad_angle)
        
        road_status = self.check_road_status(new_x, new_y)
        self.adjust_speed_and_position(road_status, new_x, new_y)

    def adjust_speed_and_position(self, road_status, new_x, new_y):
        """Adjust the vehicle's speed and position based on its road status."""
        if road_status == "on_road":
            self.max_speed = VEHICLE_CONFIG["MAX_SPEED"]
        elif road_status == "partially_off":
            self.max_speed = self.max_speed_partially_off
        else:
            self.max_speed = self.max_speed_completely_off
        
        self.speed = min(self.speed, self.max_speed)
        self.x, self.y = new_x, new_y

    def check_collision(self, check_type="WINDOW"):
        """Check if the vehicle has collided with the boundaries."""
        if check_type == "WINDOW":
            self.collided = not (self.width / 2 < self.x < self.environment.SCREEN_WIDTH - self.width / 2 and
                                 self.height / 2 < self.y < self.environment.SCREEN_HEIGHT - self.height / 2)
        elif check_type == "CIRCUIT":
            self.collided = self.check_road_status(self.x, self.y) != "on_road"

    def check_road_status(self, x, y):
        """Check the road status at the given position."""
        rotated_rect = self.get_rotated_vertices(pygame.Rect(x - self.width / 2, y - self.height / 2, self.width, self.height))
        on_road_count = sum(1 for vertex in rotated_rect if self.is_on_road(*vertex))
        
        if on_road_count == len(rotated_rect):
            return "on_road"
        elif on_road_count > 0:
            return "partially_off"
        return "completely_off"

    def get_rotated_vertices(self, rect):
        """Get the rotated vertices of the vehicle's rectangle."""
        rad_angle = math.radians(self.angle)
        cx, cy = rect.center
        corners = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
        return [(cx + (x - cx) * math.cos(rad_angle) - (y - cy) * math.sin(rad_angle),
                 cy + (x - cx) * math.sin(rad_angle) + (y - cy) * math.cos(rad_angle))
                for x, y in corners]

    def is_on_road(self, x, y):
        """Check if the given position is on the road."""
        if 0 <= x < self.environment.SCREEN_WIDTH and 0 <= y < self.environment.SCREEN_HEIGHT:
            color_at_position = self.environment.CIRCUIT_IMAGE.get_at((int(x), int(y)))
            return color_at_position in [self.environment.ROAD_COLOR, self.environment.CHECKPOINT_COLOR, self.environment.START_COLOR]
        return False

    def update_sensors(self):
        """Update the vehicle's sensors."""
        for sensor in self.sensors:
            sensor.update(self.environment)

    def update_score(self, delta):
        """Update the vehicle's score."""
        self.score = round(self.score + delta, 1)

    def check_checkpoint(self, current_time, checkpoints):
        """Check if the vehicle has reached a checkpoint."""
        radius = 2
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    check_x, check_y = int(self.x + dx), int(self.y + dy)
                    if self.is_valid_position(check_x, check_y):
                        color_at_position = self.environment.CIRCUIT_IMAGE.get_at((check_x, check_y))
                        if color_at_position == self.environment.CHECKPOINT_COLOR:
                            position = (check_x, check_y)
                            if position == self.last_checkpoint:
                                return 0
                            
                            if position in checkpoints:
                                checkpoint = checkpoints[position]
                                if checkpoint.is_active(current_time):
                                    checkpoint.last_crossed = current_time
                                    self.last_checkpoint = position
                                    return 10
                            else:
                                checkpoints[position] = Checkpoint(position)
                                checkpoints[position].last_crossed = current_time
                                self.last_checkpoint = position
                                return 10
        return 0

    def is_valid_position(self, x, y):
        """Check if the given position is within the screen boundaries."""
        return 0 <= x < self.environment.SCREEN_WIDTH and 0 <= y < self.environment.SCREEN_HEIGHT

    def reward_road(self):
        """Calculate the reward based on the vehicle's position on the road."""
        current_time = time.time()
        if current_time - self.last_road_check_time >= 0.25:
            road_status = self.check_road_status(self.x, self.y)
            self.last_road_check_time = current_time
            
            if road_status == "on_road":
                return 0.5
            return -0.5 if road_status == "partially_off" else -1
        return 0

    def reward_speed(self):
        """Calculate the reward based on the vehicle's speed."""
        return round(self.speed / 6, 1)
    
    def reward_distance(self):
        """
        Reward the agent for maintaining distance from the track edges.
        Focuses on lateral sensors (indices 0, 1, 3, 4).
        """
        lateral_sensors = [self.sensors[i] for i in [0, 1, 3, 4]]
        min_distance = min(sensor.distance for sensor in lateral_sensors)
        
        # Normalize the minimum distance (assuming 50 is the maximum distance for lateral sensors)
        reward = min_distance / 100
        
        # Calculate the reward        
        return round(reward, 1)

    def calculate_reward(self):
        """Calculate the total reward for the vehicle's current state."""
        total_reward = 0
        total_reward += round(self.reward_speed() * self.reward_distance(), 1)
        
        if self.collided:
            total_reward -= 25

        self.update_score(total_reward)
        return total_reward