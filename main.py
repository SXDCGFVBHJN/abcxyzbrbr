#import pygame library
import pygame  
#import math library    
import math  
#initialize pygame modules       
pygame.init()      
#set window caption
pygame.display.set_caption("ship game")   
#set window size    
ssize = [1200, 600]
#display window to the screen
screen = pygame.display.set_mode(ssize)
#get font from system 
font = pygame.font.SysFont("Cambria", 100)
#color for background in RGB code(light blue)
colorbg = (0,157,196)
#create clock
clock = pygame.time.Clock()
#game FPS
FPS = 60

#create button class 
class Button():
    #define the init function and get self, image and position
    def __init__(self, image, pos):
        #set self image as the image parameter 
        self.image = image
        #set self position to pos
        self.pos = pos
        #create a rectangle for the image representing the position
        self.rect = self.image.get_rect(center=(self.pos))
    #define the interact function and gets self and the mouse position   
    def interact(self,mouspos):
        #check the position x and y of the mouse if it's in the button rectangle 
        if mouspos[0] in range(self.rect.left, self.rect.right) and mouspos[1] in range(self.rect.top, self.rect.bottom):
            #return True if the requirements are met
            return True
#create ship class
class ship(pygame.sprite.Sprite):
    #define the init fuction and takes in self, image and position 
    def __init__(self, image, pos):
        #set the self image as the image parameter        
        self.image = image
        #set position to pos
        self.pos = pos
        #set rotation speed
        self.rotosp = 1.5
        #set current speed
        self.speed = 0
        #set current angle
        self.angle = 90
        #set acceleration
        self.accel = 1
        #set max speed
        self.maxspeed = 10
        #set max reverse speed
        self.maxreverse = -3
    #define draw function
    def draw(self):
        #set the size of the ship as the interger result of the default size times 0.1
        size = int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)
        #transform the image into the size above
        self.resizedim = pygame.transform.scale(self.image, size)
        #set the rotated image as the resized image and the angle
        self.rimage = pygame.transform.rotate(self.resizedim, self.angle)
        #show the rotated image to the screen
        screen.blit(self.rimage, self.pos) 
    #define the move around function   
    def movearoun(self):
        #transform the angle into radians using math library
        rad = math.radians(self.angle)
        #get the x and y coordinates by subtracting the value of the sin for x and cos for y times current speed 
        self.pos[0] -= math.sin(rad)* self.speed
        self.pos[1] -= math.cos(rad)* self.speed
    #define collision function    
    def colli(self, mask):
        #set the mask as the rotated image
        self.mask = pygame.mask.from_surface(self.rimage)
        #set the offset as the integer of the coordinates
        offset = (int(self.pos[0]),int(self.pos[1]))
        #set collision to check for the point of intersection
        coll = mask.overlap(self.mask, offset)
        #return the collision variable
        return coll
    #define beach function
    def beach(self):
        #set speed as negative speed
        self.speed = -self.speed
        #call out the movearound function
        self.movearoun()
    #define input function and takes in the player and key
    def input(player, key):
        #set movement as false
        movement = False
        #create a dictionary to map arrow keys to rotation directions and set the corresponding key to the value -1 and 1
        rotation = {pygame.K_LEFT: 1, pygame.K_RIGHT: -1}
        #iterate through key value in the rotation dictionary
        for dir_key, rot in rotation.items():
            #check if the corresponding arrow key is pressed
            if key[dir_key]:
                    #check if speed = 0
                    if player.speed == 0:
                    #slower rotation
                        player.angle += player.rotosp * rot/5
                    else:
                    # Standard rotation
                        player.angle += player.rotosp * rot
        #check if key is the up arrow key
        if key[pygame.K_UP]:
            #change movement to True
            movement = True
            #set the speed as the minimum value between the current speed + acceleration and max speed
            player.speed = min(player.speed + player.accel, player.maxspeed)
        #check if key is the down arrow key
        elif key[pygame.K_DOWN]:
            #change movement to True
            movement = True
            #set the speed as the maximum value between the current speed - acceleration and max reverse speed
            player.speed = max(player.speed - player.accel, player.maxreverse)
        #check if movement is False
        if movement == False:
            #check if speed is above 0 
            if player.speed > 0:
                #set the speed as the maximum value between the current speed - 1 and 0
                player.speed = max(player.speed - 1, 0)
            else:
                #set the speed as the minimum value between the current speed + 1 and 0
                player.speed = min(player.speed + 1, 0)
        #calling out the movearound function
        player.movearoun()
#render text "SHIP GAME" onto a surface using the font variable, antialiasing, and black color
menutext = font.render("SHIP GAME", True, "#000000")
#rectangle representing the position of the rendered text
menurect = menutext.get_rect(center=(600,100))
#Create a Button object representing the "play" button
play = Button(image=pygame.image.load("img/play.png"), pos=[600,250])
#Create a Button object representing the "quit" button
quit = Button(image=pygame.image.load("img/QUIT.png"), pos=[600,400])
#Create a ship object representing the player
p = ship(image = (pygame.image.load("img/ship.png")), pos = [600,300])
#load the islands image
islands = pygame.image.load("img/islands.png")
#get mask from the islands image
islandsmask = pygame.mask.from_surface(islands)
#set running as True
running = True
#set gamestate as menu
gamestate = "menu"
# main script 
while running:
    # fill the screen with the color light blue 
    screen.fill(colorbg)
    #check if the gamestate is menu
    if gamestate == "menu": 
        #display the button image and the menu text to the screen and the rect as its position
        screen.blit(play.image, play.rect)
        screen.blit(quit.image, quit.rect)
        screen.blit(menutext, menurect)
    #check if the gamestate is play   
    if gamestate == "play":
        #p calling out draw function
        p.draw()
        #p calling out the input function and takes in the key variable as it uses pygame to detect the key pressed
        p.input(key = pygame.key.get_pressed())
        #display the island picture to the screen at the coordinates 0,0  
        screen.blit(islands, [0,0])            
        #check if there's any collision between the island mask and the ship mask
        if p.colli(islandsmask):
        #calling out the beach fuction when met
            p.beach()    
    #iterate the events in every events that pygame gets  
    for event in pygame.event.get():
        #get the mouse position
        mousepos = pygame.mouse.get_pos()
        #check if the event type is mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check if the mouse click position is in one of the buttons
            if play.interact(mousepos):
                #change gamestate to play
                gamestate = "play"
            if quit.interact(mousepos):
                #set running as false
                running = False
        #check if the event type is quit
        if event.type == pygame.QUIT:
            #set running as false
            running = False

    #make the game runs 60 frames per seconds
    clock.tick(FPS)
    #update the screen
    pygame.display.update()
#quit pygame
pygame.quit()
