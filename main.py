import pygame
from player import Player
from gun import Gun
from bullet import Bullet

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
        self.gun = Gun(self)
        self.bullet = Bullet(self)
        
    def update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill("dark green")
            self.player.update()
            self.bullet.update(self.gun)
            self.gun.update(self.player.rect.center)
            self.clock.tick(3)
            pygame.display.update()
        pygame.quit()

game = Game()
game.update()