import pygame

class Player():
    def __init__(self, game):
        self.pos = (600,350)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load("playermode3.png").convert_alpha(), (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.angle = 90
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.centery -= 2
            self.image = pygame.transform.rotate(self.image, (self.angle*-1)+180)
            self.angle = 180
        if keys[pygame.K_s]:
            self.rect.centery += 2
            self.image = pygame.transform.rotate(self.image, (self.angle*-1))
            self.angle = 0
        if keys[pygame.K_a]:
            self.rect.centerx -= 2
            self.image = pygame.transform.rotate(self.image, (self.angle*-1)-90)
            self.angle = 270
        if keys[pygame.K_d]:
            self.rect.centerx += 2
            self.image = pygame.transform.rotate(self.image, (self.angle*-1)+90)
            self.angle = 90
    def draw(self):
        self.game.screen.blit(self.image, self.rect)
    
    def update(self):
        self.move()
        self.draw()


        