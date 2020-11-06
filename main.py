""" Gestion du jeu """
import pygame, sys
from pygame.locals import *
import pygame_menu
import random, time

pygame.init()

import src.conf as cf
import src.worldgen as wrld
import src.player as plyr
import src.menu as mn

FPS = 60
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Platformer")

wrld.initgen(0)
INC_SPEED = pygame.USEREVENT + 1        #Crée un nouvel event, le +1 sert à avorir un nouvel ID
pygame.time.set_timer(INC_SPEED, 1000)  #Toutes les secondes on augmente la vitesse
P = plyr.Player()
cf.player_sprite.add(P)

state = 1 # Etat actuel du jeu (1 : dans le menu principal)

while True:
    # print('OK : ', pygame.time.get_ticks())

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            if state == 2: # Si on est in game
                cf.SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    cf.DISPLAYSURF.fill((0,0,0))

    for p in cf.player_sprite:
        cf.DISPLAYSURF.blit(p.image, p.shape)

    P.move()
    wrld.update_sol()

    if state == 1:
        try:
            mn.menu.mainloop(cf.DISPLAYSURF, disable_loop=True)
        except:
            state = 2

    pygame.display.update()
    FramePerSec.tick(FPS)
