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
        self.distance = 140
        self.playerDirection = pygame.Vector2(1, 0)

        super().__init__(groups)
        self.gunSurf = pygame.image.load("./images/gun/gun.png").convert_alpha()
        self.image = self.gunSurf
        self.rect = self.image.get_frect(
            center=self.player.rect.center + self.playerDirection * self.distance
        )

    def update(self, _):
        self.rect.center = (
            self.player.rect.center + self.playerDirection * self.distance
        )
