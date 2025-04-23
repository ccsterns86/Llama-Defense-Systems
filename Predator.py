from Agent import Agent
import pygame
import random
import time

class Predator(Agent):
    def __init__(self, x, y, size, screen, WIDTH, HEIGHT):
        self.icon = pygame.transform.scale(pygame.image.load("assets/noun-wolf-7401722.png"), (size, size))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 3
        self.max_force = 0.05
        self.perception_radius = 100
        self.alignmentVal = 0.2
        self.cohesionVal = 0.8
        self.separationVal = 1.0
        self.fleeVal = 2.0
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.size = size
        self.pack_strength = 0

        # Attack variables
        self.max_attack_frequency = 100
        self.ticks_since_last_attack = 100
        self.attack_radius = 25

        # Health
        self.health = 5
        self.is_alive = True
        self.is_spawned = False

        # For tracking off screen 
        self.off_screen_time = None
        self.respawn_delay = 3
        self.off_screen = False

    def update_values(self, values):
        for item in values:
            if item == "cohesion":
                self.cohesionVal = values[item]
            elif item == "separation":
                self.separationVal = values[item]
            elif item == "flee":
                self.fleeVal = values[item]
            elif item == "perception":
                self.perception_radius = values[item]
            elif item == "attack time":
                self.max_attack_frequency = values[item]
            elif item == "pack strength":
                self.pack_strength = values[item]


    def move(self, llamas, water_bodies):

        if not self.is_alive:
            return
        # update attack counter
        self.ticks_since_last_attack += 1

        if not self.can_attack():
            return

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
        next_position = self.position + self.velocity
        if not any(w.contains((next_position.x, next_position.y)) for w in water_bodies):
            self.position = next_position
        
        self.velocity += self.acceleration
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * min(self.velocity.length(), self.max_speed)
        self.acceleration *= 0


    def apply_force(self, force):
        self.acceleration += force

    def edges(self, water_bodies):

        if not self.can_attack():
            return

        buffer = 50 # Buffer off screen allowed

        # Check if predator goes off-screen
        if (self.position.x < -buffer or self.position.x > self.WIDTH + buffer or 
            self.position.y < -buffer or self.position.y > self.HEIGHT + buffer):
            if not self.off_screen:
                self.off_screen_time = time.time()  # Record the time it went off-screen
                self.off_screen = True
        else:
            self.off_screen = False
            self.off_screen_time = None

        # Respawn after a delay
        if self.off_screen and (time.time() - self.off_screen_time > self.respawn_delay):
            self.respawn()

        # Water repulsion
        for water in water_bodies:
            dist = pygame.Vector2(self.position.x - water.x, self.position.y - water.y)
            if dist.length() < water.radius + self.size + 10:
                self.apply_force(dist.normalize() * 0.3)

    def respawn(self):

        # Respawn the predator at a random location on the screen after being off-screen.
        side = random.choice(["top", "bottom", "left", "right"])
        
        if side == "top":
            self.position = pygame.Vector2(random.randint(0, self.WIDTH), -self.size)
        elif side == "bottom":
            self.position = pygame.Vector2(random.randint(0, self.WIDTH), self.HEIGHT + self.size)
        elif side == "left":
            self.position = pygame.Vector2(-self.size, random.randint(0, self.HEIGHT))
        else:  # "right"
            self.position = pygame.Vector2(self.WIDTH + self.size, random.randint(0, self.HEIGHT))

        # Calculate direction towards center of screen
        center = pygame.Vector2(self.WIDTH / 2, self.HEIGHT / 2)
        direction_to_center = center - self.position
        if (direction_to_center.length() > 0):
            direction_to_center = direction_to_center.normalize() * self.max_speed / 2
        else:
            direction_to_center = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))

        self.velocity = direction_to_center  # Reset velocity
        self.off_screen = False  # Reset flag
    
    def flock(self, sheeps, llamas, predators):

        if not self.can_attack():
            return

        alignment = self.align(sheeps, predators)
        cohesion = self.cohere(sheeps, predators)
        separation = self.separate(predators)
        flee = self.flee(llamas)

        # Apply forces with weights
        # Apply forces with weights
        self.apply_force(alignment * self.alignmentVal)
        self.apply_force(cohesion * self.cohesionVal)
        self.apply_force(separation * self.separationVal)
        self.apply_force(flee * self.fleeVal)

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

    def align(self, sheeps, predators):
        # Steer towards average heading of neighbors
        total = 0
        avg_velocity = pygame.Vector2(0, 0)
        for sheep in sheeps:
            if sheep.is_alive and self.position.distance_to(sheep.position) < self.perception_radius:
                if self.pack_strength > 0:
                    avg_velocity += sheep.velocity * (1/self.pack_strength)
                else:
                    avg_velocity += sheep.velocity
                total += 1

        for predator in predators:
            if self.pack_strength > 0 and predator != self and predator.is_alive and self.position.distance_to(predator.position) < self.perception_radius:
                avg_velocity += predator.velocity * self.pack_strength
                total += 1

        if total > 0:
            avg_velocity /= total
            avg_velocity = avg_velocity.normalize() * self.max_speed
            steer = avg_velocity - self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
            return steer
        return pygame.Vector2(0, 0)
        
    def cohere(self, sheeps, predators):
        # Steer towards the center of mass of neighbors
        total = 0
        center_mass = pygame.Vector2(0, 0)
        for sheep in sheeps:
            if sheep.is_alive and self.position.distance_to(sheep.position) < self.perception_radius:
                if self.pack_strength >0:
                    center_mass += sheep.position * (1/self.pack_strength)
                else:
                    center_mass += sheep.position
                total += 1

        for predator in predators:
            if self.pack_strength > 0 and predator != self and predator.is_alive and self.position.distance_to(predator.position) < self.perception_radius:
                center_mass += predator.position * self.pack_strength
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
    
    def separate(self, predators):
        # Move away from close neighbors
        total = 0
        steer = pygame.Vector2(0, 0)
        for predator in predators:
            if self.pack_strength > 0 and predator != self and predator.is_alive:
                distance = self.position.distance_to(predator.position)
                if 0 < distance < self.perception_radius / 2:
                    diff = self.position - predator.position
                    diff /= distance # Weight by distance
                    steer += diff * self.pack_strength
                    total += 1
        if total > 0:
            steer /= total
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed - self.velocity
                if steer.length() > self.max_force:
                    steer = steer.normalize() * self.max_force
                return steer
        return pygame.Vector2(0, 0)

    def can_attack(self):
        return self.ticks_since_last_attack > self.max_attack_frequency

    def attack(self, sheeps):
        for sheep in sheeps:
            if sheep.is_alive: 
                distance = self.position.distance_to(sheep.position)
                if distance < self.attack_radius and self.can_attack():
                    sheep.die()
                    self.ticks_since_last_attack = 0
                    self.health += 1

    def check_health(self, llamas):
        for llama in llamas:
            distance = self.position.distance_to(llama.position)
            if distance < 1.5 * self.attack_radius and self.can_attack():
                self.ticks_since_last_attack = 0
                self.health -= 1
                if self.health <= 0:
                    self.is_alive = False
    
    def draw(self):
        if self.is_alive:
            self.screen.blit(self.icon, self.position)
        else:
            self.screen.blit(pygame.transform.flip(self.icon, False, True), self.position)

