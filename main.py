import random
from enum import Flag

from pygame import FLASH_BRIEFLY, key
from pytmx.util_pygame import load_pygame

from groups import AllSprites
from player import Player
from settings import *
from sprites import *


def loadAfterCooldown(eventTime, delay) -> bool:
    """
    Check if a cooldown period has passed.

    Args:
        eventTime (int): The timestamp when the event last occurred.
        delay (int): The duration of the cooldown in milliseconds.

    Returns:
        bool: True if the cooldown has passed, False otherwise.
    ""a
    if (eventTime + delay) < pygame.time.get_ticks():
        return True
    else:
        return False


class Game:
    def __init__(self) -> None:
        self.window = window
        self.screen = pygame.display.set_mode(self.window)
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.setUpMap()
        self.runGame = True
        self.clock = pygame.time.Clock()
        self.loadImages()

    def loadImages(self):
        self.bulletSurf = pygame.image.load("./images/gun/bullet.png").convert_alpha()

    def setUpPlayer(self, pos):
        self.playerSpeed = 400
        self.player = Player(
            self.allSprites,
            self.collisionSprites,
            self.playerSpeed,
            pos,
        )
        self.gun = Gun(self.allSprites, self.player)
        self.canShoot = True
        self.shootTime = 0
        self.shootDealy = 100
        self.bulletSprite = pygame.sprite.Group()

    def checkEvents(self) -> None:
        """
        Handle all user input and system events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGame = False

        self.keyboardInput()

    def setUpMap(self):
        map = load_pygame("./data/maps/world.tmx")
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite(self.allSprites, (x * tileSize, y * tileSize), image)
        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite(
                (self.allSprites, self.collisionSprites), (obj.x, obj.y), obj.image
            )
        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite(
                self.collisionSprites,
                (obj.x, obj.y),
                pygame.Surface((obj.width, obj.height)),
            )
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.setUpPlayer((obj.x, obj.y))

    def keyboardInput(self) -> None:

        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0] and self.canShoot:
            pos = self.gun.rect.center + self.gun.playerDirection * 50

            Bullets(
                (self.allSprites, self.bulletSprite),
                self.bulletSurf,
                pos,
                self.gun.playerDirection,
            )
            self.canShoot = False
            self.shootTime = pygame.time.get_ticks()
        else:
            self.canShoot = loadAfterCooldown(self.shootTime, self.shootDealy)

    def run(self) -> None:
        """
        The main game loop.
        """
        while self.runGame:
            self.dt = self.clock.tick() / 1000
            self.checkEvents()
            self.screen.fill("#212326")
            self.allSprites.update(self.dt)
            self.allSprites.draw(self.player.rect.center)
            pygame.display.flip()

        pygame.quit()


def main() -> None:
    """
    Entry point for the application.
    """
    print("welcome to Vampire Hunter")
    game = Game()
    game.run()


if __name__ == "__main__":
    main()