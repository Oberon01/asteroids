import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_state, log_event

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    # creating sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # set Player container to updatable and drawable
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    # create player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS)

    # set Asteroid container to asteroids, updatable, and drawable
    Asteroid.containers = (asteroids, updatable, drawable)

    # group for asteroid field
    asteroidfield = pygame.sprite.Group()

    # set asteroid field container to updatable only
    AsteroidField.containers = updatable
    asteroidfield = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for d in drawable:
            d.draw(screen)
        updatable.update(dt)
        for a in asteroids:
            if player.collides_with(a):
                log_event("player_hit")
                print("Game Over")
                sys.exit()
        for s in shots:
            for a in asteroids:
                if s.collides_with(a):
                    log_event("asteroid_shot")
                    a.split()
                    s.kill()
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
