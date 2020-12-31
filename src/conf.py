"""Stocke des variables partagées entre les différents fichiers."""
from enum import Enum

# Screen configurations
SCREEN_WIDTH = 1280
"""Référence de la largeur de l'écran utilisée pour créer le jeu"""

SCREEN_HEIGHT = 720
"""Référence de la hauteur de l'écran utilisée pour créer le jeu"""

FPS = 60
"""Objectif d'images par seconde"""

SEED = 0
"""Pour le générateur de nombres aléatoires"""

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


# États du jeu
class State(Enum):
    """Type énuméré pour l'état du jeu."""

    languages = 0
    menu = 1
    ingame = 2
    gameover = 3
    highscore = 4
    setup = 5


STATE = State.menu
"""État du jeu"""

DISPLAYSURF = None
"""Surface sur laquelle le jeu est créé"""
WINDOWSURF = None
"""Surface sur laquelle le jeu sera affiché"""

# Flag : true si y a un item à l'écran
# ou qu'on est dans un état spécial à cause d'un item
FLAG_ITEM = False
