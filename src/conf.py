"""Stocke des variables partagées entre les différents fichiers."""
import os
from enum import Enum

# Screen configurations
SCREEN_WIDTH = 1280
"""Référence de la largeur de l'écran utilisée pour créer le jeu"""

SCREEN_HEIGHT = 720
"""Référence de la hauteur de l'écran utilisée pour créer le jeu"""

FPS = 60
"""Objectif d'images par seconde"""

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets')
"""Chemin vers le dossier assets"""

UI = os.path.join(ASSETS, 'img', 'ui')
"""Chemin vers le dossier des images de l'interface"""

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

G = 0.8
"""Accélération due à la gravité"""

FLAG_JUMP = False
"""Drapeau de disponibilité du saut"""

FLAG_JUMP_2 = False
"""Drapeau de disponibilité du second saut"""

# Drapeau qui dit si y a un item à l'écran
# ou qu'on est dans un état spécial à cause d'un item
# mettre à True si on veut pas d'items
FLAG_ITEM = False

# Dans combien de secondes on crée un nouvel item
NEW_ITEM_TIME = 1

# Les bornes de NEW_ITEM_TIME lorsque tiré aléatoirement
ITEM_PROBA_MIN = 1
ITEM_PROBA_MAX = 2

# Dico avec la durée des effets des items (en nbre de frames)
ITEM_TIME = {'fast': 40, 'slow': 40, 'little': 200, 'big': 200}

# vitesse à laquelle on accélère ou ralentit
VEL = {'fast': 4, 'slow': -4}

# facteur de resize du monocycle
# après initialisation des images, ça n'est plus un facteur de resize
# mais une size en pixels
# par exemple SIZE['little'] vaudra (21,32)
SIZE = {'little': 1, 'normal': 3, 'big': 8}

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

MUSIC = os.path.join(ASSETS, 'music', 'monozik.mp3')
"""Chemin vers la musique"""

# États du jeu
class State(Enum):
    """Type énuméré pour l'état du jeu."""

    languages = 0
    menu = 1
    ingame = 2
    gameover = 3
    gameover_multi = 3.5
    highscore = 4
    setup = 5


STATE = State.menu
"""État du jeu"""

LANG = "NONE"
"""Langue du jeu"""

DISPLAYSURF = None
"""Surface sur laquelle le jeu est créé"""
WINDOWSURF = None
"""Surface sur laquelle le jeu sera affiché"""

# Nombre maximal de joueurs
NB_PLAYERS_MAX = 3
# Nombre de joueurs
NB_PLAYERS = 3

# Vitesse initiale lors d'un saut
V_JMP = 15
# Accélération due à la gravité
G = 0.8

# Flag : true si y a un item à l'écran
# ou qu'on est dans un état spécial à cause d'un item
FLAG_ITEM = False
