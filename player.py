import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):

    def __init__(self, x: float, y: float, radius: float, cd: float):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.shoot_cooldown = cd

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        right = pygame.Vector2(0,1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        # everytime update is called, reduce shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.shoot_cooldown < 0:
            self.shoot_cooldown = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            shot = self.shoot()
            if shot:
                return shot


    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotate_with_speed = rotated_vector * PLAYER_SPEED * dt
        self.position += rotate_with_speed

    def shoot(self) -> "Shot":
        # if current timer is greater than 0, cannot shoot
        # otherwise set time equal to cooldown seconds
        if self.shoot_cooldown > 0:
            return None

        # create shot at current position of the player
        shot = Shot(self.position.x, self.position.y)

        #set shot velocity attribute
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        return shot
