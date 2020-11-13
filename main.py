""" Gestion du jeu """
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
from pygame.locals import *
#import pygame_menu
#import random, time

pygame.init()

import src.conf as cf
import src.worldgen as wrld
import src.player as plyr
#import src.background as bg
import src.menu as mn

FPS = 60
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Platformer")

wrld.initgen()
# Crée un nouvel event, le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1
# Toutes les secondes on augmente la vitesse
pygame.time.set_timer(INC_SPEED, 1000)

P = plyr.Player()
#bg = bg.Background()

def score(n):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(n), True, (255, 255, 255))
    cf.DISPLAYSURF.blit(text,(0,0))

seconds = 0
count_frames = 0

# États du jeu :
# 1 : menu de départ
# 2 : jeu en cours
# 3 : menu de fin (scores)
state = 1

while True:
    # print('OK : ', pygame.time.get_ticks())

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            if state == 2: # Si on est in game
                cf.SPEED += 0.5
        if event.type == pygame.KEYDOWN:
            if state == 2 and event.key == K_SPACE:
                P.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 1 and mn.start_button.click(pygame.mouse.get_pos()):
                state = 2
            elif state == 3 and mn.restart_button.click(pygame.mouse.get_pos()):
                # On réinitialise le monde
                P = plyr.Player()
                cf.SPEED = cf.INITIAL_SPEED
                seconds = 0
                count_frames = 0
                cf.sol = pygame.sprite.Group()
                cf.nuages = pygame.sprite.Group()
                cf.arbres = pygame.sprite.Group()
                wrld.initgen()
                state = 2
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    cf.DISPLAYSURF.fill(cf.BlueSky)

    wrld.update(state)

    if state == 2:
        count_frames += 1
        if count_frames == 60:
            count_frames = 0
            seconds += 1
        score(seconds)

    P.move()

    if P.death():
        state = 3

    if state == 1:
        mn.start_button.print(pygame.mouse.get_pos())

    if state == 3:
        mn.restart_button.print(pygame.mouse.get_pos())

    pygame.display.flip()
    FramePerSec.tick(FPS)
