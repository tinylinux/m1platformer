# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Gère l'abstraction de pygame."""

import re
from math import ceil

import sys
import pygame
import rollnjump.conf as cf

pygame.init()

# Classes
Vec = pygame.math.Vector2
"""Classe des vecteurs de dimension 2."""
Sprite = pygame.sprite.Sprite
"""Classe des sprites."""

# Les touches
KEYDOWN = pygame.KEYDOWN
"""Événement "touche enfoncée"."""
K_ESCAPE = pygame.K_ESCAPE
"""Touche échap."""
K_SPACE = pygame.K_SPACE
"""Touche espace."""
K_RETURN = pygame.K_RETURN
"""Touche entrée."""
K_s = pygame.K_s
"""Touche S."""
K_u = pygame.K_u
"""Touche U."""
K_BACKSPACE = pygame.K_BACKSPACE
"""Touche retour."""
K_ESCAPE = pygame.K_ESCAPE
"""Touche échap"""
MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
"""Événement "clic de la souris"."""
VIDEORESIZE = pygame.VIDEORESIZE
"""Événement "redimensionnement de la fenêtre"."""
QUIT = pygame.QUIT
"""Événement "quitter le jeu"."""


def keyname(key):  # pragma: no cover
    """
    Renvoie le nom de la touche pressée.

    Parameters
    ----------
    key : Key
        Touche pressée

    Returns
    -------
    str
        Nom de la touche
    """
    return pygame.key.name(key)


def keyidentifier(control):  # pragma: no cover
    """
    Renvoie la touche à partir d'une chaîne de caractères.

    Parameters
    ----------
    control : str
        Texte caractérisant la touche

    Returns
    -------
    Key
        Variable de la touche
    """
    return pygame.key.key_code(control)


def load_image(path):  # pragma: no cover
    """
    Charge une image à partir d'un chemin.

    Parameters
    ----------
    path : str
        Chemin du fichier

    Returns
    -------
    Surface
        Image du fichier
    """
    return pygame.image.load(path)


def load_music(path):  # pragma: no cover
    """
    Charge une musique à partir d'un chemin.

    Parameters
    ----------
    path : str
        Chemin du fichier
    """
    pygame.mixer.music.load(path)


def play_music():  # pragma: no cover
    """
    Lance la musique chargée avec load_music.

    Boucle automatiquement à la fin du fichier.
    """
    pygame.mixer.music.play(-1)


def pause_music():  # pragma: no cover
    """Met sur pause la musique chargée avec load_music."""
    pygame.mixer.music.pause()


def unpause_music():  # pragma: no cover
    """Relance la musique chargée avec load_music."""
    pygame.mixer.music.unpause()


def initialize_window(icon, title, width,
                      height, graphical):  # pragma: no cover
    """
    Initialise l'environnement graphique et la fenêtre.

    Parameters
    ----------
    icon : Surface
        Icone de la fenêtre
    title : str
        Nom de la fenêtre
    width : int
        Largeur de la fenêtre
    height : int
        Hauteur de la fenêtre
    graphical : bool
        Indique si la fenêtre doit être affichée

    Returns
    -------
    Surface * Surface
        Un couple (surface de jeu, surface à afficher)
    """
    game = pygame.Surface((width, height))
    if graphical:
        pygame.display.set_icon(load_image(icon))
        pygame.display.set_caption(title)
        return (game,
                pygame.display.set_mode((width, height),
                                        flags=pygame.RESIZABLE))
    return (game, None)


def resize_window(screen_size):  # pragma: no cover
    """
    Rétablit le ratio après un redimensionnement de fenêtre.

    Parameters
    ----------
    screen_size : int * int
        Taille de la fenêtre, au ratio quelconque
    """
    ratio = min(screen_size[0] / cf.SCREEN_WIDTH,
                screen_size[1] / cf.SCREEN_HEIGHT)
    new_screen_size = (ceil(ratio * cf.SCREEN_WIDTH),
                       ceil(ratio * cf.SCREEN_HEIGHT))
    cf.WINDOWSURF = pygame.display.set_mode(new_screen_size,
                                            flags=pygame.RESIZABLE)


def initialize_clock():  # pragma: no cover
    """
    Initialise le temps.

    Returns
    -------
    Clock
        Une horloge
    """
    return pygame.time.Clock()


def make_event(event_type, attr=None):  # pragma: no cover
    """
    Renvoie un événement du type passé en entrée.

    Parameters
    ----------
    event_type : int
        Le type de l'événement
    attr : dict, optionnel
        Le dictionnaire des attributs

    Returns
    -------
    Event
        L'événement correspondant
    """
    if attr is None:
        attr = {}
    return pygame.event.Event(event_type, attr)


def get_events():  # pragma: no cover
    """
    Renvoie la liste des évènements.

    Returns
    -------
    Event list
        Liste des évènements
    """
    return pygame.event.get()


def group_sprite_define():  # pragma: no cover
    """
    Création d'un nouveau groupe de sprites.

    Returns
    -------
    Group
        le groupe de sprites
    """
    return pygame.sprite.Group()


def add_to_group(sprite, group):  # pragma: no cover
    """
    Ajoute un sprite à un groupe de sprites.

    Parameters
    ----------
    sprite : Sprite
        Le sprite à ajouter
    group : Group
        Le groupe de sprites
    """
    group.add(sprite)


def resize(surface, dimensions, destination=None):  # pragma: no cover
    """
    Change l'échelle de la surface en entrée.

    Parameters
    ----------
    surface : Surface
        La surface à modifier
    dimensions : int * int
        Les nouvelles dimensions
    destination : Surface, optionnel
        Nouvel objet à créer pour le redimensionnement

    Returns
    -------
    Surface
        Surface redimensionnée
    """
    if destination is None:
        return pygame.transform.scale(surface, dimensions)
    return pygame.transform.scale(surface, dimensions, destination)


def resize_list(L, size):  # pragma: no cover
    """
    Redimensionne les images d'une liste.

    Parameters
    ----------
    L : Surface list
        Liste d'images
    size : int * int
        La résolution attendue

    Returns
    -------
    Surface list
        La liste des images redimensionnées
    """
    for i, img in enumerate(L):
        L[i] = pygame.transform.scale(img, size)


def contact(sprite1, sprite2):  # pragma: no cover
    """
    Indique si deux sprites sont en contact.

    Parameters
    ----------
    sprite1 : Sprite
        Le premier sprite
    sprite2 : Sprite
        Le second sprite

    Returns
    -------
    bool
        True si les deux sprites sont en contact
    """
    return pygame.sprite.collide_rect(sprite1, sprite2)


def collide_group(sprite, group):  # pragma: no cover
    """
    Indique s'il y a une collision entre un sprite et un groupe de sprites.

    Parameters
    ----------
    sprite : Sprite
        Le sprite examiné
    group : Sprite group
        Le groupe de sprites examiné

    Returns
    -------
    bool
        True s'il y a une collision
    """
    return pygame.sprite.spritecollideany(sprite, group)


def update_screen():  # pragma: no cover
    """Met à jour l'écran."""
    pygame.display.flip()


def get_screen_size():  # pragma: no cover
    """
    Renvoie la taille de la fenêtre.

    Returns
    -------
    int * int
        Dimensions de la fenêtre
    """
    return pygame.display.get_surface().get_size()


def create_rect(array):  # pragma: no cover
    """
    Crée un objet rectangle.

    Parameters
    ----------
    array : int list
        liste contenant l'abscisse de la gauche du rectangle,
        l'ordonnée du haut du rectangle,
        sa largeur et sa hauteur

    Returns
    -------
    Rect
        Le rectangle correspondant
    """
    return pygame.Rect(array)


def draw_rect(surface, color, rect):  # pragma: no cover
    """
    Dessine l'objet rectangle sur une surface.

    Parameters
    ----------
    surface : Surface
        La surface sur laquelle afficher le rectangle
    color : int * int * int
        La couleur (en RGB)
    rect : Rect
        Le rectangle à afficher
    """
    pygame.draw.rect(surface, color, rect)


def mouse_pos():  # pragma: no cover
    """
    Renvoie la position de la souris.

    Returns
    -------
    int * int
        La position du pointeur
    """
    return pygame.mouse.get_pos()


def quit_game():  # pragma: no cover
    """Quitte le jeu."""
    pygame.quit()
    sys.exit()


def font(font_name, size):  # pragma: no cover
    """
    Renvoie une fonte de la taille demandée.

    Parameters
    ----------
    font_name : str
        La police de caractères
    size : int
        La taille de la fonte

    Returns
    -------
    Font
        La fonte
    """
    return pygame.font.Font(font_name, size)


def collide(obj, pos_next, rect):
    """
    Gestion des collisions.

    Parameters
    ----------
    obj : Player / Item
        objet (joueur ou objet) dont on examine la collision
    pos_next : Vector2
        position suivante de l'objet
    rect : Rect
        ce qui est potentiellement en collision avec l'objet

    Returns
    -------
    bool * bool * Vector2
        un triplet (collision verticale, collision horizontale,
        modification de position necessaire)
    """
    # On ne tient pas compte du cas dans lequel l'objet traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes façons pas possible de jouer dans ce cas.
    pos_prev = obj.pos

    if pos_next.x + obj.width > rect.left\
            and pos_next.x < rect.right:
        # Dans la plateforme horizontalement

        if pos_prev.y + obj.height <= rect.top:
            # Position initale au-dessus de la plateforme
            if pos_next.y + obj.height > rect.top:
                # Nouvelle position dans ou sous la plateforme
                obj.FLAG_JUMP = True
                return (True, False,
                        Vec(pos_next.x, rect.top - obj.height))

        elif pos_prev.y >= rect.bottom:
            # Position initiale en-dessous de la plateforme
            if pos_next.y < rect.bottom:
                # Nouvelle position dans ou au-dessus de la plateforme
                return (True, False, Vec(pos_next.x, rect.bottom))

        elif pos_next.y + obj.height > rect.top\
                and pos_next.y < rect.bottom:
            # On ne considère que les collisions à gauche des plateformes
            return (False, True, Vec(rect.left - obj.width, pos_next.y))

    return(False, False, None)


def update_pos_vel(obj, ground):
    """
    Met à jour la position et la vitesse de l'objet.

    Parameters
    ----------
    obj : Player / Item
        L'objet à mettre à jour
    ground : Sprite group
        Le groupe des plateformes
    """
    obj.vel += obj.acc
    posnext = obj.pos + obj.vel + 0.5 * obj.acc

    for plat in ground:  # Gestion des collisions
        coll = collide(obj, posnext, plat.rect)
        if coll[0] or coll[1]:
            posnext = coll[2]
            if coll[0]:
                obj.vel.y = 0
            if coll[1]:
                obj.vel.x = 0

    obj.pos = posnext
    obj.rect.topleft = obj.pos  # Mise à jour de la position


def onlydigits(value):
    """
    Filtre `value` pour ne garder que les chiffres.

    On peut ainsi retirer toutes les sauts de lignes présents
    dans le fichier `score.txt`.

    Parameters
    ----------
    value : str
        La chaîne à filtrer

    Returns
    -------
    str
        La chaîne obtenue après filtrage
    """
    final_chain = ""
    for i in value:
        if '0' <= i <= '9':
            final_chain += i
    return final_chain


def onlyalphanum(value):
    """
    Filtre `value` pour ne garder que les caractères alphanumériques.

    Parameters
    ----------
    value : str
        La chaîne à filtrer

    Returns
    -------
    str
        La chaîne obtenue après filtrage
    """
    return re.sub(r'[^A-Za-z0-9]+', '', value)


class GameObject(Sprite):
    """
    Classe des objets du monde (hors joueur).

    Attributes
    ----------
    pos : int * int
        Position de l'objet
    scroll : float
        Vitesse de déplacement
    image : Sprite
        Image de l'objet
    rect : Rect
        Rectangle encadrant l'objet
    FLAG_creation : bool
        Drapeau pour gérer la création des objets
    """

    def __init__(self, position, scroll, image):
        """
        Initialisation.

        Parameters
        ----------
        position : int * int
            Position de l'objet
        scroll : float
            Vitesse de déplacement
        image : Sprite
            image de l'objet
        """
        super().__init__()
        self.pos = Vec(position)
        self.scroll = scroll
        # À 0 l'objet ne bouge pas,
        # À 1 l'objet se déplace à la vitesse du sol
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        # Limite à partir de laquelle on génère un nouvel objet sur sa droite
        # FLAG_creation est un flag pour ne générer qu'un seul nouvel objet
        self.FLAG_creation = True

    def update(self):
        """Met à jour le vecteur position."""
        posnext = self.pos + self.scroll * Vec(-cf.SPEED, 0)
        self.pos = posnext
        self.rect.topleft = self.pos
        if self.rect.right < 0:     # si l'objet sort de l'écran
            # print(self)
            self.kill()              # on le supprime
        # On met à jour l'image
        cf.DISPLAYSURF.blit(self.image, self.rect)
