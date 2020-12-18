""" Stocke des variables partagées entre les différents fichiers """

SCREEN_WIDTH = 1280
"""Référence de la largeur de l'écran utilisée pour créer le jeu"""

SCREEN_HEIGHT = 720
"""Référence de la hauteur de l'écran utilisée pour créer le jeu"""

FPS = 60
"""Objectif d'images par seconde"""

HIGHTSCORES_FONT_SIZE = 36
"""Taille des fontes pour les meilleurs scores"""
SCORE_FONT_SIZE = 25
"""Taille des fontes pour les scores"""
RESULT_FONT_SIZE = 50
"""Taille des fontes pour le résultat"""
INPUT_FONT_SIZE = 35
"""Taille des fontes pour les entrées"""
TEXT_FONT_SIZE = 25
"""Taille des fontes pour le texte"""

INITIAL_SPEED = 5
"""Vitesse initiale de défilement du sol"""
SPEED = INITIAL_SPEED

FLAG_JUMP = False
"""Drapeau de disponibilité du saut"""

FLAG_JUMP_2 = False
"""Drapeau de disponibilité du second saut"""

# Couleurs
BLACK = (255, 255, 255)
"""Noir"""
GREY = (240, 240, 240)
"""Gris"""
WHITE = (255, 255, 255)
"""Blanc"""
BlueSky = (0, 170, 251)
"""Couleur du ciel"""
IDLE = (170, 170, 170)
"""Couleur d'un bouton inactif"""
HOVER = (100, 100, 100)
"""Couleur d'un bouton sur lequel le pointeur est situé"""

SECONDS = 0
"""Compteur de secondes pour le score"""
FRAMES = 0
"""Compteur des images pour les secondes"""

# États du jeu :
# 1 : menu de départ
# 2 : jeu en cours
# 3 : menu de fin (scores)
# 4 : affichage des meilleurs scores
STATE = 1
"""État actuel du jeu"""

DISPLAYSURF = None
"""Surface sur laquelle le jeu est créé"""
WINDOWSURF = None
"""Surface sur laquelle le jeu sera affiché"""
