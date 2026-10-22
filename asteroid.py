import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float):
        self.position += (self.velocity * dt)

    def split(self):
        # immediately call kill to remove current asteroid and form 2 smaller ones
        self.kill()
        # if current is less than the minimum size, do not split further
        if self.radius < ASTEROID_MIN_RADIUS:
            return 
        
        # log the asteroid split event
        log_event("asteroid_split")
        # generate a random angle for splitting the asteroid
        angle = random.uniform(20, 50)
        # create two new velocity vectors by rotating the current velocity by the angle and its negative
        new_velocity1 = self.velocity.rotate(angle)
        new_velocity2 = self.velocity.rotate(-angle)
        # compute the new radius for the smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # create two new asteroid objects with the new radius at the current position
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        # set the velocities for the new asteroids
        asteroid1.velocity = new_velocity1 * 1.2
        asteroid2.velocity = new_velocity2 * 1.2
        # add the new asteroids to the appropriate sprite groups
        if hasattr(Asteroid, "containers"):
            for group in Asteroid.containers:
                group.add(asteroid1)
                group.add(asteroid2)
        