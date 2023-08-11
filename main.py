import pygame
from pygame.math import Vector2
from random import random
from player import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200,700))
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.running = True
        self.init_game()
    def init_game(self):
        self.player = Player(self)
    def update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((0,51,0))
            self.player.update()
            self.clock.tick(60)
            pygame.display.update()
        pygame.quit()

game = Game()
game.update()