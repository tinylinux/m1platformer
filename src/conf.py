""" Stocke des variables partagées entre les différents fichiers """

import os
import pygame
import src.utilities as ut

def listdir(path):
    """listdir sans fichiers cachés (genre les .DS_Store)"""
    return [f for f in os.listdir(path) if not f.startswith('.')]


Vec = pygame.math.Vector2

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# vitesse initiale de défilement du sol
INITIAL_SPEED = 5
SPEED = INITIAL_SPEED
# Drapeau de disponibilité du saut
FLAG_JUMP = False
# Drapeau de disponibilité du second saut
FLAG_JUMP_2 = False

# Couleur du ciel
BlueSky = (0, 170, 251)

# Crée un nouvel event, le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1

# Toutes les secondes on augmente la vitesse
pygame.time.set_timer(INC_SPEED, 1000)

# Compteurs pour le score
SECONDS = 0
FRAMES = 0

# États du jeu :
# 1 : menu de départ
# 2 : jeu en cours
# 3 : menu de fin (scores)
# 4 : affichage des meilleurs scores
STATE = 1

# IMAGES
d = {}
Nom = ["mono", "nuage", "arbre"]
d["mono_factor"] = 3
d["nuage_factor"] = 4
d["arbre_factor"] = 8
for nom in Nom:
    d['n_'+nom] = len(listdir("./assets/img/"+nom))
    d[nom+'_img'] = []
    for i in range(d['n_'+nom]):
        img = ut.load_image("assets/img/"+nom+"/"+nom+str(i)+".png")
        w, h = img.get_rect().size
        img = pygame.transform.scale(img, (d[nom+'_factor'] * w,
                                     d[nom+'_factor'] * h))
        d[nom+'_img'].append(img)

SOL_IMG = ut.load_image("assets/img/sol.png")
PLTFRM_IMG = ut.load_image("assets/img/pltfrm.png")
BAT_IMG = ut.load_image("assets/img/bat.png")

# Dimensions
p_WIDTH, p_HEIGHT = d["mono_img"][0].get_rect().size
w, h = SOL_IMG.get_rect().size
SOL_HAUT = (SCREEN_HEIGHT - h)      # La hauteur du sol en général
SOL_LONG = w      # La longueur d'un bloc du sol en général

# Groupes
sol = ut.group_sprite_define()
nuages = ut.group_sprite_define()
arbres = ut.group_sprite_define()

# La fenêtre principale
DISPLAYSURF = None
WINDOWSURF = None
