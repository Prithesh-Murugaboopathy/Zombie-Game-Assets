import pygame

TILE_WIDTH = 60
TILE_HEIGHT = 60

class Room():
    def __init__(self,pos,size,color,name,screen):
        self.pos = pos
        self.size = [size[0]*TILE_WIDTH, size[1]*TILE_HEIGHT]
        self.color = color
        self.name = name
        self.screen = screen
        
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.draw_border()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        
    def draw_border(self):
        for x in range(self.size[0]//TILE_WIDTH+1):
            border = pygame.Surface((x*TILE_WIDTH, self.size[1]), flags=2)
            border.fill("black")
            border_rect = border.get_rect()
            pygame.draw.rect(self.image,"black",border_rect,2)
        for y in range(self.size[1]//TILE_HEIGHT):
            border = pygame.Surface((self.size[0], y*TILE_HEIGHT), flags=2)
            border.fill("black")
            border_rect = border.get_rect()
            pygame.draw.rect(self.image,"black",border_rect,2)
            
    def draw(self):
        self.screen.blit(self.image,self.rect)
        
        

        
class Table():
    def __init__(self,pos,size,game,cond):
        self.pos = pos
        self.size = size
        self.game = game
        self.screen = self.game.screen
        self.show = False
        self.cond = cond
        self.through = False
        
        self.image = pygame.Surface(self.size)
        self.image.fill("brown")
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        
        self.init_border()
        
    def init_border(self):
        border = pygame.Surface(self.size,flags=2)
        rect = border.get_rect()
        pygame.draw.rect(self.image,"black",rect,2)
    
    def check_player(self,player):
        if "c" in self.cond:           
            if "c" in str(player.status) and player.rect.colliderect(self.rect):
                self.show = False
                self.through = False
            else:
                self.show = False
                if "j" in self.cond:
                    if "j" in str(player.status) and player.rect.colliderect(self.rect) and not self.show:
                        self.through = False
                    else:
                        self.through = True
        
    def draw(self):
        if self.show:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
        self.screen.blit(self.image,self.rect)
    
    def update(self,player):
        self.check_player(player)
        self.draw()
        
        
        
class Stranger():
    def __init__(self,game):
        self.game = game
        self.screen = self.game.screen
        self.player = self.game.player
        self.size = [TILE_WIDTH,TILE_HEIGHT]
        self.pos = [90,90]
        self.check_rect = pygame.Rect((0,0),(self.size[0]*2.5,self.size[1]*2.5))
        self.check_rect.center = self.pos
        self.talking = False
        
        self.image = pygame.transform.scale(pygame.image.load("stranger.png").convert_alpha(),self.size)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
        self.button_image = pygame.transform.scale(pygame.image.load("c.png"),(20,20))
        self.button_rect = self.button_image.get_rect()
        self.button_image.set_alpha(0)
        self.button_rect.bottomleft = [self.rect.left+22.5,self.rect.bottom]
        self.button_default_pos = self.button_rect.center
        self.button_show = False
        
        self.talking_image = pygame.transform.scale(pygame.image.load("Strangerf.png"),(300,500))
        self.talking_rect = self.talking_image.get_rect()
        self.talking_rect.topright = [1210,250]
        
    def draw(self):
        if not self.talking:
            self.screen.blit(self.image,self.rect)
            if self.button_show:
                self.screen.blit(self.button_image,self.button_rect)
        else:
            self.screen.blit(self.talking_image,self.talking_rect)
    
    def check_player(self):
        keys = pygame.key.get_pressed()
        if self.check_rect.colliderect(self.player.rect):
            self.button_show = True
        else:
            self.button_show = False
    
    def update_button(self):
        self.check_player()
        if self.button_show:
            if self.button_rect.centery > self.rect.top:
                self.button_rect.centery -= 3
            self.button_image.set_alpha(self.button_image.get_alpha() + 24)
            if pygame.key.get_pressed()[pygame.K_c]:
                self.game.status = "conversation"
        else:
            self.button_image.set_alpha(0)
            self.button_rect.center = self.button_default_pos
    
    def update(self,game):
        self.draw()
        if not self.talking:
            self.check_player()
            self.update_button()
             
        
        
        
        
class Player():
    def __init__(self, game):
        self.pos = [600,350]
        self.game = game
        self.size = [50,50]
        self.image = pygame.transform.scale(pygame.image.load("Player3.png").convert_alpha(), self.size)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.check_rect = self.rect.copy()
        self.angle = 0
        self.speed = 2
        self.jumping = False
        self.crouching = False
        self.runnning = False
        self.talking = False
        self.old_size = self.size
        self.old_pos = self.pos
        self.stamina = 1000
        self.status = "s-wr"
        self.talking_image = pygame.transform.scale(pygame.image.load("Player3f.png"),(300,500))
        self.talking_rect = self.talking_image.get_rect()
        self.talking_rect.topleft = [-10,250]
    
    def update_status(self):
        for ang, dr in [(90,'l'),(0,"r"),(45,"u"),(135,"d")]:
            if self.angle == ang:
                self.status = self.status[0:-1] + dr

        if self.runnning:
            self.status = self.status[0:2] + "r" + self.status[-1]
        else:
            self.status = self.status[0:2] + "w" + self.status[-1]
        
        if self.size[0] != 50:
            self.status = "j" + self.status[1:]
        else:
            if self.crouching:
                self.status = "c" + self.status[1:]
            else:
                self.status = "s" + self.status[1:]
    
    def update_size(self):
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update_speed(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and bool(self.stamina > 4):
            if self.crouching:
                self.speed = 4
            else:
                self.speed = 6
            self.runnning = True
        else:
            self.speed = 2
            self.runnning = False
    
    def update_stamina(self):
        if self.jumping:
            self.stamina -= 6
        elif bool(self.stamina < 1000):
            self.stamina += 1
        if self.runnning:
            self.stamina -= 3
        elif bool(self.stamina < 1000):
            self.stamina += 1
        if self.stamina < 0:
            self.stamina = 0
    
    def crouch(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and not self.crouching:
            self.crouching = True
        elif keys[pygame.K_q]:
            self.crouching = False
        if self.crouching:
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Player3c.png").convert_alpha(), self.size), self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        else:
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Player3.png").convert_alpha(), self.size), self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
    
    def check_collision(self,objects,rect):
        for obj in objects:
            if (obj.through and obj.rect.colliderect(rect)) :
                return False
        else:
            return True
            
    def move(self):
        keys = pygame.key.get_pressed()
        self.check_rect.center = self.rect.center
        if keys[pygame.K_w]:
            self.check_rect.centery -= self.speed
            self.angle = 45
        if keys[pygame.K_s]:
            self.check_rect.centery += self.speed
            self.angle = 135
        if keys[pygame.K_a]:
            self.check_rect.centerx -= self.speed
            self.angle = 90
        if keys[pygame.K_d]:
            self.check_rect.centerx += self.speed
            self.angle = 0
        self.image = pygame.transform.scale(pygame.transform.rotate(self.image,self.angle),self.size)
        if game.status == "room":
            if self.check_collision(self.game.objects,self.check_rect):
                self.pos = self.check_rect.center
                self.rect.center = self.pos
                self.old_pos = self.pos
            else:
                for obj in self.game.objects:
                    if obj.rect.colliderect(self.check_rect) and self.old_pos == self.pos and "c" not in self.status:
                        self.rect.center = [1170,30]
                        self.pos = self.rect.center
        else:
            self.pos = self.check_rect.center
            self.rect.center = self.pos
            self.old_pos = self.pos

        
    def draw(self):
        if not self.talking:
            self.game.screen.blit(self.image, self.rect)
        elif self.talking:
            self.game.screen.blit(self.talking_image, self.talking_rect)
                              
    def jump(self):
        self.old_size = self.size
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.size[0] == 50:
            self.jumping = True
        if self.size[0] == 70:
            self.jumping = False
        if self.jumping and self.size[0] != 70 and bool(self.stamina >= 80) and not self.crouching:
            self.size[0] += 2
            self.size[1] += 2
        if self.stamina == 0:
            self.jumping = False
        if not self.jumping and self.size[0] != 50 and not self.crouching:
            self.size[0] -= 1
            self.size[1] -= 1
        if self.crouching:
            self.size = [50,50]
        
    def update(self):
        pygame.event.pump()
        self.draw()
        if not self.talking:
            self.move()
            self.jump()
            self.crouch()
            self.update_size()
            self.update_speed()
            self.update_stamina()
            self.update_status()

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1200,700))
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.running = True
        self.init_game()
        self.status = "room"
        self.market_background = pygame.transform.scale(pygame.image.load("market_background.png"),(1200,700))
        self.init_music()
        
    def init_game(self):
        self.player = Player(self)
        self.room = Room([0,0],[40,50],"white","black",self.screen)
        self.stranger = Stranger(self)
        self.table = Table([120,120],[60,120],self,"cj")
        self.objects = [self.table]
        self.tables = [self.table]
    
    def init_music(self):
        self.music = pygame.mixer.Sound("MUJIC.mp3")
        pygame.mixer.music.set_volume(0.9)
        
    def update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_r]:
                self.status = "room"
            
            elif keys[pygame.K_m]:
                self.status = "market"
            
            if self.status=="room":

                if self.player.rect.centery < 0:
                    if 550 < self.player.rect.centerx < 650:
                        self.player.rect.centery = 670

                
                if self.player.rect.center == (600,350):
                    self.player.rect.right = 1200
                    self.player.rect.top = 0
                
                for table in self.tables:
                    if table.show:
                        table.update(self.player)
                
                self.room.draw()
                self.player.update()
                
                for table in self.tables:
                    if not table.show:
                        table.update(self.player)
                
                if self.player.rect.centery > 680:
                    if 550 < self.player.rect.centerx < 650:
                        self.status = "market"
            
            if self.status=="market":
                if self.player.rect.centery > 680:
                    if 550 < self.player.rect.centerx < 650:
                        self.player.rect.centery = 30
                
                self.screen.fill((0,51,0))
                self.stranger.update(self)
                self.player.update()
                self.stranger.update(self)
                
                if self.player.rect.centery < 0:
                    if 550 < self.player.rect.centerx < 650:
                        self.status = "room"
            
            if self.status=="conversation":
                self.screen.blit(self.market_background,(0,0))
                self.stranger.talking = True
                self.player.talking = True
                self.player.update()
                self.stranger.update(self)
                if keys[pygame.K_o]:
                    self.status = "market"
                    self.stranger.talking = False
                    self.player.talking = False
            
#             self.music.play()
            self.clock.tick(60)
            pygame.display.update()
        pygame.quit()
        pygame.mixer.quit()

game = Game()
game.update()
