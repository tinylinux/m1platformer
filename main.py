import pygame, sys
from pygame.locals import *
import random, time


pygame.init()

import src.conf as cf
import src.worldgen as wrld

FPS = 60
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Platformer")

wrld.initgen(0)
INC_SPEED = pygame.USEREVENT + 1        #Crée un nouvel event, le +1 sert à avorir un nouvel ID
pygame.time.set_timer(INC_SPEED, 1000)  #Toutes les secondes on augmente la vitesse

while True:
    # print('OK : ', pygame.time.get_ticks())
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            cf.SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    wrld.update_sol()

    pygame.display.update()
    FramePerSec.tick(FPS)
