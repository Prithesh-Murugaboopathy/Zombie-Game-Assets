import pygame

class Bullet():
    def __init__(self, game):
        self.game = game
        self.angle = game.gun.angle - 90
        self.image = pygame.transform.rotate(pygame.Surface((20,5),pygame.SRCALPHA), self.angle)
        self.image.fill("purple")
        self.pos = game.gun.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    def update_pos(self,gun):
        print(gun.rect.center)
        self.rect.center = gun.rect.center
    def update_angle(self,gun):
        self.angle = gun.angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
    def draw(self):
        self.game.screen.blit(self.image,self.rect)
    def update(self,gun):
        self.update_angle(gun)
        self.update_pos(gun)
        self.draw()