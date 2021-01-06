"""Gère l'abstraction de pygame."""

from math import ceil

import sys
import pygame
import src.conf as cf

pygame.init()

Vec = pygame.math.Vector2
"""Classe des vecteurs de dimension 2."""

# le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1
"""Événement d'augmentation de la vitesse."""

# Toutes les secondes on augmente la vitesse
pygame.time.set_timer(INC_SPEED, 1000)

Sprite = pygame.sprite.Sprite
"""Classe des sprites."""

KEYDOWN = pygame.KEYDOWN
"""Événement "touche enfoncée"."""
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
MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
"""Événement "clic de la souris"."""
VIDEORESIZE = pygame.VIDEORESIZE
"""Événement "redimensionnement de la fenêtre"."""
QUIT = pygame.QUIT
"""Événement "quitter le jeu"."""


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


def load_music(path):
    """
    Charge une musique à partir d'un chemin.

    Parameters
    ----------
    path : str
        Chemin du fichier
    """
    pygame.mixer.music.load(path)


def play_music():
    """
    Lance la musique chargée avec load_music.

    Ça boucle automatiquement à la fin.
    """
    pygame.mixer.music.play(-1)

def pause_music():
    """
    Met sur pause la musique chargée avec load_music.

    Ça boucle automatiquement à la fin.
    """
    pygame.mixer.music.pause()

def unpause_music():
    """
    Relance la musique chargée avec load_music.

    Ça boucle automatiquement à la fin.
    """
    pygame.mixer.music.unpause()


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
    game = pygame.Surface((width, height))
    if graphical:
        pygame.display.set_icon(load_image(icon))
        pygame.display.set_caption(title)
        return (game,
                pygame.display.set_mode((width, height),
                                        flags=pygame.RESIZABLE))
    return (game, None)


def resize_window(screen_size):
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


def initialize_clock():
    """
    Initialise le temps.

    Returns
    -------
    Clock
        Une horloge
    """
    return pygame.time.Clock()


def make_event(event_type, attr=None):
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


def resize_list(L, size):
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


def contact(sprite1, sprite2):
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


def collide_group(sprite, group):
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
