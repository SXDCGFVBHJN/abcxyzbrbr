from setup import *

class ship(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, maxspeed, accel, rotospd, maxreverse):        
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.rotosp = rotospd
        self.speed = 0
        self.angle = 0
        self.accel = accel
        self.maxspeed = maxspeed
        self.maxreverse = maxreverse
        self.resizedim = scaleimg(self.image, 0.1)
    def rotatel(self):
            self.angle += self.rotosp
    def rotater(self):
            self.angle -= self.rotosp
    def rotateim( self, top_left):
        shipim = pygame.transform.rotate(self.resizedim, self.angle)
        rect= shipim.get_rect(center = self.resizedim.get_rect(topleft = top_left).center)
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
    def colli(self, mask,x = 0, y = 0 ):
        sh_mask = pygame.mask.from_surface(self.image)
        offset = [int(self.x - x),int(self.y - y)]
        coll = mask.overlap(sh_mask, offset)
        return coll
    def beach(self):
        self.speed = -self.speed
class Turret(ship):
    def __init__(self, image, pos):
        self.image = image
     
