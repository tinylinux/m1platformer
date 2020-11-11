""" Gère la génération du monde """
import pygame, random
# Import classes
import src.platform as plt
import src.conf as cf
import src.background as bg

import os
import random as rd

# Indexation des modules
modules = os.listdir("./src/modules")
modules = [file.split("_") for file in modules]
modules = [[int(mod[0]), int(mod[1]), mod[2]] for mod in modules]

MAX_JUMP = 10000 # La hauteur maximale entre la dernière plateforme d'un module
# et la première d'un nouveau module

def initgen():
    #Lance la création du sol
    
    # on rajoute des bouts de sol, on additionne leur longueur
    # et quand on a couvert tout l'écran on s'arrête.
    longueur_totale=0
    while longueur_totale < cf.SCREEN_WIDTH:
        # On en met un nouveau à la position x = longueur_totale.
        plt.Sol(longueur_totale)
        longueur_totale += cf.SOL_LONG
    #Crée quelques nuages
    for k in range(4) :
        x = random.randint(0,cf.SCREEN_WIDTH)
        y = random.randint(0,cf.SCREEN_HEIGHT//2)
        i = random.randint(0,3)
        bg.Nuage(x,y,i)


        
def genere_module(last_pltfrm):
    """ Choisit et affiche un nouveau module à la fin de l'écran"""
    # Début du nouveau module
    xoffset = last_pltfrm.rect.right + 0
    # Sélection des modules possibles
    modules_possibles = [mod for mod in modules if abs(mod[0] - last_pltfrm.rect.top) < MAX_JUMP]
    # Choix aléatoire d'un module
    module = rd.choice(modules_possibles)
    # Chargement du module
    module_name = '_'.join([str(module[0]), str(module[1]), module[2]])
    module_file = open("./src/modules/" + module_name, "r")
    lines = module_file.readlines()
    module_height = int(lines[0])
    yoffset = cf.SCREEN_HEIGHT - module_height
    for line in lines[1:]:
        bloc = line.split(';')
        top_left = bloc[1][1:-1].split(',')
        top_left_y, top_left_x = int(top_left[0]), int(top_left[1])
        bot_right = bloc[2][1:-2].split(',')
        bot_right_y, bot_right_x = int(bot_right[0]), int(bot_right[1])
        plt.Platform(top_left_x + xoffset, top_left_y + yoffset, (bot_right_y - top_left_y), (bot_right_x - top_left_x))
    module_file.close()

def update(state):
    for nuage in cf.nuages :
        nuage.update()
    for bloc in cf.sol:
        bloc.update()     # On déplace chaque bloc
    
    if state == 2:
        last_pltfrm = max(cf.sol, key = lambda bloc: bloc.rect.right)
        #print(last_pltfrm.rect.right)
        if last_pltfrm.rect.right <= cf.SCREEN_WIDTH:
            print("Enter generation module")
            genere_module(last_pltfrm)
