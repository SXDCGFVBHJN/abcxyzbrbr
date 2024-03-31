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
def scaleimg(img, cons):
    size = int(img.get_width() * cons), int(img.get_height() * cons)
    return pygame.transform.scale(img, size)