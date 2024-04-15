import pygame
import math
pygame.init()
pygame.display.set_caption("ship game")
ssize = [1200, 600]
screen = pygame.display.set_mode(ssize)
font = pygame.font.SysFont("Cambria", 100)
colorbg = (0,157,196)
clock = pygame.time.Clock()
FPS = 60


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
    
    def __init__(self, image, pos, maxspeed, accel, rotosp, maxreverse):        
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.rotosp = rotosp
        self.speed = 0
        self.angle = 90
        self.accel = accel
        self.maxspeed = maxspeed
        self.maxreverse = maxreverse
        size = int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)
        self.resizedim = pygame.transform.scale(self.image, size)
        
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
        return coll
    
    def beach(self):
        self.speed = -self.speed
        self.rotosp = -self.rotosp
        self.movearoun()
        
    def input(player, key):
        movement = False
        rotation = {pygame.K_LEFT: 1, pygame.K_RIGHT: -1}
        for direction_key, direction in rotation.items():
            if key[direction_key]:
                player.angle += player.rotosp * direction * (player.speed == 0 and 0.2 or 1)
                movement = True
        if key[pygame.K_UP]:
            movement = True
            player.speed = min(player.speed + player.accel, player.maxspeed)
        elif key[pygame.K_DOWN]:
            movement = True
            player.speed = max(player.speed - player.accel, player.maxreverse)
        if not movement:
            if player.speed > 0:
                player.speed = max(player.speed - 0.25, 0)
            else:
                player.speed = min(player.speed + 0.25, 0)
        if movement:
            player.movearoun()
                                                     
menutext = font.render("SHIP GAME", True, "#000000")

menurect = menutext.get_rect(center=(600,100))

play = Button(image=pygame.image.load("img/play.png"), pos=[600,250])

quit = Button(image=pygame.image.load("img/QUIT.png"), pos=[600,400])

p = ship(image = (pygame.image.load("img/ship.png")), pos = [600,300], maxspeed = 5, accel = 0.5, rotosp = 1.5, maxreverse = -3)
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
        p.input(key = pygame.key.get_pressed())  
        screen.blit(islands, [0,0])            
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

    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
