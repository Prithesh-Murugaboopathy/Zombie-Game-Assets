import pygame
from bullet import Bullet
import math
        
class Gun():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.pos = self.player.pos
        self.image = pygame.transform.scale(pygame.image.load("gun2.png").convert().convert_alpha(), (50,10))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.angle = 0
        
    def draw(self):
        self.screen.blit(self.image, self.rect)
    def update_pos(self, player_pos):
        self.rect.topleft = player_pos
        self.pos = player_pos
    def update_angle(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x_dif = mouse_pos[0] - self.pos[0]
        mouse_y_dif = mouse_pos[1] - self.pos[1]
        if mouse_y_dif == 0:
            mouse_y_dif = 0.000001
        angle = math.degrees(math.atan(mouse_x_dif/mouse_y_dif))
        angle *= 2
        pos = self.rect.topleft
        image_rect = self.image.get_rect(topleft = self.rect.topleft)
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        self.rect = rotated_image_rect
        self.screen.blit(rotated_image, rotated_image_rect)
        self.angle = angle
#         pos = game.player.rect.center
#         a = Vector2(pos)
#         b = Vector2(pygame.mouse.get_pos())
#         self.angle = Vector2().angle_to(a-b) + 180
#         self.image = pygame.transform.rotate(self.image,self.angle)
#         self.rect = self.image.get_rect()
#         self.rect.center = self.player.rect.center
#         self.screen.blit(self.image,self.rect)
        print("gun",self.angle)
    def update(self, player_pos):
        self.update_pos(player_pos)
        self.update_angle()
