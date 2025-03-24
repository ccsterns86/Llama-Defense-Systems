import random
import pygame

# Define agent classes
class Agent:
    def __init__(self, x, y, color, screen, WIDTH, HEIGHT):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 2
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def move(self):
        self.x += random.choice([-1, 0, 1]) * self.speed
        self.y += random.choice([-1, 0, 1]) * self.speed
        self.x = max(0, min(self.WIDTH, self.x))
        self.y = max(0, min(self.HEIGHT, self.y))

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 10)