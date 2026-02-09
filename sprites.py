import random
from math import atan2, degrees

from pytmx.util_pygame import pygame_image_loader

from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Gun(pygame.sprite.Sprite):
    def __init__(self, groups, player) -> None:
        self.player = player
        self.distance = 40
        self.playerDirection = pygame.Vector2(0, 1)

        super().__init__(groups)
        self.gunSurf = pygame.image.load(resource_path("images/gun/gun.png")).convert_alpha()
        self.image = self.gunSurf
        self.rect = self.image.get_frect(
            center=self.player.rect.center + self.playerDirection * self.distance
        )

    def getDirection(self):
        mousePos = pygame.Vector2(pygame.mouse.get_pos())
        playerPos = pygame.Vector2(windowCenter)
        self.playerDirection = (mousePos - playerPos).normalize()

    def rotateGun(self):
        angle = degrees(atan2(self.playerDirection.x, self.playerDirection.y)) - 90
        if self.playerDirection.x > 0:
            self.image = pygame.transform.rotozoom(self.gunSurf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gunSurf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.getDirection()
        self.rotateGun()
        self.rect.center = (
            self.player.rect.center + self.playerDirection * self.distance
        )


class Bullets(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos, direction) -> None:
        super().__init__(groups)
        self.surf = surf
        self.image = self.surf
        self.rect = self.image.get_frect(center=pos)
        self.direction = direction
        self.speed = 1750
        self.rotationSpeed = 200
        self.angle = random.randint(0, 360)
        self.spawnTime = pygame.time.get_ticks()
        self.lifeTime = 1500

    def move(self, dt):
        self.rect.center += self.speed * dt * self.direction

    def rotate(self, dt):
        self.image = pygame.transform.rotate(self.surf, self.angle)
        self.angle += self.rotationSpeed * dt

    def update(self, dt):
        self.move(dt)
        self.rotate(dt)
        if pygame.time.get_ticks() > self.spawnTime + 1000:
            self.kill()
