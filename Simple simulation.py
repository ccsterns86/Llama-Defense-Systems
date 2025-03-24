import pygame
import random


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define colors
GREEN = (0, 100, 50)


# Define agent classes
class Agent:
    def __init__(self, x, y, size, icon_path):
        self.icon = pygame.transform.scale(pygame.image.load(icon_path), (size, size))
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.x = x
        self.icon_rect.y = y
        self.speed = 1.1

    def move_randomly(self):
        self.icon_rect.x += random.choice([-1, 0, 1]) * self.speed
        self.icon_rect.y += random.choice([-1, 0, 1]) * self.speed
        self.icon_rect.x = max(0, min(WIDTH, self.icon_rect.x))
        self.icon_rect.y = max(0, min(HEIGHT, self.icon_rect.y))

    def draw(self):
        screen.blit(self.icon, self.icon_rect)


# Create agents
sheep = [Agent(random.randint(100, 700), random.randint(100, 500), 50, "assets/noun-sheep-4744242.png") for _ in range(10)]
llamas = [Agent(400, 300, 100, "assets/noun-llama-7034038.png")]
predators = [Agent(700, 300, 80, "assets/noun-wolf-7401722.png")]

# Main loop
running = True
while running:
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw agents
    for s in sheep:
        s.move_randomly()
        s.draw()

    for l in llamas:
        l.move_randomly()
        l.draw()

    for p in predators:
        p.move_randomly()
        p.draw()

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
