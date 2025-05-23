import pygame
import random
import sys
from argparse import ArgumentParser
import UI
from Sheep import Sheep
from Llama import Llama
from Predator import Predator
from water import Water

# Get the passed in values
parser = ArgumentParser(prog="Llama Defense System")
parser.add_argument('--lcohesion', help='sets the cohesion value for the llama(s)', default=0.9, type=float)
parser.add_argument('--lseparation', help='sets the separation value for the llama(s)', default=0.2, type=float)
parser.add_argument('--ldefend', help='sets the defend value for the llama(s)', default=5.0, type=float)
parser.add_argument('--lperception', help='sets the perception value for the llama(s)', default=225.0, type=float)
parser.add_argument('--lnum', help='sets the number of llamas in the simulation', default=2, type=int)
parser.add_argument('--time', help='time the simulation should run in seconds', type=int)
parser.add_argument('--lpred', help='the number of predators', default=1, type=int)
parser.add_argument('--water_bodies', help='the number of bodies of water', default=0, type=int)

args = parser.parse_args()

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()


# background
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (UI.WIDTH, UI.HEIGHT))

# create control screen
control_screen = UI.ControlScreen(args)
font = pygame.font.SysFont(None, 24)
updated_values, running, reset = control_screen.draw()

# Bodies of water
min_radius=30
max_radius=80
water_bodies = []
for body in range(args.water_bodies):
    radius = random.randint(min_radius, max_radius)
    x = random.randint(radius, UI.WIDTH - radius)
    y = random.randint(radius, UI.HEIGHT - radius)
    water_bodies.append(Water(x,y,radius))

# Create agents
def spawn(num, Agent, size):
    agents = []
    for _ in range(num):
        while True:
            x = random.randint(100, UI.WIDTH - 100)
            y = random.randint(100, UI.HEIGHT - 100)
            if not any(w.contains((x,y)) for w in water_bodies):
                agents.append(Agent(x, y, size, UI.screen, UI.WIDTH, UI.HEIGHT))
                break
    return agents

num_sheep = updated_values['agents']['sheep']
sheep = spawn(num_sheep, Sheep, 50)
llamas = spawn(args.lnum, Llama, 100)
predators = [Predator(random.randint(100, UI.WIDTH - 100), random.randint(100, UI.HEIGHT - 100), 80, UI.screen, UI.WIDTH, UI.HEIGHT) for _ in range(args.lpred)]

# Main loop
running = True
while running:

    UI.screen.blit(background, (0, 0))

    # Draw water
    for water in water_bodies:
        water.draw(UI.screen)

    # Change number of agents 
    # Sheep
    desired_sheep = updated_values["agents"]["sheep"]
    if len(sheep) < desired_sheep:
        for _ in range(desired_sheep - len(sheep)):
            sheep.append(Sheep(random.randint(100, UI.WIDTH - 100), random.randint(100, UI.HEIGHT - 100), 50, UI.screen, UI.WIDTH, UI.HEIGHT))
    elif len(sheep) > desired_sheep:
        sheep = sheep[:desired_sheep]

    # Llamas
    desired_llamas = updated_values["agents"]["llamas"]
    if len(llamas) < desired_llamas:
        for _ in range(desired_llamas - len(llamas)):
            llamas.append(Llama(random.randint(100, UI.WIDTH - 100), random.randint(100, UI.HEIGHT - 100), 100, UI.screen, UI.WIDTH, UI.HEIGHT))
    elif len(llamas) > desired_llamas:
        llamas = llamas[:desired_llamas]

    # Predators
    desired_predators = updated_values["agents"]["predators"]
    if len(predators) < desired_predators:
        for _ in range(desired_predators - len(predators)):
            predators.append(Predator(random.randint(100, UI.WIDTH - 100), random.randint(100, UI.HEIGHT - 100), 80, UI.screen, UI.WIDTH, UI.HEIGHT))
    elif len(predators) > desired_predators:
        predators = predators[:desired_predators]
    
    # Move and draw agents
    alive_sheep_count = 0
    for s in sheep:
        s.update_values(updated_values["sheep"])
        s.flock(sheep, predators)
        s.move(predators, water_bodies)
        s.edges(water_bodies)
        if s.is_alive:
            alive_sheep_count += 1
        s.draw()

    for l in llamas:
        l.update_values(updated_values["llama"])
        l.flock(sheep, llamas, predators)
        l.move(predators, water_bodies)
        l.edges(water_bodies)
        l.draw()

    predators_alive = False
    if pygame.time.get_ticks() > 3000: # Wait 3 seconds for the sheep to flock
        for i, p in enumerate(predators):
            if p.is_alive:
                predators_alive = True
                if not p.is_spawned:
                    p.respawn()
                    p.is_spawned = True
                p.update_values(updated_values["predator"])
                p.flock(sheep, llamas, predators)
                p.move(llamas, water_bodies)
                p.attack(sheep)
                p.check_health(llamas)
                p.edges(water_bodies)
            control_screen.set_display_vals(i, p.health)
            p.draw()
    else: predators_alive=True

    # Display sheep counter
    updated_values, running, reset = control_screen.draw()
    UI.screen.blit(font.render(f"{alive_sheep_count} remaining sheep", True, UI.WHITE), (UI.WIDTH + 25, UI.HEIGHT - 20))

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

    # Check timing on the simulation
    if (args.time and pygame.time.get_ticks() > (args.time * 1000)) or (args.time and not predators_alive):
        running = False
        print(f"Sheep Left: {alive_sheep_count}")

    # Check if we want to reset:
    if reset:
        sheep = []
        llamas = []
        predators = []

pygame.quit()
