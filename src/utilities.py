"""Gère l'abstraction de pygame par la (re)définition de fonctions"""

from math import ceil

import sys
import pygame
import src.conf as cf

Vec = pygame.math.Vector2

# Crée un nouvel event, le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1

# Toutes les secondes on augmente la vitesse
pygame.time.set_timer(INC_SPEED, 1000)

Sprite = pygame.sprite.Sprite

# pygame events
KEYDOWN = pygame.KEYDOWN
K_SPACE = pygame.K_SPACE
K_BACKSPACE = pygame.K_BACKSPACE
MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
VIDEORESIZE = pygame.VIDEORESIZE
QUIT = pygame.QUIT


def keyname(key):
    """
    Renvoie le nom de la touche pressée
    """
    return pygame.key.name(key)


def initialize():
    """
    Initialiser l'environnement Pygame
    """
    return pygame.init()


def load_image(path):
    """
    Charger une image à partir de path
    """
    return pygame.image.load(path)


def initialize_window(icon, title, width, height, graphical):
    """
    Initialiser les variables d'environnement graphique
    et initialisation des paramètres
    de fenêtre
    """
    pygame.display.set_icon(
        load_image(icon))
    pygame.display.set_caption(title)
    if graphical:
        return (pygame.Surface((width, height)),
                pygame.display.set_mode((width, height),
                                        flags=pygame.RESIZABLE))
    return (pygame.Surface((width, height)), None)


def resize_window(screen_size):
    """
    Redimensionne la fenêtre, en gardant le ratio
    screen_size : int*int, taille actuelle, mais pas au bon ratio.
    """
    ratio = min(screen_size[0]/cf.SCREEN_WIDTH,
                screen_size[1]/cf.SCREEN_HEIGHT)
    new_screen_size = (ceil(ratio * cf.SCREEN_WIDTH),
                       ceil(ratio * cf.SCREEN_HEIGHT))
    cf.WINDOWSURF = pygame.display.set_mode(new_screen_size,
                                            flags=pygame.RESIZABLE)


def initialize_clock():
    """
    Initialiser le temps
    """
    return pygame.time.Clock()


def get_events():
    """
    Obtenir les évènements
    """
    return pygame.event.get()


def group_sprite_define():
    """
    Création d'une nouvelle instance de groupage de sprites
    """
    return pygame.sprite.Group()


def add_to_group(sprite, group):
    """
    Ajoute un sprite à un groupe de sprites
    """
    pygame.sprite.Sprite.__init__(sprite, group)


def resize(surface, dimensions, destination=None):
    """
    Changer l'échelle de la surface en question
    """
    if destination is None:
        return pygame.transform.scale(surface, dimensions)
    return pygame.transform.scale(surface, dimensions, destination)


def resize_list(L, size):
    """
    Resize toutes les images d'une liste L à la taille size
    """
    for i in range(len(L)):
        L[i] = pygame.transform.scale(L[i], size)


def touch(sprite1, sprite2):
    """
    Renvoie True si les deux sprites se touchent
    """
    return pygame.sprite.collide_rect(sprite1, sprite2)

def collidegroup(sprite, group):
    """
    Renvoie true si y a une collision entre le sprite
    et n'importe quel sprite du groupe.
    """
    return pygame.sprite.spritecollideany(sprite, group)

def update_screen():
    """
    Mettre à jour l'écran
    """
    return pygame.display.flip()


def get_screen_size():
    """
    Avoir la taille de la fenêtre
    """
    return pygame.display.get_surface().get_size()


def create_rect(array):
    """
    Creer l'objet rectangle
    """
    return pygame.Rect(array)


def draw_rect(surface, color, objet):
    """
    Dessine l'objet rectangle sur une surface désignée
    """
    return pygame.draw.rect(surface, color, objet)


def mouse_pos():
    """
    Retourne la position de la souris
    """
    return pygame.mouse.get_pos()


def quit_game():
    """
    Quitte le jeu quand on ferme la fenêtre.
    """
    pygame.quit()
    sys.exit()


def font(font_name, size):
    """
    Renvoie une police à la bonne taille
    """
    return pygame.font.Font(font_name, size)


def collide(obj, pos_prev, pos_next, rect):
    """Gestion des collisions.
    obj : objet qui tombe (un joueur ou un item)
    pos_prev : Vector2, position précédente de l'objet
    pos_next : Vector2, position suivante de l'objet
    rect : Rect, ce qui est possiblement en collision avec l'objet
    Renvoie un triplet (collision verticale, collision horizontale,
    modification de position necessaire) (de type bool * bool * Vector2)"""
    # On ne tient pas compte du cas dans lequel l'objet traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes façons pas possible de jouer dans ce cas.
    if pos_next.x + obj.width > rect.left\
            and pos_next.x < rect.right:
        # Dans la plateforme horizontalement

        if pos_prev.y + obj.height <= rect.top:
            # Position initale au-dessus de la plateforme
            if pos_next.y + obj.height > rect.top:
                # Nouvelle position dans ou sous la plateforme
                cf.FLAG_JUMP = True
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


class GameObject(Sprite):
    # pylint: disable=too-few-public-methods
    """Utilisée pour tous les objets du monde, comme le sol, les plateformes,
        les nuages, les bâtiments, etc. qui se déplacent de droite à gauche"""
    def __init__(self, position, scroll, image):
        """position : int * int, position de l'objet
        scroll : float/int, vitesse de déplacement
        img : sprite"""
        super().__init__()
        self.pos = Vec(position)
        self.scroll = scroll
        # 0 si c'est loin et que ça bouge pas,
        # 1 si c'est près et que ça bouge à la vitesse du sol
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        # Limite à partir de laquelle on génère un nouvel objet sur sa droite
        # FLAG_creation est un flag pour ne générer qu'un seul nouvel objet
        self.FLAG_creation = True

    def update(self):
        """Modifie le vecteur position"""
        posnext = self.pos + self.scroll * Vec(-cf.SPEED, 0)
        self.pos = posnext
        self.rect.topleft = self.pos
        if self.rect.right < 0:     # si l'objet sort de l'écran
            #print(self)
            self.kill()              # on le supprime
        # On met à jour l'image
        cf.DISPLAYSURF.blit(self.image, self.rect)
