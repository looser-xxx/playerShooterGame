import random

from pytmx.util_pygame import load_pygame

from groups import AllSprites
from player import Player
from settings import *
from sprites import *


class Game:
    def __init__(self) -> None:
        self.window = window
        self.screen = pygame.display.set_mode(self.window)
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.setUpMap()
        self.runGame = True
        self.clock = pygame.time.Clock()

    def setUpPlayer(self, pos):
        self.playerSpeed = 400
        self.player = Player(
            self.allSprites,
            self.collisionSprites,
            self.playerSpeed,
            pos,
        )
        self.gun = Gun(self.allSprites, self.player)

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
