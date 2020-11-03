""" Gestion du jeu """
import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

import src.conf as cf
import src.worldgen as wrld
import src.player as plyr
import src.background as bg

FPS = 60
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Platformer")

wrld.initgen(0)
# Crée un nouvel event, le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1
# Toutes les secondes on augmente la vitesse
pygame.time.set_timer(INC_SPEED, 1000)
P = plyr.Player()

bg = bg.Background()

state = 1 # Etat actuel du jeu (1 : dans le menu principal)

while True:
    # print('OK : ', pygame.time.get_ticks())
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            if state == 2:  # Si on est in game
                cf.SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    bg.update()

    wrld.update_sol()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_SPACE]:
        P.jump()

    P.move()

    pygame.display.update()
    FramePerSec.tick(FPS)
