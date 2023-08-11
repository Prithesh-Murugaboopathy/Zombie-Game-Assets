import pygame
from pygame.math import Vector2

def correct_angle(angle):
    angle *= 0.6
    return angle

class Bullet():
    def __init__(self, game):
        self.game = game
        self.pos = game.player.gun.rect.center
        a = Vector2(self.pos)
        b = Vector2(pygame.mouse.get_pos())
        self.angle = Vector2().angle_to(a-b) + 180
        self.image = pygame.transform.rotate(pygame.Surface((5,5),pygame.SRCALPHA), self.angle)
        self.image.fill("yellow")
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        offset = Vector2(40, 0).rotate(self.angle)
        self.pos = Vector2(self.pos) + offset
        self.velocity = Vector2(1, 0).rotate(self.angle) * 9
        self.shoot = False
    def update_pos(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        print("bullet",self.angle)
        if not self.game.screen.get_rect().colliderect(self.rect):
            del self
    def update_angle(self,gun):
        self.angle = gun.angle
    def shot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot = True
        else:
            self.shoot = False
    def draw(self):
        self.game.screen.blit(self.image,self.rect)
    def update(self,gun):
        self.update_angle(gun)
        self.update_pos(gun)
        self.shot()
        self.draw()
