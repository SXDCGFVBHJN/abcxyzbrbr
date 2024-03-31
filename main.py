from setup import *
from button import Button
from ship import *
                                        
menutext = font.render("SHIP GAME", True, "#000000")
menurect = menutext.get_rect(center=(600,100))
play = Button(image=pygame.image.load("img/play.png"), pos=[600,250])
quit = Button(image=pygame.image.load("img/QUIT.png"), pos=[600,400])
player = ship(image = (pygame.image.load("img/ship.png")), pos = [600,300], maxspeed = 5, accel = 0.5, rotospd = 1.5, maxreverse = -3)
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
        player.draw()
        screen.blit(islands, [0,0])            
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
        if player.colli(islandsmask):
            player.beach()    
        
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