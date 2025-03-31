import random
import pygame

# Define agent classes
class Agent:
    def __init__(self, x, y, size, icon_path, screen, WIDTH, HEIGHT):
        self.icon = pygame.transform.scale(pygame.image.load(icon_path), (size, size))
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.x = x
        self.icon_rect.y = y
        self.speed = 2
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def move(self, _):
        self.icon_rect.x += random.choice([-1, 0, 1]) * self.speed
        self.icon_rect.y += random.choice([-1, 0, 1]) * self.speed
        self.icon_rect.x = max(0, min(self.WIDTH, self.icon_rect.x))
        self.icon_rect.y = max(0, min(self.HEIGHT, self.icon_rect.y))

    def draw(self):
        self.screen.blit(self.icon, self.icon_rect)