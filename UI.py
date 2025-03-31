# Slider class to handle the individual sliders
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                x = max(self.rect.left, min(event.pos[0], self.rect.right))
                self.slider_rect.x = x - 10  # Adjust the slider position
                # Update the value based on the slider position
                self.value = self.min_val + (float(x - self.rect.left)) / self.width * (self.max_val - self.min_val)

class ControlScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        # Create sliders
        self.slider1 = Slider(WIDTH + 25, 60, 150.0, 20.0, 0.0, 3.0, 1.0)
        self.slider2 = Slider(WIDTH + 25, 110, 150.0, 20.0, 0.0, 1.0, 0.05)
        self.slider3 = Slider(WIDTH + 25, 160, 150.0, 20, 0, 200, 100)


    def draw(self):
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH, 0, WIDTH + 200, HEIGHT))  # right panel
        screen.blit(self.font.render("Sheep", True, WHITE), (WIDTH + 25, 10))
        # Draw sliders
        self.slider1.draw(screen)
        value_text1 = self.font.render(f"Max Speed: {self.slider1.value:.2f}", True, WHITE)
        screen.blit(value_text1, (self.slider1.rect.left, self.slider1.rect.top - 17))
        self.slider2.draw(screen)
        value_text2 = self.font.render(f"Max Force: {self.slider2.value:.2f}", True, WHITE)
        screen.blit(value_text2, (self.slider2.rect.left, self.slider2.rect.top - 17))
        self.slider3.draw(screen)
        value_text3 = self.font.render(f"Perception: {int(self.slider3.value)}", True, WHITE)
        screen.blit(value_text3, (self.slider3.rect.left, self.slider3.rect.top - 17))

        for event in pygame.event.get():
            self.slider1.handle_event(event)
            self.slider2.handle_event(event)
            self.slider3.handle_event(event)
        return {"sheep": {
            "max_speed": self.slider1.value,
            "max_force": self.slider2.value,
            "perception": self.slider3.value
        }}
