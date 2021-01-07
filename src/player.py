"""Module de gestion des joueurs."""

import random as rd

import src.conf as cf
import src.sprites as spt
import src.utilities as ut

JUMP_KEYS = [ut.K_SPACE, ut.K_RETURN, ut.K_s, ut.K_u]
"""Touches de saut des joueurs."""
WINNER = 0
"""Joueur gagnant."""
COLORS = ["green", "purple", "red", "white"]
COLORSTRAD = {
    "fr" : ["vert", "violet", "rouge", "blanc"],
    "en" : ["green", "purple", "red", "white"]
}


class Player(ut.Sprite):
    """
    Gestion du joueur.

    Attributes
    ----------
    images : Surface list
        Liste des images de l'objet
    img : int
        Indice dans la liste d'images
    rect : Rect
        Rectangle de collision du joueur
    pos : Vector2
        Position du joueur
    vel : Vector2
        Vitesse du joueur
    acc : Vector2
        Accélération du joueur
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, color="green"):
        """
        Initialisation du joueur.

        Parameters
        ----------
        color : str
            La couleur du joueur parmis Player.COLORS
        """
        # Initialisation de la classe parent
        # ut.add_to_group(self, cf.player_sprite)
        super().__init__()
        # Liste d'images de l'objet, et indice de cette liste
        # [:] pour une copie parfaite, à cause du multijoueur pour l'instant
        self.images = spt.img_dict["mono" + color + "_img"][:]
        self.img = 0
        # Création de l'objet
        self.rect = self.images[0].get_rect()

        # dimensions
        self.width, self.height = cf.SIZE['normal']

        # Est vivant
        self.alive = True

        # Position
        # X : milieu de l'écran
        # moins la largeur sur 2 pour être centré (car topleft)
        x = cf.SCREEN_WIDTH // 2 - self.width // 2
        y = spt.GROUND_HEIGHT - self.height
        self.pos = ut.Vec(x, y)
        self.rect.midbottom = self.pos

        # Vitesse
        self.vel = ut.Vec(0, 0)
        # Accélération
        self.acc = ut.Vec(0, cf.G)

        # Drapeau de disponibilité du saut
        self.FLAG_JUMP = True
        # Drapeau de disponibilité du second saut
        self.FLAG_JUMP_2 = False

        # état dans lequel est le joueur, est modifié par la prise d'item.
        # normal, fast, slow, little, big
        self.state = "normal"

        # Lorsqu'on prend un item, ça a une durée limitée
        # D'où ce timer (en frames)
        self.timer = 0

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
        # Gestion de l'état dans lequel on est (selon l'item mangé)
        if self.state != "normal":
            self.timer -= 1
            # si le timer est fini on redevient normal
            if self.timer == 0:
                self.end_item()

            if self.state == "fast":
                self.vel.x = cf.V_ITEM['fast']
                # si on arrive aux 2/3 de l'écran ça arrête d'avancer
                if self.pos.x > (cf.SCREEN_WIDTH * 2) // 3:
                    self.end_item()

            elif self.state == "slow":
                self.vel.x = cf.V_ITEM['slow']
                # si on sort presque de l'écran ça arrête de ralentir
                if self.pos.x < self.width:
                    self.end_item()

        ut.update_pos_vel(self, spt.ground)

        for item in spt.items:  # Gestion de la prise d'item
            if ut.contact(self, item):
                self.change_state(item)

        # On change le sprite du joueur
        self.img += 0.03 * cf.SPEED
        # Faire par fraction permet d'accélérer plus lentement les pédales
        if int(self.img) >= len(self.images):
            self.img = 0

        cf.DISPLAYSURF.blit(self.images[int(self.img)], self.rect)
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
               or self.pos.y + self.height < 0
               or self.pos.x + self.width < 0
               or self.pos.x > cf.SCREEN_WIDTH)

    def change_state(self, item):
        """
        Modifie l'état après la prise d'un objet et supprime ce dernier.

        Parameters
        ----------
        item : Item
            L'objet récupéré
        """
        self.state = item.type
        item.kill()
        self.timer = cf.ITEM_TIME[item.type]

        # resize le player
        if self.state in ['little', 'big']:
            self.resize('normal', self.state)

    def end_item(self):
        """Retour à l'état normal."""
        # On se remet à la bonne taille, position, etc.
        if self.state in ['little', 'big']:
            self.resize(self.state, 'normal')

        # On se remet dans l'état normal et on annule le FLAG_ITEM
        self.state = "normal"
        self.vel.x = 0

        cf.FLAG_ITEM = False
        cf.NEW_ITEM_TIME = cf.SECONDS + rd.randint(cf.ITEM_PROBA_MIN,
                                                   cf.ITEM_PROBA_MAX)

    def resize(self, size1, size2):
        """Fais passer le joueur de la size1 à la size2"""
        ut.resize_list(self.images, cf.SIZE[size2])
        self.width, self.height = cf.SIZE[size2]
        for i in range(2):
            self.pos[i] = self.pos[i] + cf.SIZE[size1][i]\
                - cf.SIZE[size2][i]
        self.rect = self.images[0].get_rect()
        self.rect.midbottom = self.pos
