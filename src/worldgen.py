import pygame
# Import classes
import src.platform as pltfrm
import src.conf as cf

def initgen(longueur_totale):
    global INC_SPEED
    while longueur_totale < cf.SCREEN_WIDTH :
    #on rajoute des bouts de sol, on additionne leur longueur
    #et quand on a couvert tout l'écran on s'arrête.
        pltfrm.plateforme(longueur_totale)      #On en met un nouveau à la position x = longueur_totale.
        longueur_totale += cf.SOL_LONG


def update_sol():
    for bloc in cf.sol :
        bloc.move()     #On déplace chaque bloc
        cf.DISPLAYSURF.blit(bloc.image, bloc.rect)
