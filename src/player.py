"""Contient la classe Player, permettant de gérer le personnage."""

import pygame
import src.conf as cf
# Pour créer des vecteurs de dimension 2
vec = pygame.math.Vector2

# Dimensions
WIDTH = 20
HEIGHT = 30
# Position initiale
X_INIT = 100
Y_INIT = 100
# Vitesse initiale
V_0 = 0
# Vitesse initiale lors d'un saut
V_JMP = 100
# Accélération initiale
A_0 = 0
# Accélération due à la gravité
G = 1


def collide(pos1, pos2, rect):
    """Vérifie la collision avec l'objet rect, étant donné la position
    à l'instant précédent, et la position prévue pour l'instant suivant.
    Renvoie une position corrigée s'il y a collision.
    Suppose un mouvement vertical du joueur."""
    # On ne tient pas compte du cas dans lequel le joueur traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes façons pas possible de jouer dans ce cas.
    if pos2.x + WIDTH <= rect.left or pos2.x >= rect.right:
        return (False, None)
    if pos1.y + HEIGHT <= rect.top:
        if pos2.y + HEIGHT <= rect.top:
            return (False, None)
        return (True, vec(pos2.x, rect.top - HEIGHT))
    if pos1.y <= rect.bottom:
        if pos2.y <= rect.bottom:
            return (False, None)
        return (True, vec(pos2.x, rect.bottom))
    return None


class Player(pygame.sprite.Sprite):
    """Gestion du personnage, par les méthodes jump(self) et move(self)."""
    def __init__(self):
        # Initialisation de la classe parent
        # pygame.sprite.Sprite.__init__(self, cf.player_sprite)
        super().__init__()
        # Dimensions et couleur de l'objet
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill([255, 140, 25])
        # Création de l'objet
        self.shape = self.image.get_rect()

        # Position
        self.pos = vec(X_INIT, Y_INIT)
        self.shape.midbottom = self.pos

        # Vitesse
        self.vel = vec(V_0, 0)
        # Accélération
        self.acc = vec(A_0, G)

    def jump(self):
        """Lance le saut du personnage."""
        self.vel.y -= V_JMP

    def move(self):
        """Modifie les vecteurs position,
        vitesse et accélération si nécessaire."""
        self.vel += self.acc
        posnext = self.pos + self.vel + 0.5 * self.acc
        flag = False
        # On suppose qu'il ne peut y avoir qu'une seule collision à la fois
        for plat in cf.sol:
            coll = collide(self.pos, posnext, plat.rect)
            if coll[0]:
                self.pos = coll[1]
                self.vel.y = 0
                flag = True
        if not flag:
            self.pos = posnext
        self.shape.topleft = self.pos
