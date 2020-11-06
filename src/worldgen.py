""" Gère la génération du monde """
import pygame
# Import classes
import src.platform as pltfrm
import src.conf as cf

import os
import random as rd

modules = os.listdir("./src/modules")
modules = [file.split("_") for file in modules]
modules = [[int(mod[0]), int(mod[1]), mod[2]] for mod in modules]

def initgen(longueur_totale):
    """ Lance la création du sol """
    # on rajoute des bouts de sol, on additionne leur longueur
    # et quand on a couvert tout l'écran on s'arrête.
    while longueur_totale < cf.SCREEN_WIDTH:
        # On en met un nouveau à la position x = longueur_totale.
        pltfrm.Sol(longueur_totale)
        longueur_totale += cf.SOL_LONG
        
def genere_module(last_pltfrm):
    xoffset = last_pltfrm.rect.right + 0
    modules_possibles = [mod for mod in modules if abs(mod[0] - last_pltfrm.rect.top) < 10000]
    module = rd.choice(modules_possibles)
    module_name = '_'.join([str(module[0]), str(module[1]), module[2]])
    module_file = open("./src/modules/" + module_name, "r")
    lines = module_file.readlines()
    module_height = int(lines[0])
    for line in lines[1:]:
        print(line)
        bloc = line.split(';')
        print(bloc)
        top_left = bloc[1][1:-1].split(',')
        top_left_y, top_left_x = (module_height - int(top_left[0])), int(top_left[1])
        bot_right = bloc[2][1:-2].split(',')
        bot_right_y, bot_right_x = (module_height - int(bot_right[0])), int(bot_right[1])
        print(top_left_x + xoffset, top_left_y, (top_left_y - bot_right_y), (top_left_x - bot_right_x))
        pltfrm.Platform(top_left_x + xoffset, top_left_y, (top_left_y - bot_right_y), (bot_right_x - top_left_x))

def update_sol(state):
    """ Met le sol à jour """
    for bloc in cf.sol:
        bloc.move()     # On déplace chaque bloc
        cf.DISPLAYSURF.blit(bloc.image, bloc.rect)
    
    if state == 2:
        for bloc in cf.sol:
            if isinstance(bloc, pltfrm.Sol):
                bloc.stop_creation()
    last_pltfrm = max(cf.sol, key = lambda bloc: bloc.rect.right)
    if last_pltfrm.rect.right < cf.SCREEN_WIDTH:
        print("Enter generation module")
        genere_module(last_pltfrm)
