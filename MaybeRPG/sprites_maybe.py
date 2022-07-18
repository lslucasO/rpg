import os.path
import pygame
import math
import random
from config_maybe import *

class Spritesheet:
    def __init__(self, game, file):
        self.game = game
        self.sheet = pygame.image.load(os.path.join(self.game.image_directory, file)).convert()

    def get_sprite(self, x, y, widht, height):
        sprite = pygame.Surface([widht, height])
        sprite.blit(self.sheet, (0, 0), (x, y, widht, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.widht = TILESIZE
        self.height = TILESIZE

        self.facing = 'down'

        self.x_control = 0
        self.y_control = 0

        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(1, 2, self.widht, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()


        self.rect.x += self.x_control
        self.collide_blocks('x')
        self.rect.y += self.y_control
        self.collide_blocks('y')

        self.x_control = 0
        self.y_control = 0

    def movement(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_control -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_control += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.y_control -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_control += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_control > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_control < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_control > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_control < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):

        down_animation = [self.game.character_spritesheet.get_sprite(1, 2, 32, 48),
                          self.game.character_spritesheet.get_sprite(32, 0, 32, 48),
                          self.game.character_spritesheet.get_sprite(64, 0, 32, 48),
                          self.game.character_spritesheet.get_sprite(96, 0, 32, 48)
                          ]

        up_animation = [self.game.character_spritesheet.get_sprite(0, 144, 32, 48),
                          self.game.character_spritesheet.get_sprite(32, 144, 32, 48),
                          self.game.character_spritesheet.get_sprite(64, 144, 32, 48),
                          self.game.character_spritesheet.get_sprite(96, 144, 32, 48)]

        left_animation = [self.game.character_spritesheet.get_sprite(0, 48, 32, 48),
                          self.game.character_spritesheet.get_sprite(32, 48, 32, 48),
                          self.game.character_spritesheet.get_sprite(64, 48, 32, 48),
                          self.game.character_spritesheet.get_sprite(96, 48, 32, 48)
                          ]

        right_animation = [self.game.character_spritesheet.get_sprite(0, 96, 32, 48),
                          self.game.character_spritesheet.get_sprite(32, 96, 32, 48),
                          self.game.character_spritesheet.get_sprite(64, 96, 32, 48),
                          self.game.character_spritesheet.get_sprite(96, 96, 32, 48)
                          ]

        if self.facing == 'down':
            if self.y_control == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, 32, 48)
            else:
                self.image = down_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_control == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 144, 32, 48)
            else:
                self.image = up_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_control == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 48, 32, 48)
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_control == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 96, 32, 48)
            else:
                self.image = right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.widht = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.widht, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = WATER_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.widht = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(875, 65, 75, 80)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Rock(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ROCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.widht = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.widht, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemies(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMIES_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.widht = TILESIZE
        self.height = TILESIZE

        self.x_control = 0
        self.y_control = 0

        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemies_spritesheet.get_sprite(96, 16, 16, 16)
        self.image = pygame.transform.scale(self.image, (16 * 2, 16 * 2))


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.rect.x += self.x_control
        self.rect.y += self.y_control

        self.x_control = 0
        self.y_control = 0

    def movement(self):
        if self.facing == 'left':
            self.x_control = ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_control = ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop <= self.max_travel:
                self.facing = 'left'

    def animate(self):
        pass
