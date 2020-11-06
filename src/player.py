"""Contient la classe Player, permettant de gérer le personnage."""

import pygame
import src.conf as cf
# Pour créer des vecteurs de dimension 2
vec = pygame.math.Vector2

# Dimensions
WIDTH = 20
HEIGHT = 30
# Position initiale
X_INIT = cf.SCREEN_WIDTH/2
Y_INIT = cf.SOL_HAUT - HEIGHT
# Vitesse initiale
V_0 = 0
# Vitesse initiale lors d'un saut
V_JMP = 15
# Accélération initiale
A_0 = 0
# Accélération due à la gravité
G = 1
# Drapeau de disponibilité du saut
FLAG_JUMP = False
# Drapeau de disponibilité du second saut
FLAG_JUMP_2 = False


def collide(pos_prev, pos_next, rect_next):
    """Vérifie la collision avec l'objet rect, étant donné la position
    à l'instant précédent, et la position prévue pour l'instant suivant.
    Renvoie une position corrigée s'il y a collision.
    Suppose un mouvement vertical du joueur.
    Renvoie un triplet (collision verticale, collision horizontale,
    modification de position nécessaire)"""
    global FLAG_JUMP
    # On ne tient pas compte du cas dans lequel le joueur traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes façons pas possible de jouer dans ce cas.
    if pos_next.x + WIDTH <= rect_next.left or pos_next.x >= rect_next.right:
        return (False, False, None)
    if pos_prev.y + HEIGHT <= rect_next.top:
        if pos_next.y + HEIGHT <= rect_next.top:
            return (False, False, None)
        FLAG_JUMP = True
        return (True, False, vec(pos_next.x, rect_next.top - HEIGHT))
    if pos_prev.y >= rect_next.bottom:
        if pos_next.y <= rect_next.bottom:
            return (False, False, None)
        return (True, False, vec(pos_next.x, rect_next.bottom))
    # pos_prev.y + HEIGHT > rect_next.top and pos_prev.y < rect_next.bottom
    if pos_next.y + HEIGHT <= rect_next.top or pos_next.y >= rect_next.bottom:
        (False, False, None)
    # On ne considère que les collisions à gauche des plateformes
    (False, True, vec(rect_next.left, pos_next.y))
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
        global FLAG_JUMP
        global FLAG_JUMP_2
        if FLAG_JUMP :
            FLAG_JUMP = False
            cf.JMP_COOLDOWN = 15
            self.vel.y = -V_JMP
            FLAG_JUMP_2 = True
        elif FLAG_JUMP_2 and cf.JMP_COOLDOWN == 0:
            self.vel.y = -V_JMP
            FLAG_JUMP_2 = False

    def move(self):
        """Modifie les vecteurs position,
        vitesse et accélération si nécessaire."""
        self.vel += self.acc
        posnext = self.pos + self.vel + 0.5 * self.acc
        flag = False
        # On suppose qu'il ne peut y avoir qu'une seule collision à la fois
        for plat in cf.sol:
            coll = collide(self.pos, posnext, plat.rect)
            if coll[0] or coll[1]:
                self.pos = coll[2]
                if coll[0]:
                    self.vel.y = 0
                    flag = True
                if coll[1]:
                    self.vel.x = 0
                    flag = True
        if not flag:
            self.pos = posnext
        self.shape.topleft = self.pos
        cf.DISPLAYSURF.blit(self.image, self.shape)
