import pygame
import math
import random
pygame.init()
logo = pygame.image.load("img/icon.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("ship game")
ssize = [1200, 600]
screen = pygame.display.set_mode(ssize)
font = pygame.font.SysFont("Cambria", 100)
colorbg = (0,157,196)
clock = pygame.time.Clock()
FPS = 60


def scaleimg(img, cons):
    size = int(img.get_width() * cons), int(img.get_height() * cons)
    return pygame.transform.scale(img, size)


class Button():
    
    def __init__(self, image, pos):
        self.image = image.convert_alpha()
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def interact(self,posi):
        if posi[0] in range(self.rect.left, self.rect.right) and posi[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
class ship(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, maxspeed, accel, rotospd, maxreverse):        
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.rotosp = rotospd
        self.speed = 0
        self.angle = 90
        self.accel = accel
        self.maxspeed = maxspeed
        self.maxreverse = maxreverse
        self.resizedim = scaleimg(self.image, 0.1)
        
    def rotateim(self, top_left):
        self.rimage = pygame.transform.rotate(self.resizedim, self.angle)
        rect= self.rimage.get_rect(center = self.rimage.get_rect(topleft = top_left).center)
        screen.blit(self.rimage, rect.topleft) 
        
    def draw(self):
        self.rotateim((self.x, self.y))
        
    def movearoun(self):
        rad = math.radians(self.angle)
        self.x -= math.sin(rad)* self.speed
        self.y -= math.cos(rad)* self.speed
        
    def colli(self, mask,x = 0, y = 0 ):
        self.mask = pygame.mask.from_surface(self.rimage)
        offset = [int(self.x - x),int(self.y - y)]
        coll = mask.overlap(self.mask, offset)
        
    
    def beach(self):
        self.speed = -self.speed
        self.movearoun()
        
    def input(player, key):
        movement = False            
        if key[pygame.K_LEFT]:
            if player.speed == 0:
                player.angle += player.rotosp/5
            else:
                player.angle += player.rotosp
        elif key[pygame.K_RIGHT]:
            if player.speed == 0:
                player.angle -= player.rotosp/5
            else:
                player.angle -= player.rotosp
        if key[pygame.K_UP]:
            movement = True
            player.speed = min(player.speed + player.accel, player.maxspeed)
            player.movearoun()
        if key[pygame.K_DOWN]:
            movement = True
            player.speed = max(player.speed - player.accel, player.maxreverse)
            player.movearoun()
        if not movement:
            if player.speed > 0:
                player.speed = max(player.speed - 0.25, 0)
                player.movearoun()
            else:
                player.speed = min(player.speed + 0.25, 0)
                player.movearoun()
                
                
                                                     
menutext = font.render("SHIP GAME", True, "#000000")

menurect = menutext.get_rect(center=(600,100))

play = Button(image=pygame.image.load("img/play.png"), pos=[600,250])

quit = Button(image=pygame.image.load("img/QUIT.png"), pos=[600,400])

p = ship(image = (pygame.image.load("img/ship.png")), pos = [600,300], maxspeed = 5, accel = 0.5, rotospd = 1.5, maxreverse = -3)
islands = pygame.image.load("img/islands.png").convert_alpha()

islandsmask = pygame.mask.from_surface(islands)

running = True

gamestate = "menu"

while running:
    
    screen.fill(colorbg)
    if gamestate == "menu": 
        play.draw(screen)
        quit.draw(screen)
        screen.blit(menutext, menurect)
        
    if gamestate == "play":
        p.draw()
        screen.blit(islands, [0,0])            
        p.input(key = pygame.key.get_pressed())   
        if p.colli(islandsmask):
            p.beach()    
        
    for event in pygame.event.get():
        menu_mousepos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play.interact(menu_mousepos):
                gamestate = "play"
            if quit.interact(menu_mousepos):
                running = False
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
