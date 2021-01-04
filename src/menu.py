"""Gestion des menus."""

import os
import src.conf as cf
import src.utilities as ut

FONT_PIXEL = "assets/font/punk_rockf.ttf"
"""Chemin vers la police"""

CHARS_LOW = "azertyuiopqsdfghjklmwxcvbn1234567890"
"""Caractères acceptés, en minuscules"""
CHARS_CAP = "AZERTYUIOPQSDFGHJKLMWXCVBN1234567890"
"""Caractères acceptés, en majuscules"""


def scaled_mouse_pos(mouse):
    """
    Renvoie la position de la souris mise à l'échelle de l'image.

    Parameters
    ----------
    mouse : int * int
        La position réelle de la souris

    Returns
    -------
    int * int
        La position mise à l'échelle
    """
    # Récupération de la dimension de la fenêtre
    window_dimensions = ut.get_screen_size()

    # Calcul du facteur d'échelle
    scale_factor_x = cf.SCREEN_WIDTH/window_dimensions[0]
    scale_factor_y = cf.SCREEN_HEIGHT/window_dimensions[1]

    return mouse[0] * scale_factor_x, mouse[1] * scale_factor_y


def mouse_on_button(scaled_mouse, button_pos, button_size):
    """
    Indique si le pointeur de la souris est sur le bouton.

    Parameters
    ----------
    scaled_mouse : int * int
        Position du pointeur de la souris mise à l'échelle
    button_pos : int * int
        Position du bouton
    button_size : int * int
        Largeur et hauteur du bouton

    Returns
    -------
    bool
        True si le pointeur est sur le bouton
    """
    return(button_pos[0] <= scaled_mouse[0]
           <= button_pos[0] + button_size[0]
           and button_pos[1] <= scaled_mouse[1]
           <= button_pos[1] + button_size[1])


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

    def print(self, mouse, pushed=False):
        """
        Affiche le bouton.

        Parameters
        ----------
        mouse : int * int
            Position de la souris
        pushed : bool, optionnel
            Bouton enfoncé
        """
        if mouse_on_button(mouse, self.position, self.size) or pushed:
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

    def print(self, mouse, pushed=False):
        """
        Affiche le bouton.

        Parameters
        ----------
        mouse : int * int
            Position du pointeur de la souris
        pushed : bool, optionnel
            Bouton enfoncé
        """
        if mouse_on_button(mouse, self.position, self.size) or pushed:
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


# start_button = ButtonImage((440, 314), (401, 123), "assets/img/ui/begin.png",
#                            "assets/img/ui/beginpushed.png")

Oneplayer_pos = (358, 323)
Oneplayer_size = (100, 100)
Oneplayer_idle = os.path.join(cf.UI, 'oneplayer.png')
Oneplayer_hover = os.path.join(cf.UI, 'oneplayerpushed.png')
oneplayer_button = ButtonImage(
        Oneplayer_pos,
        Oneplayer_size,
        Oneplayer_idle,
        Oneplayer_hover
    )

Multiplayer_pos = (591, 323)
Multiplayer_size = (100, 100)
Multiplayer_idle = os.path.join(cf.UI, 'multiplayer.png')
Multiplayer_hover = os.path.join(cf.UI, 'multiplayerpushed.png')
multiplayer_button = ButtonImage(
        Multiplayer_pos,
        Multiplayer_size,
        Multiplayer_idle,
        Multiplayer_hover
    )

Settings_pos = (824, 323)
Settings_size = (100, 100)
Settings_idle = os.path.join(cf.UI, 'settings.png')
Settings_hover = os.path.join(cf.UI, 'settingspushed.png')
settings_button = ButtonImage(
        Settings_pos,
        Settings_size,
        Settings_idle,
        Settings_hover
    )

Records_pos = (358, 460)
Records_size = (250, 75)
Records_idle = os.path.join(cf.UI, 'top5.png')
Records_hover = os.path.join(cf.UI, 'top5pushed.png')
records_button = ButtonImage(
        Records_pos,
        Records_size,
        Records_idle,
        Records_hover
    )

Credits_pos = (674, 460)
Credits_size = (250, 75)
Credits_idle = os.path.join(cf.UI, 'credits.png')
Credits_hover = os.path.join(cf.UI, 'creditspushed.png')
credits_button = ButtonImage(
        Credits_pos,
        Credits_size,
        Credits_idle,
        Credits_hover
    )

Restart_pos = (440, 500)
Restart_size = (401, 123)
Restart_idle = os.path.join(cf.UI, 'playagain.png')
Restart_hover = os.path.join(cf.UI, 'playagainpushed.png')
restart_button = ButtonImage(
        Restart_pos,
        Restart_size,
        Restart_idle,
        Restart_hover
    )

Return_pos = (20, 20)
Return_size = (100, 100)
Return_idle = os.path.join(cf.UI, 'return.png')
Return_hover = os.path.join(cf.UI, 'returnpushed.png')
return_button = ButtonImage(
        Return_pos,
        Return_size,
        Return_idle,
        Return_hover
    )

# Buttons for each language
Flag_size = (180, 120)
Flag_pos = [(418, 369), (684, 369)]
Flag_idle = [os.path.join(cf.UI, 'flag', 'fr.png'),
             os.path.join(cf.UI, 'flag', 'en.png')]
Flag_hover = [os.path.join(cf.UI, 'flag', 'fr_hover.png'),
              os.path.join(cf.UI, 'flag', 'en_hover.png')]

flagbutton = []
flagbutton.append(
    ButtonImage(
        Flag_pos[0], Flag_size,
        Flag_idle[0],
        Flag_hover[0]
    )
)
flagbutton.append(
    ButtonImage(
        Flag_pos[1], Flag_size,
        Flag_idle[1],
        Flag_hover[1]
    )
)


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
