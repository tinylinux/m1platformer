"""Gestion des menus."""

import src.conf as cf
import src.utilities as ut

FONT_PIXEL = "assets/font/punk_rockf.ttf"
"""Chemin vers la police"""

CHARS_LOW = "azertyuiopqsdfghjklmwxcvbn1234567890"
"""Caractères acceptés, en minuscules"""
CHARS_CAP = "AZERTYUIOPQSDFGHJKLMWXCVBN1234567890"
"""Caractères acceptés, en majuscules"""


def mouse_on_button(mouse, button_pos, button_size):
    """
    Indique si le pointeur de la souris est sur le bouton.

    Parameters
    ----------
    mouse : int * int
        Position du pointeur de la souris
    button_pos : int * int
        Position du bouton
    button_size : int * int
        Largeur et hauteur du bouton

    Returns
    -------
    bool
        True si le pointeur est sur le bouton
    """
    # Récupération de la dimension de la fenêtre
    window_dimensions = ut.get_screen_size()

    # Calcul du facteur d'échelle
    scale_factor_x = cf.SCREEN_WIDTH/window_dimensions[0]
    scale_factor_y = cf.SCREEN_HEIGHT/window_dimensions[1]

    # Position de la sourie ajustée
    new_mouse = mouse[0] * scale_factor_x, mouse[1] * scale_factor_y

    return(button_pos[0] <= new_mouse[0] <= button_pos[0] + button_size[0]
           and button_pos[1] <= new_mouse[1] <= button_pos[1] + button_size[1])


class Button:
    """Boutons pour les menus."""

    def __init__(self, position, size):
        """
        Initialisation.

        Parameters
        ----------
        position : int * int
            Position du bouton
        size : int * int
            Largeur et hauteur du bouton
        """
        self.position = position
        self.size = size
        self.rect = ut.create_rect([position[0], position[1],
                                    size[0], size[1]])

    def click(self, mouse):
        """
        Indique si le pointeur de la souris est sur le bouton.

        Parameters
        ----------
        mouse : int * int
            Position de la souris

        Returns
        -------
        bool
            True si le pointeur est sur le bouton
        """
        return mouse_on_button(mouse, self.position, self.size)


class ButtonText(Button):
    """Boutons aillant du texte comme étiquette."""

    def __init__(self, position, size, text):
        """
        Initialisation.

        Parameters
        ----------
        position : int * int
            Position du bouton
        size : int * int
            Largeur et hauteur du bouton
        text : string
            Étiquette du bouton
        """
        super().__init__(position, size)
        self.text = text
        self.text_position = (position[0] + 10, position[1] + 10)

    def print(self, mouse):
        """
        Affiche le bouton.

        Parameters
        ----------
        mouse : int * int
            Position de la souris
        """
        if mouse_on_button(mouse, self.position, self.size):
            ut.draw_rect(cf.DISPLAYSURF, cf.HOVER, self.rect)
        else:
            ut.draw_rect(cf.DISPLAYSURF, cf.IDLE, self.rect)
        cf.DISPLAYSURF.blit(self.text, self.text_position)


class ButtonImage(Button):
    """
    Boutons affichant une image.

    Attributes
    ----------
    image : str
        Nom de l'image à afficher quand le bouton est inactif
    image_hover : str
        Nom de l'image à afficher quand le pointeur est sur le bouton
    """

    def __init__(self, position, size, image, image_hover):
        """
        Initialisation.

        Parameters
        ----------
        position : int * int
            Position du bouton
        size : int * int
            Largeur et hauteur du bouton
        image : str
            Nom de l'image à afficher quand le bouton est inactif
        image_hover : str
            Nom de l'image à afficher quand le pointeur est sur le bouton
        """
        super().__init__(position, size)
        self.image = image
        self.image_hover = image_hover

    def print(self, mouse):
        """
        Affiche le bouton.

        Parameters
        ----------
        mouse : int * int
            Position du pointeur de la souris
        """
        if mouse_on_button(mouse, self.position, self.size):
            cf.DISPLAYSURF.blit(ut.load_image(self.image_hover),
                                self.position)
        else:
            cf.DISPLAYSURF.blit(ut.load_image(self.image), self.position)


class InputZone(Button):
    """
    Zones permettant le saisie de texte.

    Attributes
    ----------
    input : str
        Texte inséré dans la zone
    selescted : bool
        Indique si la zone est sélectionnée
    text_position : int * int
        Position du texte par rapport à la zone
    font : Font
        La fonte
    """

    def __init__(self, position, size, font=None):
        """
        Initialisation.

        Parameters
        ----------
        position : int * int
            Position du bouton
        size : int * int
            Largeur et hauteur du bouton
        font : Font, optionnel
            La fonte
        """
        super().__init__(position, size)
        if font is None:
            font = ut.font(None, cf.INPUT_FONT_SIZE)
        self.input = ""
        self.selected = False
        self.text_position = (position[0] + 10, position[1] + 10)
        self.font = font

    def print(self):
        """Affiche la zone et le texte entré."""
        ut.draw_rect(cf.DISPLAYSURF, cf.IDLE, self.rect)
        cf.DISPLAYSURF.blit(self.font.render(self.input, True, cf.WHITE),
                            self.text_position)

    def select(self):
        """Active la sélection de la zone."""
        self.selected = True

    def deselect(self):
        """Désactive la sélection de la zone."""
        self.selected = False

    def read(self, key):
        """
        Lit les caractères entrés.

        Parameters
        ----------
        key : key
            La touche détectée
        """
        if self.selected:
            key_name = ut.keyname(key)
            if key_name in CHARS_LOW:
                self.input += CHARS_CAP[CHARS_LOW.index(key_name)]
            elif key == ut.K_SPACE:
                self.input += " "
            elif key == ut.K_BACKSPACE and self.input != "":
                self.input = self.input[:-1]


start_button = ButtonImage((440, 314), (401, 123), "assets/img/ui/begin.png",
                           "assets/img/ui/beginpushed.png")
"""Bouton pour lancer le jeu"""

records_button = ButtonImage((440, 463), (401, 123),
                             "assets/img/ui/records.png",
                             "assets/img/ui/recordspushed.png")
"""Boutons pour afficher les records"""

restart_button = ButtonImage((440, 500), (401, 123),
                             "assets/img/ui/playagain.png",
                             "assets/img/ui/playagainpushed.png")
"""Bouton pour relancer le jeu"""

return_button = ButtonImage((20, 20), (123, 123),
                            "assets/img/ui/return.png",
                            "assets/img/ui/returnpushed.png")
"""Bouton pour revenir au menu principal"""


def print_image(image, position):
    """
    Affiche une image à une position donnée.

    Parameters
    ----------
    image : string
        Le chemin vers l'image dans les fichiers
    position : int * int
        Les coordonnées de l'image
    """
    cf.DISPLAYSURF.blit(ut.load_image(image), position)


def print_text(text, position_center, color=cf.WHITE,
               font=None, bold=False):
    """
    Affiche une surface de texte centrée sur une position.

    Parameters
    ----------
    text : string
        Le texte à afficher
    position_center : int * int
        La position du centre du texte
    color : int * int * int, optionnel
        La couleur du texte
    font : Font, optionnel
        La fonte
    bold : bool, optionnel
        Indique si le texte doit être en gras
    """
    if font is None:
        ut.font(None, cf.TEXT_FONT_SIZE)
    if bold:
        font.set_bold(True)
    size_text = font.size(text)
    position = (int(position_center[0] - size_text[0]/2),
                int(position_center[1] - size_text[1]/2))
    txtgen = font.render(text, True, color)
    cf.DISPLAYSURF.blit(txtgen, position)
