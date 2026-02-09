from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collisionSprites, speed, pos) -> None:
        super().__init__(groups)
        self.loadImages()
        self.state, self.frameIndex = "down", 0
        self.image = pygame.image.load("./images/player/down/0.png")
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(-90, -30)
        self.speed = speed
        self.direction = pygame.Vector2()
        self.collisionSprites = collisionSprites

    def loadImages(self):
        self.frames = {
            "left": [],
            "right": [],
            "up": [],
            "down": [],
        }
        for state in self.frames.keys():
            for folderPath, subFolder, fileNames in walk(
                join("images", "player", state)
            ):
                if fileNames:
                    for fileName in sorted(
                        fileNames, key=lambda name: int(name.split(".")[0])
                    ):
                        fullPath = join(folderPath, fileName)
                        surf = pygame.image.load(fullPath).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d] - int(keys[pygame.K_a]))
        self.direction.y = int(keys[pygame.K_s] - int(keys[pygame.K_w]))
        if self.direction:
            self.direction = self.direction.normalize()

    def move(self, dt):
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        for sprite in self.collisionSprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def animate(self, dt):

        if self.direction.x != 0:
            if self.direction.x > 0:
                self.state = "right"
            else:
                self.state = "left"
        if self.direction.y != 0:
            if self.direction.y > 0:
                self.state = "down"
            else:
                self.state = "up"

        if self.direction:
            self.frameIndex += 5 * dt
        else:
            self.frameIndex = 0

        self.image = self.frames[self.state][
            int(self.frameIndex) % len(self.frames[self.state])
        ]

    def update(self, dt) -> None:
        self.input()
        self.move(dt)
        self.animate(dt)
