import pygame
import random

import UI
from Sheep import Sheep
from Llama import Llama
from Predator import Predator

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Create agents
num_sheep = 100
sheep = [
    Sheep(random.randint(100, UI.WIDTH - 100), random.randint(100, UI.HEIGHT - 100), 50, UI.screen, UI.WIDTH, UI.HEIGHT)
    for _ in range(num_sheep)]
llamas = [Llama(400, 300, 100, UI.screen, UI.WIDTH, UI.HEIGHT)]
predators = [Predator(700, 300, 80, UI.screen, UI.WIDTH, UI.HEIGHT)]
preadators_spawned = False

# background
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (UI.WIDTH, UI.HEIGHT))

# create control screen
control_screen = UI.ControlScreen()
font = pygame.font.SysFont(None, 24)
updated_values, running = control_screen.draw()

# Main loop
running = True
while running:

    UI.screen.blit(background, (0, 0))
    

    # Move and draw agents
    alive_sheep_count = 0
    for s in sheep:
        s.update_values(updated_values["sheep"])
        s.flock(sheep, predators)
        s.move(predators)
        s.edges()
        if s.is_alive:
            alive_sheep_count += 1
        s.draw()

    for l in llamas:
        l.update_values(updated_values["llama"])
        l.flock(sheep, predators)
        l.move(predators)
        l.edges()
        l.draw()

    for p in predators:
        if pygame.time.get_ticks() > 3000: # Wait 3 seconds for the sheep to flock
            if not preadators_spawned:
                p.respawn()
                preadators_spawned = True
            p.update_values(updated_values["predator"])
            control_screen.set_display_vals(p.health)
            p.flock(sheep, llamas)
            p.move(llamas)
            p.attack(sheep)
            p.check_health(llamas)
            p.edges()
            p.draw()

    # Display sheep counter
    updated_values, running = control_screen.draw()
    UI.screen.blit(font.render(f"{alive_sheep_count} remaining sheep", True, UI.WHITE), (UI.WIDTH + 25, UI.HEIGHT - 20))

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
