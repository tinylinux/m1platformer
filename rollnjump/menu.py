# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Gestion des menus."""

import os
import rollnjump.conf as cf
import rollnjump.utilities as ut

FONT_PIXEL = os.path.join(cf.ASSETS, "font", "punk_rockf.ttf")
"""Chemin vers la police"""

CHARS_LOW = "azertyuiopqsdfghjklmwxcvbn1234567890"
"""Caractères acceptés, en minuscules"""
CHARS_CAP = "AZERTYUIOPQSDFGHJKLMWXCVBN1234567890"
"""Caractères acceptés, en majuscules"""


def scaled_mouse_pos(mouse):  # pragma: no cover
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
    scale_factor_x = cf.SCREEN_WIDTH / window_dimensions[0]
    scale_factor_y = cf.SCREEN_HEIGHT / window_dimensions[1]

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
    """
    Boutons pour les menus.

    Attributes
    ----------
    position : int * int
        Position du bouton
    size : int * int
        Taille du bouton
    rect : Rect
        Rectangle du bouton
    """

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
    """
    Boutons aillant du texte comme étiquette.

    Attributes
    ----------
    text : str
        Étiquette du bouton
    text_position :
        Position de l'étiquette
    """

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
        self.text = ut.font(None, 48).render(text, True, cf.BLACK)
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
    lang : str
        Langue à afficher (sous-repertoire à utiliser)
    """

    def __init__(self, position, size, image, image_hover, lang=""):
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
        lang : str, optionnel
            Langue à afficher (sous-repertoire à utiliser)
        """
        super().__init__(position, size)
        self.image = image
        self.image_hover = image_hover
        self.lang = lang

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
            cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                                                           self.lang,
                                                           self.image_hover)),
                                self.position)
        else:
            cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                                                           self.lang,
                                                           self.image)),
                                self.position)

    def changlang(self, lang):
        """
        Changer la langue du bouton.

        Parameters
        ----------
        lang : str
            Langue à utiliser
        """
        self.lang = lang


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


Oneplayer_pos = (358, 323)
Oneplayer_size = (100, 100)
Oneplayer_idle = 'oneplayer.png'
Oneplayer_hover = 'oneplayerpushed.png'
oneplayer_button = ButtonImage(
    Oneplayer_pos,
    Oneplayer_size,
    Oneplayer_idle,
    Oneplayer_hover
)
"""Bouton pour lancer le jeu à un joueur."""

Multiplayer_pos = (591, 323)
Multiplayer_size = (100, 100)
Multiplayer_idle = 'multiplayer.png'
Multiplayer_hover = 'multiplayerpushed.png'
multiplayer_button = ButtonImage(
    Multiplayer_pos,
    Multiplayer_size,
    Multiplayer_idle,
    Multiplayer_hover
)
"""Bouton pour lancer le jeu en multijoueur."""

Settings_pos = (824, 323)
Settings_size = (100, 100)
Settings_idle = 'settings.png'
Settings_hover = 'settingspushed.png'
settings_button = ButtonImage(
    Settings_pos,
    Settings_size,
    Settings_idle,
    Settings_hover
)
"""Bouton des réglages."""

Records_pos = (358, 460)
Records_size = (250, 75)
Records_idle = 'top5.png'
Records_hover = 'top5pushed.png'
records_button = ButtonImage(
    Records_pos,
    Records_size,
    Records_idle,
    Records_hover
)
"""Bouton des meilleurs scores."""

Credits_pos = (674, 460)
Credits_size = (250, 75)
Credits_idle = 'credits.png'
Credits_hover = 'creditspushed.png'
credits_button = ButtonImage(
    Credits_pos,
    Credits_size,
    Credits_idle,
    Credits_hover
)
"""Bouton des crédits."""

Restart_pos = (357, 482)
Restart_size = (567, 101)
Restart_idle = 'playagain.png'
Restart_hover = 'playagainpushed.png'
restart_button = ButtonImage(
    Restart_pos,
    Restart_size,
    Restart_idle,
    Restart_hover,
    "fr"
)
"""Bouton pour recommencer le jeu."""

Start_pos = (357, 552)
Start_size = (567, 101)
Start_idle = 'begin.png'
Start_hover = 'beginpushed.png'
start_button = ButtonImage(
    Start_pos,
    Start_size,
    Start_idle,
    Start_hover,
    "fr"
)
"""Bouton pour commencer une partie."""

Return_pos = (20, 20)
Return_size = (100, 100)
Return_idle = 'return.png'
Return_hover = 'returnpushed.png'
return_button = ButtonImage(
    Return_pos,
    Return_size,
    Return_idle,
    Return_hover
)
"""Bouton pour revenir au menu."""

Language_pos = (357, 241)
Language_size = (567, 101)
Language_idle = 'language.png'
Language_hover = 'languagepushed.png'
language_button = ButtonImage(
    Language_pos,
    Language_size,
    Language_idle,
    Language_hover,
    "fr"
)
"""Bouton pour changer la langue dans les paramètres."""

Commands_pos = (357, 379)
Commands_size = (567, 101)
Commands_idle = 'controls.png'
Commands_hover = 'controlspushed.png'
commands_button = ButtonImage(
    Commands_pos,
    Commands_size,
    Commands_idle,
    Commands_hover,
    "fr"
)
"""Bouton pour changer les touches."""

Sound_pos = (1168, 11)
Sound_size = (100, 100)
Sound_idle = 'soundon.png'
Sound_hover = 'soundonpushed.png'
sound_button = ButtonImage(
    Sound_pos,
    Sound_size,
    Sound_idle,
    Sound_hover
)
"""Bouton pour couper ou remettre la musique."""

# Boutons pour chaque langue
Flag_size = (180, 120)
Flag_pos = [(418, 369), (684, 369)]
Flag_idle = ['fr.png', 'en.png']
Flag_hover = ['fr_hover.png', 'en_hover.png']

flagbutton = []
"""Liste des boutons pour les langues."""
flagbutton.append(
    ButtonImage(
        Flag_pos[0], Flag_size,
        Flag_idle[0],
        Flag_hover[0],
        "flag"
    )
)
flagbutton.append(
    ButtonImage(
        Flag_pos[1], Flag_size,
        Flag_idle[1],
        Flag_hover[1],
        "flag"
    )
)

# Boutons pour choisir le nombre de joueurs
Multi_size = (100, 100)
Multi_pos = [(cf.SCREEN_WIDTH // 8 + (i + 1) * cf.SCREEN_WIDTH // 4 - 50, 150)
             for i in range(cf.NB_PLAYERS_MAX)]
Multi_idle = [str(i + 2) + ".png" for i in range(cf.NB_PLAYERS_MAX)]
Multi_hover = [str(i + 2) + "pushed.png" for i in range(cf.NB_PLAYERS_MAX)]
multi_button = []
"""Liste des boutons pour choisir le nombre de joueurs"""
for i in range(cf.NB_PLAYERS_MAX - 1):
    multi_button.append(
        ButtonImage(
            Multi_pos[i],
            Multi_size,
            Multi_idle[i],
            Multi_hover[i]
        )
    )

Multi_nb_pos = (cf.SCREEN_WIDTH // 2, 70)

# Traductions
MULTIMENU = {
    "fr": "Nombre de joueurs :",
    "en": "Number of players:"
}
"""Dictionnaire pour traduire le menu multijoueur."""

INDICBUTTON = {
    "fr": "Pour sauter, appuyer sur ",
    "en": "To jump, press "
}
"""Dictionnaire pour traduire l'instruction de saut."""

NOSCORES = {
    "fr": "Pas de scores",
    "en": "No scores"
}
"""Dictionnaire pour traduire qu'il n'y a pas de scores."""

Player_pos = (490, 350)
Player_size = (300, 50)
player_name_area = InputZone(
    Player_pos,
    Player_size,
    ut.font(FONT_PIXEL, 3 * cf.RESULT_FONT_SIZE // 4)
)
"""Zone de texte pour le pseudo du joueur."""


def print_image(image, position, scale=1):
    """
    Affiche une image à une position donnée.

    Parameters
    ----------
    image : string
        Le chemin vers l'image dans les fichiers
    position : int * int
        Les coordonnées de l'image
    scale : int
        Le facteur d'échelle
    """
    img = ut.load_image(image)
    w, h = img.get_rect().size
    img = ut.resize(img, (w * scale, h * scale))
    cf.DISPLAYSURF.blit(img, position)


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
        font = ut.font(None, cf.TEXT_FONT_SIZE)
    if bold:
        font.set_bold(True)
    size_text = font.size(text)
    position = (int(position_center[0] - size_text[0] / 2),
                int(position_center[1] - size_text[1] / 2))
    txtgen = font.render(text, True, color)
    cf.DISPLAYSURF.blit(txtgen, position)
