"""Module de gestion des joueurs."""

import src.conf as cf
import src.sprites as spt
import src.utilities as ut

# Position initiale
X_INIT = cf.SCREEN_WIDTH // 2
"""Abscisse initiale"""
Y_INIT = spt.GROUND_HEIGHT - spt.p_HEIGHT
"""Ordonnée initiale"""

V_0 = 0
"""Vitesse initiale"""
V_JMP = 15
"""Vitesse initiale lors d'un saut"""
A_0 = 0
"""Accélération initiale"""
G = 0.8
"""Accélération due à la gravité"""
JUMP_KEYS = [ut.K_SPACE, ut.K_RETURN, ut.K_s]
"""Touches de saut des joueurs"""
WINNER = 1
"""Joueur gagnant"""


def collide(player, pos_next, rect):
    """
    Gestion des collisions.

    Parameters
    ----------
    player : Player
        joueur dont on examine la collision
    pos_next : Vector2
        position suivante du joueur
    rect : Rect
        l'objet potentiellement en collision avec le joueur

    Returns
    -------
    bool * bool * Vector2
        un triplet (collision verticale, collision horizontale,
        modification de position necessaire)
    """
    # On ne tient pas compte du cas dans lequel le joueur traverserait
    # une plateforme dans sa longueur entre deux positions, il ne serait
    # de toutes façons pas possible de jouer dans ce cas.
    pos_prev = player.pos
    if pos_next.x + spt.p_WIDTH > rect.left\
            and pos_next.x < rect.right:
        # Dans la plateforme horizontalement

        if pos_prev.y + spt.p_HEIGHT <= rect.top:
            # Position initale au-dessus de la plateforme
            if pos_next.y + spt.p_HEIGHT > rect.top:
                # Nouvelle position dans ou sous la plateforme
                player.FLAG_JUMP = True
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
    """
    Gestion du joueur.

    Attributes
    ----------
    images : Surface list
        Liste des images de l'objet
    img : int
        Indice dans la liste d'images
    shape : Rect
        Rectangle de collision du joueur
    pos : Vector2
        Position du joueur
    vel : Vector2
        Vitesse du joueur
    acc : Vector2
        Accélération du joueur
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """Initialisation du joueur."""
        # Initialisation de la classe parent
        # ut.add_to_group(self, cf.player_sprite)
        super().__init__()
        # Liste d'images de l'objet, et indice de cette liste
        self.images = spt.img_dict["mono_img"]
        self.img = 0
        # Création de l'objet
        self.shape = self.images[0].get_rect()

        # Est vivant
        self.alive = True

        # Position
        self.pos = ut.Vec(X_INIT, Y_INIT)
        self.shape.midbottom = self.pos

        # Vitesse
        self.vel = ut.Vec(V_0, 0)
        # Accélération
        self.acc = ut.Vec(A_0, cf.G)

        # Drapeau de disponibilité du saut
        self.FLAG_JUMP = True
        # Drapeau de disponibilité du second saut
        self.FLAG_JUMP_2 = False

    def jump(self):
        """Lance le saut du personnage."""
        if self.FLAG_JUMP:
            self.FLAG_JUMP = False
            self.vel.y = -cf.V_JMP
            self.FLAG_JUMP_2 = True
        elif self.FLAG_JUMP_2:
            self.vel.y = -cf.V_JMP
            self.FLAG_JUMP_2 = False

    def move(self):
        """Met à jour pos, vec et acc."""
        self.vel += self.acc
        posnext = self.pos + self.vel + 0.5 * self.acc

        for plat in spt.ground:  # Gestion des collisions
            coll = collide(self, posnext, plat.rect)
            if coll[0] or coll[1]:
                posnext = coll[2]
                if coll[0]:
                    self.vel.y = 0
                if coll[1]:
                    self.vel.x = 0
        self.pos = posnext
        self.shape.topleft = self.pos  # Mise à jour de la position

        # On change le sprite du joueur
        self.img += 0.03 * cf.SPEED
        # Faire par fraction permet d'accélérer plus lentement les pédales
        if int(self.img) >= len(self.images):
            self.img = 0
        cf.DISPLAYSURF.blit(self.images[int(self.img)], self.shape)
        if self.in_death_position():
            self.alive = False

    def in_death_position(self):
        """
        Condition de défaite du joueur.

        Returns
        -------
        bool
            True si le joueur sort suffisamment de l'écran.
        """
        return(self.pos.y > cf.SCREEN_HEIGHT + 50
               or self.pos.y + spt.p_HEIGHT < 0
               or self.pos.x + spt.p_WIDTH < 0
               or self.pos.x > cf.SCREEN_WIDTH)
