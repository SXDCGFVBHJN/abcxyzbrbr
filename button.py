from setup import *
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