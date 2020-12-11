"""Gère l'abstraction de pygame par la (re)définition de fonctions"""

import pygame
import src.conf as cf

Vec = pygame.math.Vector2

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


def initialize_window(icon, title, width, height):
    """
    Initialiser les variables d'environnement graphique
    et initialisation des paramètres
    de fenêtre
    """
    pygame.display.set_icon(
        load_image(icon))
    pygame.display.set_caption(title)
    return (pygame.Surface((width, height)),
            pygame.display.set_mode((width, height),
                                            flags=pygame.RESIZABLE))


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

def add_to_group(sprite,group):
    """
    Ajoute un sprite à un groupe de sprites
    """
    pygame.sprite.Sprite.__init__(sprite, group)


def resize(surface, dimensions, destination=None):
    """
    Changer l'échelle de la surface en question
    """
    return pygame.transform.scale(surface, dimensions, destination)


class GameObject(pygame.sprite.Sprite):
    # pylint: disable=too-few-public-methods
    """Utilisée pour tous les objets du monde, comme le sol, les plateformes,
        les nuages, les bâtiments, etc. qui se déplacent de droite à gauche"""
    def __init__(self, position, scroll, image):
        """position : int * int, position de l'objet
        scroll : float/int, vitesse de déplacement
        img : sprite"""
        super().__init__()
        self.pos = cf.Vec(position)
        self.scroll = scroll
        # 0 si c'est loin et que ça bouge pas,
        # 1 si c'est près et que ça bouge à la vitesse du sol
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        # Limite à partir de laquelle on génère un nouvel objet sur sa droite
        # pasencorecree est un flag pour ne générer qu'un seul nouvel objet
        self.pasencorecree = True

    def update(self):
        """Modifie le vecteur position"""
        posnext = self.pos + self.scroll * cf.Vec(-cf.SPEED, 0)
        self.pos = posnext
        self.rect.topleft = self.pos
        if self.rect.right < 0:     # si l'objet sort de l'écran
            self.kill()              # on le supprime
        # On met à jour l'image
        cf.DISPLAYSURF.blit(self.image, self.rect)
