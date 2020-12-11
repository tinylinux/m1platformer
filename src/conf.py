""" Stocke des variables partagées entre les différents fichiers """

import pygame


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

# La fenêtre principale
DISPLAYSURF = None
WINDOWSURF = None
