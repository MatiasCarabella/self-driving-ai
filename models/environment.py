import os
import pygame
import math
from config import WINDOW_CONFIG, COLOR_CONFIG, FONT_CONFIG

class Environment:
    def __init__(self):
        # Attributes: Dimensions
        self.SCREEN_WIDTH = WINDOW_CONFIG["WIDTH"]
        self.SCREEN_HEIGHT = WINDOW_CONFIG["HEIGHT"]

        # Attributes: Colors
        self.ROAD_COLOR = COLOR_CONFIG["BLACK"]
        self.BACKGROUND_COLOR = COLOR_CONFIG["WHITE"]
        self.VEHICLE_COLOR = COLOR_CONFIG["RED"]
        self.SENSOR_COLOR = COLOR_CONFIG["GREEN"]
        self.START_COLOR = COLOR_CONFIG["YELLOW"]
        self.CHECKPOINT_COLOR = COLOR_CONFIG["GRAY"]
        self.TEXT_COLOR = COLOR_CONFIG["WHITE"]
        self.TEXTBOX_COLOR = COLOR_CONFIG["BLACK"]

        # Initialize PyGame
        pygame.init()

        # Font for score and timer text
        pygame.font.init()
        self.FONT_BIG = pygame.font.Font(None, FONT_CONFIG["BIG"])
        self.FONT_SMALL = pygame.font.Font(None, FONT_CONFIG["SMALL"])

        # Configure the PyGame window
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Self Driving AI")

        # Get the absolute path of the directory where the .py file is running
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        circuit_image_path = os.path.join(parent_directory, "assets/images/circuit_2.png")

        # Load the circuit image from the relative path
        self.CIRCUIT_IMAGE = pygame.image.load(circuit_image_path).convert()
        self.CIRCUIT_IMAGE = pygame.transform.scale(self.CIRCUIT_IMAGE, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def find_start_position(self):
        """Find the first pixel with the start color and determine the initial direction."""
        for y in range(self.CIRCUIT_IMAGE.get_height()):
            for x in range(self.CIRCUIT_IMAGE.get_width()):
                if self.CIRCUIT_IMAGE.get_at((x, y)) == self.START_COLOR:
                    # Look for the road direction
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.CIRCUIT_IMAGE.get_width() and 0 <= ny < self.CIRCUIT_IMAGE.get_height():
                            if self.CIRCUIT_IMAGE.get_at((nx, ny)) == self.ROAD_COLOR:
                                # Calculate the initial angle
                                angle = math.degrees(math.atan2(-dy, dx))
                                return x, y, angle
        return None

    def draw_circuit(self):
        """Draw the circuit image onto the window."""
        self.window.blit(self.CIRCUIT_IMAGE, (0, 0))

    def clear_screen(self):
        """Clear the screen with the background color."""
        self.window.fill(self.BACKGROUND_COLOR)

    def draw_hud(self, vehicle, remaining_time):
        """Draw the entire HUD (Head-Up Display)."""
        self.draw_score(vehicle.score)
        self.draw_timer(remaining_time)
        self.draw_speed(vehicle.speed)
        self.draw_sensor_values(vehicle.sensors)
        is_on_track = vehicle.check_road_status(vehicle.x, vehicle.y) != "completely_off"
        self.draw_vehicle_status(is_on_track, vehicle.angle)

    def draw_score(self, vehicle_score):
        """Draw the score in the top-left corner."""
        score_text = self.FONT_BIG.render(f"Score: {vehicle_score}", True, self.TEXT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (score_rect.left - 5, score_rect.top - 5, 
                                         score_rect.width + 10, score_rect.height + 10))
        self.window.blit(score_text, score_rect)

    def draw_timer(self, remaining_time):
        """Draw the timer in the top-right corner."""
        timer_text = self.FONT_BIG.render(f"Time: {remaining_time:.1f}", True, self.TEXT_COLOR)
        timer_rect = timer_text.get_rect()
        timer_rect.topright = (self.SCREEN_WIDTH - 10, 10)
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (timer_rect.left - 5, timer_rect.top - 5, 
                                         timer_rect.width + 10, timer_rect.height + 10))
        self.window.blit(timer_text, timer_rect)

    def draw_speed(self, vehicle_speed):
        """Draw the current speed of the vehicle in the bottom-right corner."""
        speed_text = self.FONT_BIG.render(f"Speed: {vehicle_speed:.1f}", True, self.TEXT_COLOR)
        speed_rect = speed_text.get_rect()
        speed_rect.bottomright = (self.SCREEN_WIDTH - 10, self.SCREEN_HEIGHT - 10)
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (speed_rect.left - 5, speed_rect.top - 5, 
                                            speed_rect.width + 10, speed_rect.height + 10))
        self.window.blit(speed_text, speed_rect)

    def draw_sensor_values(self, vehicle_sensors):
        """Draw the sensor values in the bottom-right corner, just above the speed indicator."""
        sensor_texts = [f"Sensor {i+1}: {sensor.distance:.1f}" for i, sensor in enumerate(vehicle_sensors)]
        sensor_texts.reverse()  # Reverse the order of the sensor values

        base_x = self.SCREEN_WIDTH - 10
        base_y = self.SCREEN_HEIGHT - 50  # Located just above the speed indicator

        for i, sensor_text in enumerate(sensor_texts):
            text_surface = self.FONT_SMALL.render(sensor_text, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect()
            text_rect.bottomright = (base_x, base_y - i * 20)  # Place the text in order
            pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (text_rect.left - 5, text_rect.top - 5,
                                                            text_rect.width + 10, text_rect.height + 10))
            self.window.blit(text_surface, text_rect)

    def draw_vehicle_status(self, is_on_track, vehicle_angle):
        """Draw the vehicle's on-track status and current angle in the bottom-right corner."""
        status_text = "On Track: " + ("Yes" if is_on_track else "No")
        angle_text = f"Angle: {vehicle_angle:.1f}°"

        base_x = self.SCREEN_WIDTH - 10  # Position from the right
        base_y = self.SCREEN_HEIGHT - 178  # Positioned above the sensor info

        # Draw the on-track status
        status_surface = self.FONT_SMALL.render(status_text, True, self.TEXT_COLOR)
        status_rect = status_surface.get_rect()
        status_rect.bottomright = (base_x, base_y)
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (status_rect.left - 5, status_rect.top - 5,
                                                            status_rect.width + 10, status_rect.height + 10))
        self.window.blit(status_surface, status_rect)

        # Draw the vehicle angle
        angle_surface = self.FONT_SMALL.render(angle_text, True, self.TEXT_COLOR)
        angle_rect = angle_surface.get_rect()
        angle_rect.bottomright = (base_x, base_y + 20)  # Position below the status text
        pygame.draw.rect(self.window, self.TEXTBOX_COLOR, (angle_rect.left - 5, angle_rect.top - 5,
                                                            angle_rect.width + 10, angle_rect.height + 10))
        self.window.blit(angle_surface, angle_rect)

