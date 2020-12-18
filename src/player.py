"""Contient la classe Player, permettant de gerer le personnage."""

import src.conf as cf
import src.sprites as spt
import src.utilities as ut

# Position initiale
X_INIT = cf.SCREEN_WIDTH//2
Y_INIT = spt.GROUND_HEIGHT - spt.p_HEIGHT
# Vitesse initiale
V_0 = 0
# Vitesse initiale lors d'un saut
V_JMP = 15
# Accélération initiale
A_0 = 0
# Accélération due à la gravité
G = 0.8


def collide(pos_prev, pos_next, rect):
    """Gestion des collisions.
    pos_prev : Vector2, position précédente du joueur
    pos_next : Vector2, position suivante du joueur
    rect : Rect, l'objet possiblement en collision avec le joueur
    Renvoie un triplet (collision verticale, collision horizontale,
    modification de position necessaire) (de type bool * bool * Vector2)"""
    # On ne tient pas compte du cas dans lequel le joueur traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes façons pas possible de jouer dans ce cas.
    if pos_next.x + spt.p_WIDTH > rect.left\
            and pos_next.x < rect.right:
        # Dans la plateforme horizontalement

        if pos_prev.y + spt.p_HEIGHT <= rect.top:
            # Position initale au-dessus de la plateforme
            if pos_next.y + spt.p_HEIGHT > rect.top:
                # Nouvelle position dans ou sous la plateforme
                cf.FLAG_JUMP = True
                return (True, False,
                        ut.Vec(pos_next.x, rect.top - spt.p_HEIGHT))

        elif pos_prev.y >= rect.bottom:
            # Position initiale en-dessous de la plateforme
            if pos_next.y < rect.bottom:
                # Nouvelle position dans ou au-dessus de la plateforme
                return (True, False, ut.Vec(pos_next.x, rect.bottom))

        elif pos_next.y + spt.p_HEIGHT > rect.top\
                and pos_next.y < rect.bottom:
            # On ne considère que les collisions à gauche des plateformes
            return (False, True, ut.Vec(rect.left - spt.p_WIDTH, pos_next.y))

    return(False, False, None)


class Player(ut.Sprite):
    """Gestion du personnage, par les méthodes jump(self), move(self)
    et death(self)."""

    def __init__(self):
        # Initialisation de la classe parent
        # ut.add_to_group(self, cf.player_sprite)
        super().__init__()
        # Liste d'images de l'objet, et indice de cette liste
        self.images = spt.d["mono_img"]
        self.img = 0
        # Création de l'objet
        self.shape = self.images[0].get_rect()

        # Position
        self.pos = ut.Vec(X_INIT, Y_INIT)
        self.shape.midbottom = self.pos

        # Vitesse
        self.vel = ut.Vec(V_0, 0)
        # Accélération
        self.acc = ut.Vec(A_0, G)

        # état dans lequel est le joueur, est modifié par la prise d'item.
        # normal, fast, slow, little, big
        self.state = "normal"

        # Lorsqu'on prend un item, ça a une durée limitée
        # D'où ce timer (en frames)
        self.timer = 0

    def jump(self):
        """Lance le saut du personnage."""
        if cf.FLAG_JUMP:
            cf.FLAG_JUMP = False
            self.vel.y = -V_JMP
            cf.FLAG_JUMP_2 = True
        elif cf.FLAG_JUMP_2:
            self.vel.y = -V_JMP
            cf.FLAG_JUMP_2 = False

    def move(self):
        """Modifie les vecteurs position, vitesse
        et accélération si nécessaire."""

        # Gestion de l'état dans lequel on est
        if self.state != "normal":
            self.timer -= 1
            # si le timer est fini on redevient normal
            if self.timer == 0:
                self.end_item()

            if self.state == "fast":
                self.vel.x = 4
                # si on arrive aux 2/3 de l'écran ça arrête d'avancer
                if self.pos.x > (cf.SCREEN_WIDTH*2)//3:
                    self.end_item()

            elif self.state == "slow":
                self.vel.x = -4
                # si on sort presque de l'écran ça arrête de ralentir
                if self.pos.x < spt.p_WIDTH:
                    self.end_item()

        self.vel += self.acc
        posnext = self.pos + self.vel + 0.5 * self.acc

        for plat in spt.ground:  # Gestion des collisions
            coll = collide(self.pos, posnext, plat.rect)
            if coll[0] or coll[1]:
                posnext = coll[2]
                if coll[0]:
                    self.vel.y = 0
                if coll[1]:
                    self.vel.x = 0

        for item in spt.items: # Gestion de la prise d'item
            coll = collide(self.pos, posnext, item.rect)
            if coll[0] or coll[1]:
                self.change_state(item)

        self.pos = posnext
        self.shape.topleft = self.pos  # Mise à jour de la position

        # On change le sprite du joueur
        self.img += 0.03 * cf.SPEED
        # Faire par fraction permet d'accélérer plus lentement les pédales
        if int(self.img) >= len(self.images):
            self.img = 0
        cf.DISPLAYSURF.blit(self.images[int(self.img)], self.shape)

    def death(self):
        """Renvoie si le joueur sort (suffisamment) de l'écran ou non"""
        return(self.pos.y > cf.SCREEN_HEIGHT + 50
               or self.pos.x + spt.p_WIDTH < 0)

    def change_state(self, item):
        """Modifie l'état du joueur parce qu'il a pris un item"""
        self.state = item.type
        item.kill()
        self.timer = cf.ITEM_TIME[item.type]

        # il faut resize la taille de l'image mais aussi le rect...
        if self.state == "little":
            pass
        if self.state == "big":
            pass

    def end_item(self):
        """Quand on redevient normal"""
        self.state = "normal"
        cf.FLAG_ITEM = False
        self.vel.x = 0
