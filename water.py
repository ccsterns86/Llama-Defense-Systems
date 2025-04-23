import pygame

class Water:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 100, 255), (self.x, self.y), self.radius)

    def contains(self, pos):
        dx = self.x - pos[0]
        dy = self.y - pos[1]
        return dx*dx + dy*dy <= self.radius * self.radius