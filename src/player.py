#Contient la classe Player, permettant de g�rer le personnage.

import pygame, sys
import src.conf as cf
# Pour cr�er des vecteurs de dimension 2
vec = pygame.math.Vector2


# Dimensions
WIDTH = 63
HEIGHT = 96
# Position initiale
X_INIT = cf.SCREEN_WIDTH//2
Y_INIT = cf.SOL_HAUT - HEIGHT
# Vitesse initiale
V_0 = 0
# Vitesse initiale lors d'un saut
V_JMP = 15
# Acc�l�ration initiale
A_0 = 0
# Acc�l�ration due � la gravit�
G = 0.4
# Drapeau de disponibilit� du saut
FLAG_JUMP = False
# Drapeau de disponibilit� du second saut
FLAG_JUMP_2 = False


def collide(pos_prev, pos_next, rect_next):
    # """V�rifie la collision avec l'objet rect, �tant donn� la position
    # � l'instant pr�c�dent, et la position pr�vue pour l'instant suivant.
    # Renvoie une position corrig�e s'il y a collision.
    # Suppose un mouvement vertical du joueur.
    # Renvoie un triplet (collision verticale, collision horizontale,
    # modification de position n�cessaire)"""
    global FLAG_JUMP
    # On ne tient pas compte du cas dans lequel le joueur traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes fa�ons pas possible de jouer dans ce cas.
    if pos_next.x + WIDTH <= rect_next.left or pos_next.x >= rect_next.right:
        return (False, False, None)
    if pos_prev.y + HEIGHT <= rect_next.top:
        if pos_next.y + HEIGHT <= rect_next.top:
            return (False, False, None)
        FLAG_JUMP = True
        return (True, False, vec(pos_next.x, rect_next.top - HEIGHT))
    if pos_prev.y >= rect_next.bottom:
        if pos_next.y >= rect_next.bottom:
            return (False, False, None)
        return (True, False, vec(pos_next.x, rect_next.bottom))
    # pos_prev.y + HEIGHT > rect_next.top and pos_prev.y < rect_next.bottom
    if pos_next.y + HEIGHT <= rect_next.top or pos_next.y >= rect_next.bottom:
        return (False, False, None)
    # On ne consid�re que les collisions � gauche des plateformes
    return (False, True, vec(rect_next.left - WIDTH, pos_next.y))



class Player(pygame.sprite.Sprite):
    #Gestion du personnage, par les m�thodes jump(self) et move(self).
    def __init__(self):
        # Initialisation de la classe parent
        # pygame.sprite.Sprite.__init__(self, cf.player_sprite)
        super().__init__()
        # Liste d'images de l'objet, et indice de cette liste
        self.images = []
        for i in range(8) :
            self.images.append(pygame.image.load("assets/img/mono/Mono"+str(i)+".png"))
        self.img = 0
        # Cr�ation de l'objet
        self.shape = self.images[0].get_rect()

        # Position
        self.pos = vec(X_INIT, Y_INIT)
        self.shape.midbottom = self.pos

        # Vitesse
        self.vel = vec(V_0, 0)
        # Acc�l�ration
        self.acc = vec(A_0, G)

    def jump(self):
        #Lance le saut du personnage.
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
        #Modifie les vecteurs position, vitesse et acc�l�ration si n�cessaire.
        self.vel += self.acc
        posnext = self.pos + self.vel + 0.5 * self.acc
        flag = False
        # On suppose qu'il ne peut y avoir qu'une seule collision � la fois
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
        # On v�rifie la mort
        if self.pos.y > cf.SCREEN_HEIGHT or self.pos.x + WIDTH < 0:
            pygame.quit()
            sys.exit()
        #On change l'image
        self.img+=0.03*cf.SPEED
        #faire par fraction permet d'update plus lentement que le FPS classique
        #le *cf.SPEED permet d'acc�l�rer les p�dales
        if int(self.img)>=len(self.images) :
            self.img = 0
        cf.DISPLAYSURF.blit(self.images[int(self.img)], self.shape)
