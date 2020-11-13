"""Contient la classe Player, permettant de gerer le personnage."""

import pygame, sys
import src.conf as cf
# Pour créer des vecteurs de dimension 2
vec = pygame.math.Vector2

# Position initiale
X_INIT = cf.SCREEN_WIDTH//2
Y_INIT = cf.SOL_HAUT - cf.p_HEIGHT
# Vitesse initiale
V_0 = 0
# Vitesse initiale lors d'un saut
V_JMP = 15
# Accélération initiale
A_0 = 0
# Accélération due �  la gravité
G = 0.4
# Drapeau de disponibilité du saut
FLAG_JUMP = False
# Drapeau de disponibilité du second saut
FLAG_JUMP_2 = False


def collide(pos_prev, pos_next, rect_next):
    """Verifie la collision avec l'objet rect, etant donne la position
    A l'instant precedent, et la position prevue pour l'instant suivant.
    Renvoie une position corrigee s'il y a collision.
    Suppose un mouvement vertical du joueur.
    Renvoie un triplet (collision verticale, collision horizontale,
    modification de position necessaire)"""
    global FLAG_JUMP
    # On ne tient pas compte du cas dans lequel le joueur traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes fa�ons pas possible de jouer dans ce cas.
    if pos_next.x + cf.p_WIDTH <= rect_next.left or pos_next.x >= rect_next.right:
        return (False, False, None)
    if pos_prev.y + cf.p_HEIGHT <= rect_next.top:
        if pos_next.y + cf.p_HEIGHT <= rect_next.top:
            return (False, False, None)
        FLAG_JUMP = True
        return (True, False, vec(pos_next.x, rect_next.top - cf.p_HEIGHT))
    if pos_prev.y >= rect_next.bottom:
        if pos_next.y >= rect_next.bottom:
            return (False, False, None)
        return (True, False, vec(pos_next.x, rect_next.bottom))
    if pos_next.y + cf.p_HEIGHT <= rect_next.top or pos_next.y >= rect_next.bottom:
        return (False, False, None)
    # On ne consid�re que les collisions � gauche des plateformes
    return (False, True, vec(rect_next.left - cf.p_WIDTH, pos_next.y))



class Player(pygame.sprite.Sprite):
    """Gestion du personnage, par les méthodes jump(self) et move(self)."""
    def __init__(self):
        # Initialisation de la classe parent
        # pygame.sprite.Sprite.__init__(self, cf.player_sprite)
        super().__init__()
        # Liste d'images de l'objet, et indice de cette liste
        self.images = cf.mono_img
        self.img = 0
        # Création de l'objet
        self.shape = self.images[0].get_rect()

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
            self.vel.y = -V_JMP
            FLAG_JUMP_2 = True
        elif FLAG_JUMP_2:
            self.vel.y = -V_JMP
            FLAG_JUMP_2 = False

    def move(self):
        """Modifie les vecteurs position, vitesse et accélération si nécessaire."""
        self.vel += self.acc
        posnext = self.pos + self.vel + 0.5 * self.acc
        flag = False
        # On suppose qu'il ne peut y avoir qu'une seule collision �  la fois
        for plat in cf.sol:
            coll = collide(self.pos, posnext, plat.rect)
            if coll[0] or coll[1]:
                posnext = coll[2]
                if coll[0]:
                    self.vel.y = 0
                if coll[1]:
                    self.vel.x = 0
        self.pos = posnext
        self.shape.topleft = self.pos
        #On change l'image
        self.img+=0.03*cf.SPEED
        #faire par fraction permet d'update plus lentement que le FPS classique
        #le *cf.SPEED permet d'accélérer les pédales
        if int(self.img)>=len(self.images) :
            self.img = 0
        cf.DISPLAYSURF.blit(self.images[int(self.img)], self.shape)

    def death(self):
        """Renvoie si le joueur sort (suffisamment) de l'écran ou non"""
        return(self.pos.y > cf.SCREEN_HEIGHT + 50 or self.pos.x + cf.p_WIDTH < 0)
