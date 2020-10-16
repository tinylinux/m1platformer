import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Display configuration for user
ch, cw = pygame.display.Info().current_h, pygame.display.Info().current_w

SCREEN_WIDTH = (cw * 5)//7
SCREEN_HEIGHT = min((ch * 8)//9, 9*SCREEN_WIDTH//16)

ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Platformer")

while True:
    # print('OK : ', pygame.time.get_ticks())
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    FramePerSec.tick(FPS)
