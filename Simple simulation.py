import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define agent classes
class Agent:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 2

    def move_randomly(self):
        self.x += random.choice([-1, 0, 1]) * self.speed
        self.y += random.choice([-1, 0, 1]) * self.speed
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

# Create agents
sheep = [Agent(random.randint(100, 700), random.randint(100, 500), GREEN) for _ in range(10)]
llamas = [Agent(400, 300, WHITE)]
predators = [Agent(700, 300, RED)]

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw agents
    for s in sheep:
        s.move_randomly()
        s.draw()
    
    for l in llamas:
        l.draw()
    
    for p in predators:
        p.move_randomly()
        p.draw()

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
