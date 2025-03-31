from Agent import Agent
import pygame
import random


class Predator(Agent):
    def __init__(self, x, y, size, screen, WIDTH, HEIGHT):
        self.icon = pygame.transform.scale(pygame.image.load("assets/noun-wolf-7401722.png"), (size, size))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 3
        self.max_force = 0.05
        self.perception_radius = 100
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.size = size

    def move(self, llamas):
        danger_zone = self.perception_radius / 2
        # alert_zone = self.perception_radius * 1.5

        closest_llama = float("inf")

        for llama in llamas:
            distance = self.position.distance_to(llama.position)
            if distance < closest_llama:
                closest_llama = distance

        # Modify max speed based on the closest predator
        if closest_llama < danger_zone:
            self.max_speed = 3
        # elif closest_llama < alert_zone:
        #     self.max_speed = 2
        else: # Calm movement (default)
            self.max_speed = 2
        
        # Move the predator
        self.position += self.velocity
        self.velocity += self.acceleration
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * min(self.velocity.length(), self.max_speed)
        self.acceleration *= 0

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
    
    def flock(self, sheeps, llamas):
        alignment = self.align(sheeps)
        cohesion = self.cohere(sheeps)
        flee = self.flee(llamas)

        # Apply forces with weights
        self.apply_force(alignment * 1.0)
        self.apply_force(cohesion * 0.8)
        self.apply_force(flee * 2.0)

    def flee(self, llamas):
        flee_force = pygame.Vector2(0, 0)
        for llama in llamas:
            distance = self.position.distance_to(llama.position)
            if distance < self.perception_radius * 1.5: # Larger perception radius for predators
                diff = self.position - llama.position
                diff = diff.normalize() * self.max_speed # Move in opposite direction
                flee_force += diff
        if flee_force.length() > 0:
            flee_force = flee_force.normalize() * self.max_speed
            flee_force -= self.velocity
            if flee_force.length() > self.max_force:
                flee_force = flee_force.normalize() * self.max_force
        return flee_force

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

