# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Stocke des variables partagées entre les différents fichiers."""
import os
from enum import Enum

# Screen configurations
SCREEN_WIDTH = 1280
"""Référence de la largeur de l'écran utilisée pour créer le jeu."""

SCREEN_HEIGHT = 720
"""Référence de la hauteur de l'écran utilisée pour créer le jeu."""

FPS = 60
"""Objectif d'images par seconde."""

SRC = os.path.join(os.path.dirname(__file__), '..', 'rollnjump')
"""Chemin vers le dossier src."""
CONFDIR = os.path.join(os.path.dirname(__file__), '..')
"""Chemein vers le dossier contenant les configurations."""
ASSETS = os.path.join(os.path.dirname(__file__), '..', 'rollnjump/assets')
"""Chemin vers le dossier assets."""
UI = os.path.join(ASSETS, 'img', 'ui')
"""Chemin vers le dossier des images de l'interface."""
MUSIC = os.path.join(ASSETS, 'music', 'monozik.ogg')
"""Chemin vers la musique."""
SCORES = os.path.join(CONFDIR, 'score.txt')
"""Chemin vers le fichier contenant les scores."""
MODULES = os.path.join(os.path.dirname(__file__), '..', 'rollnjump', 'modules')
"""Chemin vers le dossier contenant les modules."""

HIGHSCORES_FONT_SIZE = 36
"""Taille des fontes pour les meilleurs scores."""
SCORE_FONT_SIZE = 25
"""Taille des fontes pour les scores."""
RESULT_FONT_SIZE = 50
"""Taille des fontes pour le résultat."""
INPUT_FONT_SIZE = 35
"""Taille des fontes pour les entrées."""
TEXT_FONT_SIZE = 25
"""Taille des fontes pour le texte."""

INITIAL_SPEED = 5
"""Vitesse initiale de défilement du sol."""
SPEED = INITIAL_SPEED
"""Vitesse de défilement du monde."""
ACC = 0.5
"""Accélération de SPEED"""

V_JMP = 15
"""Vitesse initiale lors d'un saut."""
G = 0.8
"""Accélération due à la gravité."""

NB_PLAYERS_MAX = 4
"""Nombre maximal de joueurs."""
NB_PLAYERS = 1
"""Nombre de joueurs."""

# Capture des touches de saut
CAPT = False
"""En cours de capture de touches."""
CAPT_PLYR = 0
"""Numéro du joueur en cours pour changer sa commande."""

NEW_ITEM_TIME = 5
"""Le nombre de secondes avant le prochain objet."""

ITEM_PROBA_MIN = 3
"""Le minimum de NEW_ITEM_TIME lorsque tiré aléatoirement."""
ITEM_PROBA_MAX = 7
"""Le maximum de NEW_ITEM_TIME lorsque tiré aléatoirement."""

ITEM_TIME = {'fast': 40, 'slow': 40, 'little': 200, 'big': 200, 'delay': 5}
"""Dictionnaire avec la durée des effets des items (en nbre de frames)."""

V_ITEM = {'fast': 4, 'slow': -4}
"""Vitesse à laquelle on accélère ou ralentit."""

SIZE_FACTOR = {'little': 1, 'normal': 3, 'big': 8}
"""Facteurs de redimensionnement du joueur."""
SIZE = {'little': (0, 0), 'normal': (0, 0), 'big': (0, 0)}
"""Les différentes dimensions du joueur (normal, big, little)."""

FLAG_MUSIC = True
"""Drapeau indiquant s'il y a de la musique ou non"""

FLAG_ITEM = False
"""
Drapeau indiquant un objet à l'écran ou un effet d'objet.
A pour effet d'empêcher l'apparition d'objets.
"""

# Couleurs
BLACK = (0, 0, 0)
"""Noir."""
GREY = (240, 240, 240)
"""Gris."""
WHITE = (255, 255, 255)
"""Blanc."""
BlueSky = (0, 170, 251)
"""Couleur du ciel."""
IDLE = (170, 170, 170)
"""Couleur d'un bouton inactif."""
HOVER = (100, 100, 100)
"""Couleur d'un bouton sur lequel le pointeur est situé."""

COLORS = ["green", "purple", "red", "white"]
"""Couleurs des joueurs."""

SECONDS = 0
"""Compteur de secondes pour le score."""
FRAMES = 0
"""Compteur des images pour les secondes"""


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
    langchange = 6
    keyset = 7
    multiplayer_set = 8
    credits = 9


STATE = State.menu
"""État du jeu."""

LANG = "NONE"
"""Langue du jeu."""
COLORSTRAD = {
    "fr": ["vert", "violet", "rouge", "blanc"],
    "en": ["green", "purple", "red", "white"]
}
"""Dictionnaire pour la traduction des couleurs."""

DISPLAYSURF = None
"""Surface sur laquelle le jeu est créé."""
WINDOWSURF = None
"""Surface sur laquelle le jeu sera affiché."""
