import pygame
# Import classes
from .platform import *
from .conf import *

def initgen(longueur_totale, SCREEN_WIDTH, SOL_LOG):
    global INC_SPEED
    global sol
    while longueur_totale < SCREEN_WIDTH :
    #on rajoute des bouts de sol, on additionne leur longueur
    #et quand on a couvert tout l'écran on s'arrête.
        plateforme(longueur_totale)          #On en met un nouveau à la position x = longueur_totale.
        longueur_totale += SOL_LONG


def update_sol():
    global sol
    for bloc in sol :
        bloc.move()     #On déplace chaque bloc
        DISPLAYSURF.blit(bloc.image, bloc.rect)
