import random
from enum import Flag

from pytmx.util_pygame import load_pygame

from enemies import Bat, Blob, Skeleton
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
    """
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
        self.map = load_pygame(resource_path("data/maps/world.tmx"))
        self.setUpEnemy()

    def loadImages(self):
        self.bulletSurf = pygame.image.load(resource_path("images/gun/bullet.png")).convert_alpha()

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

    def setUpEnemy(self):
        self.toSpawnEnemy = True
        self.enemySpawnDelay = 1000
        self.enemySpawnTime = 0
        self.enemyPos = []
        self.enemyIndex = 1
        for obj in self.map.get_layer_by_name("Entities"):
            if obj.name == "Enemy":
                self.enemyPos.append((obj.x, obj.y))
        self.enemySprites = pygame.sprite.Group()

    def spawnEnemy(self):
        if self.toSpawnEnemy:
            match self.enemyIndex:
                case 1:
                    Bat(
                        (self.allSprites, self.enemySprites),
                        random.choice(self.enemyPos),
                        self.player,
                    )
                    self.enemyIndex = 2
                case 2:
                    Blob(
                        (self.allSprites, self.enemySprites),
                        random.choice(self.enemyPos),
                        self.player,
                    )
                    self.enemyIndex = 3
                case 3:
                    Skeleton(
                        (self.allSprites, self.enemySprites),
                        random.choice(self.enemyPos),
                        self.player,
                    )
                    self.enemyIndex = 1
            self.toSpawnEnemy = False
            self.enemySpawnTime = pygame.time.get_ticks()
        else:
            self.toSpawnEnemy = loadAfterCooldown(
                self.enemySpawnTime, self.enemySpawnDelay
            )

    def checkEvents(self) -> None:
        """
        Handle all user input and system events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGame = False

        self.keyboardInput()
        print(self.player.hp)
        if self.player.hp <= 0:
            self.runGame = False

    def setUpMap(self):
        map = load_pygame(resource_path("data/maps/world.tmx"))
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite(self.allSprites, (x * tileSize, y * tileSize), image)
        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((self.allSprites), (obj.x, obj.y), obj.image)
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

    def updates(self):
        self.spawnEnemy()

    def run(self) -> None:
        """
        The main game loop.
        """
        while self.runGame:
            self.dt = self.clock.tick() / 1000
            self.checkEvents()
            self.screen.fill("#212326")
            self.allSprites.update(self.dt)

            hits = pygame.sprite.groupcollide(
                self.bulletSprite, self.enemySprites, True, True
            )

            self.updates()
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
