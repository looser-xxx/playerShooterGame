from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.image = pygame.Surface((69, 69))
        self.rect = self.image.get_frect(center=windowCenter)
        self.speed = 0
        self.direction = pygame.Vector2(0, 1)
        self.pos = pygame.Vector2(self.rect.center)
        self.frameIndex = 0
        self.enemy = ""

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def getDirection(self):
        centerVect = pygame.Vector2(self.player.rect.center)
        vectorToCenter = centerVect - self.pos
        if vectorToCenter.length() > 0:
            self.direction = vectorToCenter.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

    def die(self):
        if self.rect.colliderect(self.player.rect):
            print("collide")
            self.kill()

    def update(self, dt):
        self.getDirection()
        self.animate(dt)
        self.move(dt)
        self.die()

    def loadImages(self):
        self.frames = {"bat": [], "blob": [], "skeleton": []}
        for enemy in self.frames.keys():
            for folderPath, subFolder, fileNames in walk(
                join("images", "enemies", enemy)
            ):
                if fileNames:
                    for fileName in sorted(
                        fileNames, key=lambda name: int(name.split(".")[0])
                    ):
                        fullPath = join(folderPath, fileName)
                        surf = pygame.image.load(fullPath).convert_alpha()
                        self.frames[enemy].append(surf)

    def getEnemyType(self, name):
        self.enemy = name

    def animate(self, dt):

        self.frameIndex += 5 * dt
        self.image = self.frames[self.enemy][
            int(self.frameIndex) % len(self.frames[self.enemy])
        ]


class Bat(Enemy):
    def __init__(self, group, pos, player) -> None:
        super().__init__(group)
        self.loadImages()
        self.rect = self.image.get_frect(center=pos)
        self.speed = 400
        self.pos = pygame.Vector2(self.rect.center)
        self.player = player
        self.getEnemyType("bat")


class Blob(Enemy):
    def __init__(self, group, pos, player) -> None:
        super().__init__(group)
        self.loadImages()
        self.rect = self.image.get_frect(center=pos)
        self.speed = 400
        self.pos = pygame.Vector2(self.rect.center)
        self.player = player
        self.getEnemyType("blob")


class Skeleton(Enemy):
    def __init__(self, group, pos, player) -> None:
        super().__init__(group)
        self.loadImages()
        self.rect = self.image.get_frect(center=pos)
        self.speed = 400
        self.pos = pygame.Vector2(self.rect.center)
        self.player = player
        self.getEnemyType("skeleton")
