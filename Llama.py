from Agent import Agent
import pygame
import random

WHITE = (255, 255, 255)

class Llama(Agent):
    def __init__(self, x, y, size, screen, WIDTH, HEIGHT):
        self.icon = pygame.transform.scale(pygame.image.load("assets/noun-llama-7034038.png"), (size, size))
        self.position = self.icon.get_rect()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 3
        self.max_force = 0.05
        self.perception_radius = 50
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def move(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.velocity = self.velocity.normalize() * min(self.velocity.length(), self.max_speed)
        self.acceleration *= 0

    def apply_force(self, force):
        self.acceleration += force

    def edges(self):
        if self.position.x > self.WIDTH:
            self.position.x = self.WIDTH
        elif self.position.x < 0:
            self.position.x = 0
        if self.position.y > self.HEIGHT:
            self.position.y = self.HEIGHT
        elif self.position.y < 0:
            self.position.y = 0
    
    def flock(self, sheeps):
        alignment = self.align(sheeps)
        cohesion = self.cohere(sheeps)
        separation = self.separate(sheeps)

        # Apply forces with weights
        self.apply_force(alignment * 1.0)
        self.apply_force(cohesion * 0.8)
        self.apply_force(separation * 1.50)
    
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
                diff /= distance # Weight by distance
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

