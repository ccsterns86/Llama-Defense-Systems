import pygame
import random
from Sheep import Sheep
from Llama import Llama
from Predator import Predator

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create agents
num_sheep = 10
sheep = [Sheep(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 50, screen, WIDTH, HEIGHT) for _ in range(num_sheep)]
llamas = [Llama(400, 300, 100, screen, WIDTH, HEIGHT)]
predators = [Predator(700, 300, 80, screen, WIDTH, HEIGHT)]

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw agents
    for s in sheep:
        s.flock(sheep)
        s.move()
        s.edges()
        s.draw()
    
    for l in llamas:
        l.draw()

    for p in predators:
        p.move()
        p.draw()

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
