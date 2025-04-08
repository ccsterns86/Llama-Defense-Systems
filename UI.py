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
screen = pygame.display.set_mode((WIDTH + 400, HEIGHT))

# Sliders for value adjustment
class Slider:
    def __init__(self, label, x, y, width, height, min_val, max_val, current_val):
        self.font = pygame.font.SysFont(None, 18)
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = current_val
        self.height = height
        self.width = width
        self.slider_rect = pygame.Rect(x + (self.value - self.min_val) / (self.max_val - self.min_val) * width - 10, y,
                                       20, height)
        self.label = label
        self.dragging = False


    def draw(self, surface):
        value_text = self.font.render(f"{self.label}: {self.value:.2f}", True, WHITE)
        screen.blit(value_text, (self.rect.left, self.rect.top - 15))
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
    def __init__(self, args):
        self.font = pygame.font.SysFont(None, 24)
        self.slider_height = 15
        self.text_height = 15
        self.slider_spacing = self.slider_height + self.text_height + 10
        self.intra_species_sep = 100
        self.predators_health = {}
        self.game_running = True
        self.llama_vals = { "lcohesion": args.lcohesion, "lseparation": args.lseparation, 
            "ldefend": args.ldefend, "lperception": args.lperception }

        # Sheep sliders
        sheep_slider_specs = [
            # (name, lowVal, highVal, presetVal)
            ("Alignment", 0, 2.0, 0.23),
            ("Cohesion", 0, 2.0, 0.72),
            ("Separation", 0, 3.0, 3.0),
            ("Flee", 0, 3.0, 2.0),
            ("Perception", 0, 200, 55),
        ]
        self.sheep_sliders = [
            {"label": label, "slider": Slider(label, WIDTH + 25, 60 + (self.slider_spacing * i), 150, self.slider_height, min_val, max_val, default_val)}
            for i, (label, min_val, max_val, default_val) in enumerate(sheep_slider_specs)
        ]

        # Llama sliders
        start_point = (len(sheep_slider_specs)*self.slider_spacing) + self.intra_species_sep + (3 * self.text_height )
        llama_slider_specs = [
            # (name, lowVal, highVal, presetVal)
            ("Cohesion", 0, 2.0, self.llama_vals['lcohesion']),
            ("Separation", 0, 3.0, self.llama_vals['lseparation']),
            ("Defend", 0, 6.0, self.llama_vals['ldefend']),
            ("Perception", 0, 300, self.llama_vals['lperception']),
        ]
        self.llama_sliders = [
            {"label": label, "slider": Slider(label, WIDTH + 25, start_point + (self.slider_spacing * i), 150, self.slider_height, min_val, max_val, default_val)}
            for i, (label, min_val, max_val, default_val) in enumerate(llama_slider_specs)
        ]

        # Predator sliders
        predator_slider_specs = [
            # (name, lowVal, highVal, presetVal)
            ("Cohesion", 0, 2.0, 0.65),
            ("Flee", 0, 4.0, 2.0),
            ("Perception", 0, 300, 55),
            ("Separation", 0, 3, 1),
            ("Attack Time", 0, 200, 100),
            ("Pack Strength", 0, 10, 0),
        ]
        self.predator_sliders = [
            {"label": label,
             "slider": Slider(label, WIDTH + 225, 60 + (self.slider_spacing * i), 150, self.slider_height,
                              min_val, max_val, default_val)}
            for i, (label, min_val, max_val, default_val) in enumerate(predator_slider_specs)
        ]
    def set_display_vals(self, val_id, predator_health):
        self.predators_health[val_id] = predator_health

    def draw(self):
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH, 0, WIDTH + 400, HEIGHT))  # right panel
        screen.blit(self.font.render("Sheep", True, WHITE), (WIDTH + 25, 10))

        # Draw sliders
        sheep_values = {}
        for slider_data in self.sheep_sliders:
            label, slider = slider_data["label"], slider_data["slider"]
            slider.draw(screen)
            sheep_values[label.lower()] = slider.value  # Store values in dictionary

        screen.blit(self.font.render("Llama", True, WHITE), (WIDTH + 25, (len(self.sheep_sliders)*self.slider_spacing) + self.intra_species_sep))
        llama_values = {}
        for slider_data in self.llama_sliders:
            label, slider = slider_data["label"], slider_data["slider"]
            slider.draw(screen)
            llama_values[label.lower()] = slider.value  # Store values in dictionary

        screen.blit(self.font.render("Predator", True, WHITE), (WIDTH + 225, 10))
        predator_values = {}
        for slider_data in self.predator_sliders:
            label, slider = slider_data["label"], slider_data["slider"]
            slider.draw(screen)
            predator_values[label.lower()] = slider.value  # Store values in dictionary

        for i, health in zip(self.predators_health.keys(), self.predators_health.values()):
            screen.blit(self.font.render(f"#{i} Health {health}", True, WHITE), (WIDTH + 225, 280 + (20 * i)))

        # # Return all values to use for updates
        for event in pygame.event.get():
            for slider_data in self.sheep_sliders:
                slider_data["slider"].handle_event(event)
            for slider_data in self.llama_sliders:
                slider_data["slider"].handle_event(event)
            for slider_data in self.predator_sliders:
                slider_data["slider"].handle_event(event)
            if event.type == pygame.QUIT:
                self.game_running = False

        return {"sheep": sheep_values, "llama": llama_values, "predator": predator_values}, self.game_running
