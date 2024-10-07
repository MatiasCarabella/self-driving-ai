import pygame
import math
import time
from sensor import Sensor
from checkpoint import Checkpoint
from environment import Environment
from config import VEHICLE_CONFIG, COLOR_CONFIG

environment = Environment()

# Class representing the vehicle
class Vehicle:
    def __init__(self, x, y, initial_angle):
        """Initialize the vehicle with position, size, speed, and sensors."""
        self.x = x
        self.y = y
        self.angle = self.normalize_angle(initial_angle)
        self.initial_x = x  # Store initial position
        self.initial_y = y  # Store initial position
        self.initial_angle = self.angle
        self.width = VEHICLE_CONFIG["WIDTH"]
        self.height = VEHICLE_CONFIG["HEIGHT"]
        self.speed = 0  # Initial speed
        self.max_speed = VEHICLE_CONFIG["MAX_SPEED"]
        self.max_speed_partially_off = VEHICLE_CONFIG["MAX_SPEED_PARTIALLY_OFF"]
        self.max_speed_completely_off = VEHICLE_CONFIG["MAX_SPEED_COMPLETELY_OFF"]
        self.acceleration = VEHICLE_CONFIG["ACCELERATION"]
        self.desacceleration = VEHICLE_CONFIG["DESACCELERATION"]
        self.rotation_speed = VEHICLE_CONFIG["ROTATION_SPEED"]
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(environment.VEHICLE_COLOR)
        self.sensors = [
            Sensor(self, -90, 150),
            Sensor(self, -45, 150),
            Sensor(self, 0, 250),
            Sensor(self, 45, 150),
            Sensor(self, 90, 150)
        ]  # List of sensors (rays) with distances
        self.score = 0  # Initial score
        self.last_checkpoint = None  # Last checkpoint crossed
        self.last_penalty_time = time.time()  # Time of last penalty
        self.last_speed_check_time = time.time()  # Time of last speed check

    def reset(self):
        """Reset the vehicle to its initial state."""
        self.x = self.initial_x  # Reset initial position
        self.y = self.initial_y
        self.angle = self.initial_angle  # Reset initial angle
        self.speed = 0  # Reset initial speed
        self.score = 0  # Reset score
        self.last_checkpoint = None  # Reset last checkpoint crossed
        self.last_penalty_time = time.time()  # Reset penalty time

    def draw(self, window):
        """Draw the vehicle and its sensors."""
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        window.blit(rotated_image, new_rect.topleft)

        # Draw sensors
        for sensor in self.sensors:
            sensor.draw(window)

    def get_state(self):
        """Get the current state of the vehicle."""
        road_status = self.check_road_status(self.x, self.y)
        return (
            1 if road_status != "completely_off" else 0,
            int(self.speed),
            int(self.angle),
        ) + tuple(int(sensor.distance / 10) for sensor in self.sensors)

    def normalize_angle(self, angle):
        """Normalize the angle to be between 0 and 360 degrees."""
        return angle % 360

    def update_angle(self, delta):
        """Update the angle, ensuring it stays between 0 and 360 degrees."""
        self.angle = self.normalize_angle(self.angle + delta)

    def update_manual(self):
        """Update the vehicle based on manual control."""
        self.handle_input()
        self.update_position()
        self.update_sensors()

    def update_from_agent(self, action):
        """Update the vehicle based on the agent's action."""
        self.handle_agent_action(action)
        self.update_position()
        self.update_sensors()

    def handle_input(self):
        """Handle user input and update speed and angle."""
        keys = pygame.key.get_pressed()

        # Handle acceleration
        if keys[pygame.K_UP]:
            if self.speed < self.max_speed:
                self.speed += self.acceleration
        elif keys[pygame.K_DOWN]:
            pass  # The agent cannot brake
        else:
            self.speed *= self.desacceleration  # Natural deceleration

        # Handle rotation (modified)
        rotation = 0
        if keys[pygame.K_LEFT]:
            rotation = self.rotation_speed * (self.speed / self.max_speed)
        if keys[pygame.K_RIGHT]:
            rotation = -self.rotation_speed * (self.speed / self.max_speed)
        self.update_angle(rotation)

    def handle_agent_action(self, action):
        """Interpret the agent's action."""
        if action == 0:  # Accelerate
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif action == 1:  # Turn left
            self.update_angle(self.rotation_speed * (self.speed / self.max_speed))
        elif action == 2:  # Turn right
            self.update_angle(-self.rotation_speed * (self.speed / self.max_speed))
        elif action == 3:  # Do nothing
            self.speed *= self.desacceleration

    def update_position(self):
        """Update the vehicle's position based on its speed and angle.
        Return True if the vehicle collides with the window boundaries, False otherwise."""
        rad_angle = math.radians(self.angle)
        new_x = self.x + self.speed * math.cos(rad_angle)
        new_y = self.y - self.speed * math.sin(rad_angle)

        # Check if within window boundaries
        if new_x < self.width / 2 or new_x > environment.SCREEN_WIDTH - self.width / 2 or \
        new_y < self.height / 2 or new_y > environment.SCREEN_HEIGHT - self.height / 2:
            return True  # Collides with window boundaries

        # Check vehicle's road status
        road_status = self.check_road_status(new_x, new_y)

        if road_status == "on_road":
            self.x = new_x
            self.y = new_y
            self.max_speed = 6  # Reset max speed when back on road
            self.speed = min(self.speed, self.max_speed)  # Ensure speed does not exceed max
        elif road_status == "partially_off":
            self.max_speed = self.max_speed_partially_off
            if self.speed > self.max_speed_partially_off:
                self.speed *= self.desacceleration  # Keep speed within limits
            self.x = new_x
            self.y = new_y
        elif road_status == "completely_off":
            self.max_speed = self.max_speed_completely_off
            if self.speed > self.max_speed_completely_off:
                self.speed *= self.desacceleration  # Keep speed within limits
            self.x = new_x
            self.y = new_y

        return False  # No collision with boundaries

    def check_road_status(self, x, y):
        """Determine if the vehicle is on the road, partially off, or completely off."""
        rect = pygame.Rect(x - self.width / 2, y - self.height / 2, self.width, self.height)
        rotated_rect = self.get_rotated_vertices(rect)

        # Count corners that are on the road
        on_road_count = 0
        total_corners = len(rotated_rect)

        for vertex in rotated_rect:
            if self.is_on_road(vertex[0], vertex[1]):
                on_road_count += 1

        # Determine vehicle status based on how many corners are on the road
        if on_road_count == total_corners:
            return "on_road"  # Fully on the road
        elif on_road_count > 0:
            return "partially_off"  # Partially off the road
        else:
            return "completely_off"  # Completely off the road

    def get_rotated_vertices(self, rect):
        """Get the vertices of the vehicle's rotated rectangle."""
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
        """Check if a given position is on the road."""
        if 0 <= x < environment.SCREEN_WIDTH and 0 <= y < environment.SCREEN_HEIGHT:
            color_at_position = environment.CIRCUIT_IMAGE.get_at((int(x), int(y)))
            return color_at_position in [environment.ROAD_COLOR, environment.CHECKPOINT_COLOR, environment.START_COLOR]
        return False

    def update_sensors(self):
        """Update all the vehicle's sensors."""
        for sensor in self.sensors:
            sensor.update(environment)

    def update_score(self, delta):
        """Update the score and round it to one decimal."""
        self.score += delta
        self.score = round(self.score, 1)  # Round the score to one decimal
    
    def check_checkpoint(self, current_time, checkpoints):
        """Check if the vehicle crossed an active checkpoint and return the reward."""
        radius = 2  # Detection radius
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:  # Circular area
                    check_x = int(self.x + dx)
                    check_y = int(self.y + dy)
                    if 0 <= check_x < environment.SCREEN_WIDTH and 0 <= check_y < environment.SCREEN_HEIGHT:
                        color_at_position = environment.CIRCUIT_IMAGE.get_at((check_x, check_y))
                        if color_at_position == environment.CHECKPOINT_COLOR:  # Check if it is the checkpoint color
                            position = (check_x, check_y)
                            # Check if the current checkpoint is the same as the last crossed
                            if position in checkpoints and position == self.last_checkpoint:
                                return 0  # Do not reward if it's the same checkpoint
                            
                            if position in checkpoints:
                                checkpoint = checkpoints[position]
                                if checkpoint.is_active(current_time):
                                    checkpoint.last_crossed = current_time
                                    self.last_checkpoint = position  # Update last crossed checkpoint
                                    self.update_score(10)  # Increase score for crossing a checkpoint
                                    return 10  # Return the reward for crossing the checkpoint
                            else:
                                # New checkpoint detected
                                checkpoints[position] = Checkpoint(position)
                                checkpoints[position].last_crossed = current_time
                                self.last_checkpoint = position  # Save the new checkpoint crossed
                                self.update_score(10)  # Increase score for crossing a new checkpoint
                                return 10  # Return the reward for crossing a new checkpoint
        return 0  # No checkpoint crossed, return 0

    def check_off_track(self):
        """Check if the vehicle is off the circuit and return the penalty."""
        current_time = time.time()
        if current_time - self.last_penalty_time >= 0.25:  # Delay of 0.25 seconds
            road_status = self.check_road_status(self.x, self.y)
            
            if road_status != "on_road":
                # Determine penalty based on how far off the road the vehicle is
                penalty = -0.5 if road_status == "partially_off" else -1  # -0.5 for partial off, -1 for total
                self.update_score(penalty)  # Update score with penalty
                self.last_penalty_time = current_time  # Update the last penalty time
                return penalty  # Return the penalty
        return 0  # No penalty if on road or not enough time has passed

    def check_speed(self):
        """Check the vehicle's speed and return a reward proportional to the speed, with delay."""
        current_time = time.time()

        # Check if enough time has passed since the last speed check
        if current_time - self.last_speed_check_time >= 0.25:
            self.last_speed_check_time = current_time  # Update last speed check time

            reward = 0
            
            if self.speed >= 6:  # Highest reward for speed >= 6
                reward = 9
            elif self.speed >= 3:  # Medium reward for speed >= 3
                reward = 3
            elif self.speed >= 1.5:  # Default reward for speed > 1.5
                reward = 2
            elif self.speed >= 0.5:  # No reward for speed > 0.5
                reward = 0
            else:  # Penalize for no speed (below 0.5)
                reward = -1

            self.update_score(reward)  # Update the vehicle's score based on the reward
            return reward  # Return the reward

        return 0  # If not enough time has passed, return 0 as reward

