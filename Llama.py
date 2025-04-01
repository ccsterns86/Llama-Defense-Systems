from Agent import Agent
import pygame
import random
import noise

WHITE = (255, 255, 255)

class Llama(Agent):
    def __init__(self, x, y, size, screen, WIDTH, HEIGHT):
        self.icon = pygame.transform.scale(pygame.image.load("assets/noun-llama-7034038.png"), (size, size))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 3
        self.max_force = 0.05
        self.perception_radius = 150
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.size = size
        self.noise_time = random.uniform(0, 1000)
        self.alignmentVal = 0.1
        self.cohesionVal = 0.4
        self.separationVal = 3.0
        self.defendVal = 2.0

    def update_values(self, values):
        for item in values:
            if item == "cohesion":
                self.cohesionVal = values[item]
            elif item == "separation":
                self.separationVal = values[item]
            elif item == "defend":
                self.fleeVal = values[item]
            elif item == "perception":
                self.perception_radius = values[item]

    def move(self, predators):
        self.wander()

        danger_zone = self.perception_radius / 2
        alert_zone = self.perception_radius * 1.5

        closest_predator = float("inf")

        for predator in predators:
            distance = self.position.distance_to(predator.position)
            if distance < closest_predator:
                closest_predator = distance

        # Modify max speed based on the closest predator
        if closest_predator < danger_zone:
            self.max_speed = 3
        elif closest_predator < alert_zone:
            self.max_speed = 2
        else: # Calm movement (default)
            self.max_speed = 1
        
        # Move the llama
        self.position += self.velocity
        self.velocity += self.acceleration
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * min(self.velocity.length(), self.max_speed)
        self.acceleration *= 0

    def wander(self):
        # Applies a small random force to create a wandering effect.
        wander_strength = 0.3  # Adjust this value for more or less wandering

        # Perlin Noise Wandering (better than just random)
        self.noise_time += 0.2
        noise_x = noise.pnoise1(self.noise_time, repeat=1000)
        noise_y = noise.pnoise1(self.noise_time + 100, repeat=1000)
        wander_force = pygame.Vector2(noise_x, noise_y) * wander_strength
  
        self.apply_force(wander_force)

    def apply_force(self, force):
        self.acceleration += force

    def edges(self):
        buffer = 30 # Distance before turning
        turn_strength = 0.3 # How sharply they turn

        if self.position.x > self.WIDTH - self.size - buffer:
            self.apply_force(pygame.Vector2(-turn_strength, 0))
        elif self.position.x < buffer:
            self.apply_force(pygame.Vector2(turn_strength, 0))
            
        if self.position.y > self.HEIGHT - self.size - buffer:
            self.apply_force(pygame.Vector2(0, -turn_strength))
        elif self.position.y < buffer:
            self.apply_force(pygame.Vector2(0, turn_strength))
    
    def flock(self, sheeps, predators):
        alignment = self.align(sheeps)
        cohesion = self.cohere(sheeps)
        separation = self.separate(sheeps)
        defend = self.defend(predators)

        # Apply forces with weights
        self.apply_force(alignment * self.alignmentVal)
        self.apply_force(cohesion * self.cohesionVal)
        self.apply_force(separation * self.separationVal)
        self.apply_force(defend * self.defendVal)
    
    def defend(self, predators):
        defend_force = pygame.Vector2(0, 0)
        for predator in predators:
            distance = self.position.distance_to(predator.position)
            if distance < self.perception_radius * 1.5: # Larger perception radius for predators
                diff = predator.position - self.position # Move toward predator
                diff = diff.normalize() * self.max_speed 
                defend_force += diff
        if defend_force.length() > 0:
            defend_force = defend_force.normalize() * self.max_speed
            defend_force += self.velocity
            if defend_force.length() > self.max_force:
                defend_force = defend_force.normalize() * self.max_force
        return defend_force
    
    def align(self, sheeps):
        # Steer towards average heading of neighbors
        total = 0
        avg_velocity = pygame.Vector2(0, 0)
        for sheep in sheeps:
            if self.position.distance_to(sheep.position) < self.perception_radius:
                avg_velocity += sheep.velocity
                total += 1
        if total > 0:
            avg_velocity /= total
            avg_velocity = avg_velocity.normalize() * self.max_speed
            steer = avg_velocity - self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
            return steer
        return pygame.Vector2(0, 0)
        
    def cohere(self, sheeps):
        # Steer towards the center of mass of neighbors
        total = 0
        center_mass = pygame.Vector2(0, 0)
        for sheep in sheeps:
            if self.position.distance_to(sheep.position) < self.perception_radius:
                center_mass += sheep.position
                total += 1
        if total > 0:
            center_mass /= total
            desired = center_mass - self.position
            if desired.length() > 0:
                desired = desired.normalize() * self.max_speed
                steer = desired - self.velocity
                if steer.length() > self.max_force:
                    steer = steer.normalize() * self.max_force
                return steer
        return pygame.Vector2(0, 0)
    
    def separate(self, sheeps):
        # Move away from close neighbors
        total = 0
        steer = pygame.Vector2(0, 0)
        for sheep in sheeps:
            distance = self.position.distance_to(sheep.position)
            if 0 < distance < self.perception_radius / 2:
                diff = self.position - sheep.position
                diff /= ( distance * 0.5 ) # Weight by distance
                steer += diff
                total += 1
        if total > 0:
            steer /= total
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed - self.velocity
                if steer.length() > self.max_force:
                    steer = steer.normalize() * self.max_force
                return steer
        return pygame.Vector2(0, 0)
    
    def draw(self):
        self.screen.blit(self.icon, self.position)

