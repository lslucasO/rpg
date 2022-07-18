import pygame
from pygame.locals import *
from sprites_maybe import *
from config_maybe import *
import os
from sys import exit

class Game:
    def __init__(self):
        pygame.init()

        self.main_directory = os.path.dirname(__file__)
        self.image_directory = os.path.join(self.main_directory, 'imagem_maybe')

        self.screen = pygame.display.set_mode((WIN_WIDHT, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 40)

        self.title = pygame.display.set_caption('Test for Fun')

        self.character_spritesheet = Spritesheet(self, 'gal.jpg')
        self.terrain_spritesheet = Spritesheet(self, 'terrain.png')
        self.enemies_spritesheet = Spritesheet(self, 'character rpg.png')

        self.running = True

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'E':
                    Enemies(self, j, i)
                if column == 'R':
                    Rock(self, j, i)
                if column == 'W':
                    Water(self, j, i)
                if column == 'P':
                    Player(self, j, i)

    def new(self):
        # new game start
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def update(self):
        # updates the sprite
        self.all_sprites.update()

    def events(self):
        # check events in the game
        for event in pygame.event.get():
            if event.type == QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        # draw the things
        self.screen.fill(BLACK)
        self.clock.tick(FPS)
        self.all_sprites.draw(self.screen)
        pygame.display.update()

    def main(self):
        # the real loop
        while self.running:
            self.draw()
            self.update()
            self.events()
        self.playing = False

    def start_screen(self):
        pass

    def game_over(self):
        pass

game = Game()
game.start_screen()
game.new()

while game.running:
    game.main()
    game.game_over()

pygame.quit()
exit()