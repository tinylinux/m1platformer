"""Gère l'abstraction de pygame."""

from math import ceil

import sys
import pygame
import src.conf as cf

pygame.init()

Vec = pygame.math.Vector2

# Crée un nouvel event, le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1

# Toutes les secondes on augmente la vitesse
pygame.time.set_timer(INC_SPEED, 1000)

Sprite = pygame.sprite.Sprite

# pygame events
KEYDOWN = pygame.KEYDOWN
K_SPACE = pygame.K_SPACE
K_RETURN = pygame.K_RETURN
K_s = pygame.K_s
K_BACKSPACE = pygame.K_BACKSPACE
MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
VIDEORESIZE = pygame.VIDEORESIZE
QUIT = pygame.QUIT


def keyname(key):
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


def load_image(path):
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


def initialize_window(icon, title, width, height, graphical):
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
    if graphical:
        pygame.display.set_icon(load_image(icon))
        pygame.display.set_caption(title)
        return (pygame.Surface((width, height)),
                pygame.display.set_mode((width, height),
                                        flags=pygame.RESIZABLE))
    return (pygame.Surface((width, height)), None)


def resize_window(screen_size):
    """
    Rétablit le ratio après un redimensionnement de fenêtre.

    Parameters
    ----------
    screen_size : int * int
        Taille de la fenêtre, au ratio quelconque
    """
    ratio = min(screen_size[0]/cf.SCREEN_WIDTH,
                screen_size[1]/cf.SCREEN_HEIGHT)
    new_screen_size = (ceil(ratio * cf.SCREEN_WIDTH),
                       ceil(ratio * cf.SCREEN_HEIGHT))
    cf.WINDOWSURF = pygame.display.set_mode(new_screen_size,
                                            flags=pygame.RESIZABLE)


def initialize_clock():
    """
    Initialise le temps.

    Returns
    -------
    Clock
        Une horloge
    """
    return pygame.time.Clock()


def get_events():
    """
    Renvoie la liste des évènements.

    Returns
    -------
    Event list
        Liste des évènements
    """
    return pygame.event.get()


def group_sprite_define():
    """
    Création d'un nouveau groupe de sprites.

    Returns
    -------
    Group
        le groupe de sprites
    """
    return pygame.sprite.Group()


def add_to_group(sprite, group):
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


def resize(surface, dimensions, destination=None):
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


def update_screen():
    """Met à jour l'écran."""
    pygame.display.flip()


def get_screen_size():
    """
    Renvoie la taille de la fenêtre.

    Returns
    -------
    int * int
        Dimensions de la fenêtre
    """
    return pygame.display.get_surface().get_size()


def create_rect(array):
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


def draw_rect(surface, color, rect):
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


def mouse_pos():
    """
    Renvoie la position de la souris.

    Returns
    -------
    int * int
        La position du pointeur
    """
    return pygame.mouse.get_pos()


def quit_game():
    """Quitte le jeu."""
    pygame.quit()
    sys.exit()


def font(font_name, size):
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
            self.kill()              # on le supprime
        # On met à jour l'image
        cf.DISPLAYSURF.blit(self.image, self.rect)
