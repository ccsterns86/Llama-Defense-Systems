import pygame
import random
import sys
from argparse import ArgumentParser
import UI
from Sheep import Sheep
from Llama import Llama
from Predator import Predator

# Get the passed in values
parser = ArgumentParser(prog="Llama Defense System")
parser.add_argument('--lcohesion', help='sets the cohesion value for the llama(s)', default=0.65, type=float)
parser.add_argument('--lseparation', help='sets the separation value for the llama(s)', default=0.74, type=float)
parser.add_argument('--ldefend', help='sets the defend value for the llama(s)', default=4.0, type=float)
parser.add_argument('--lperception', help='sets the perception value for the llama(s)', default=250.0, type=float)
parser.add_argument('--lnum', help='sets the number of llamas in the simulation', default=1, type=int)
parser.add_argument('--time', help='time the simulation should run in seconds', type=int)

args = parser.parse_args()

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Create agents
num_sheep = 100
num_llamas = 5
sheep = [
    Sheep(random.randint(100, UI.WIDTH - 100), random.randint(100, UI.HEIGHT - 100), 50, UI.screen, UI.WIDTH, UI.HEIGHT)
    for _ in range(num_sheep)]
llamas = [Llama(random.randint(100, UI.WIDTH - 100), random.randint(100, UI.HEIGHT - 100), 100, UI.screen, UI.WIDTH, UI.HEIGHT) for _ in range(num_llamas)]
predators = [Predator(700, 300, 80, UI.screen, UI.WIDTH, UI.HEIGHT)]
preadators_spawned = False

# background
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (UI.WIDTH, UI.HEIGHT))

# create control screen
control_screen = UI.ControlScreen(args)
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
        l.flock(sheep, llamas, predators)
        l.move(predators)
        l.edges()
        l.draw()

    for p in predators:
        if pygame.time.get_ticks() > 3000: # Wait 3 seconds for the sheep to flock
            if p.is_alive:
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

    # Check timing on the simulation
    if args.time and pygame.time.get_ticks() > (args.time * 1000):
        running = False
        print(f"Sheep Left: {alive_sheep_count}")

pygame.quit()
