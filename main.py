import pygame
import math
pygame.init()
logo = pygame.image.load("img/icon.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("ship game")
screen = pygame.display.set_mode((1200,600))
font = pygame.font.SysFont("Cambria", 100)
colorbg = (0,157,196)
clock = pygame.time.Clock()
FPS = 60
    
def play():
    pygame.init()
    player = ship(image = (pygame.image.load("img/ship1.png")), pos = (600,300), maxspeed = 5, rotospd = 1.5, maxreverse = -3)
    while True:
        screen.fill(colorbg)
        player.draw()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        movement = False
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.rotatel()
        elif key[pygame.K_RIGHT]:
            player.rotater()
        if key[pygame.K_UP]:
            movement = True
            player.movef()
        if key[pygame.K_DOWN]:
            movement = True
            player.mover()
        if not movement:
            if player.speed > 0:
                player.deccel()
            else:
                player.revde()
        pygame.display.update()


def mainmenu():
        pygame.init()
        menutext = font.render("SHIP GAME", True, "#000000")
        menurect = menutext.get_rect(center=(600,100))
        playb = Button(image=pygame.image.load("img/play.png"), pos=(600,250))
        quitb = Button(image=pygame.image.load("img/QUIT.png"), pos=(600,400))
        running = True
        while running:
            screen.fill(colorbg) 
            playb.draw()
            quitb.draw()
            screen.blit(menutext, menurect)
            clock.tick(60)  
            pygame.display.flip()
            for event in pygame.event.get():
                menu_mousepos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playb.interact(menu_mousepos):
                        return play()
                    if quitb.interact(menu_mousepos):
                        running = False
                        pygame.quit()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

class Button():
    def __init__(self, image, pos):
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
    def interact(self,posi):
        if posi[0] in range(self.rect.left, self.rect.right) and posi[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
        
class ship(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, maxspeed, rotospd, maxreverse):        
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.rotosp = rotospd
        self.speed = 0
        self.angle = 0
        self.accel = 0.5
        self.maxspeed = maxspeed
        self.maxreverse = maxreverse
    def rotatel(self):
            self.angle += self.rotosp
    def rotater(self):
            self.angle -= self.rotosp
    def rotateim( self, top_left):
        shipim = pygame.transform.rotate(self.image, self.angle)
        rect= shipim.get_rect(center = self.image.get_rect(topleft = top_left).center)
        screen.blit(shipim, rect.topleft) 
    def draw(self):
        self.rotateim((self.x, self.y))
    def movef(self):
        self.speed = min(self.speed + self.accel, self.maxspeed)
        self.movearoun()
    def mover(self):
        self.speed = max(self.speed - self.accel, self.maxreverse)
        self.movearoun()
    def movearoun(self):
        rad = math.radians(self.angle)
        self.x -= math.sin(rad)* self.speed
        self.y -= math.cos(rad)* self.speed
    def deccel(self):
        self.speed = max(self.speed - 0.25, 0)
        self.movearoun()
    def revde(self):
        self.speed = min(self.speed + 0.25, 0)
        self.movearoun()                           

       

mainmenu()





pygame.quit()
