# Handles UI Elements
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 100, 50)
RED = (255, 0, 0)

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))

# Sliders for value adjustment
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, current_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = current_val
        self.height = height
        self.width = width
        self.slider_rect = pygame.Rect(x + (self.value - self.min_val) / (self.max_val - self.min_val) * width - 10, y,
                                       20, height)
        self.dragging = False

    def draw(self, surface):
        # Draw the track
        pygame.draw.rect(surface, GRAY, self.rect)
        # Draw the slider
        pygame.draw.circle(surface, GREEN, (self.slider_rect.x + (self.height/2), self.slider_rect.y + (self.height/2)), self.height/2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.slider_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = max(self.rect.left, min(event.pos[0], self.rect.right))
            self.slider_rect.x = x - 10  # Adjust the slider position
            # Update the value based on the slider position
            self.value = self.min_val + (float(x - self.rect.left)) / self.width * (self.max_val - self.min_val)

# UI Controls
class ControlScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)

        slider_specs = [
            # (name, height, lowVal, highVal, presetVal)
            ("Alignment", 60, 0, 2.0, 0.3),
            ("Cohesion", 110, 0, 2.0, 0.65),
            ("Separation", 160, 0, 3.0, 3.0),
            ("Flee", 210, 0, 3.0, 2.0),
            ("Perception", 260, 0, 200, 55),
        ]

        self.sliders = [
            {"label": label, "slider": Slider(WIDTH + 25, y, 150, 20, min_val, max_val, default_val)}
            for label, y, min_val, max_val, default_val in slider_specs
        ]

    def draw(self):
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH, 0, WIDTH + 200, HEIGHT))  # right panel
        screen.blit(self.font.render("Sheep", True, WHITE), (WIDTH + 25, 10))

        # Draw sliders
        values = {}
        for slider_data in self.sliders:
            label, slider = slider_data["label"], slider_data["slider"]
            slider.draw(screen)
            value_text = self.font.render(f"{label}: {slider.value:.2f}", True, WHITE)
            screen.blit(value_text, (slider.rect.left, slider.rect.top - 17))
            values[label.lower()] = slider.value  # Store values in dictionary

        # Return all values to use for updates
        for event in pygame.event.get():
            for slider_data in self.sliders:
                slider_data["slider"].handle_event(event)
        
        return {"sheep": values}
