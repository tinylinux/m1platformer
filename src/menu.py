"""Gestion des menus"""

import src.conf as cf
import src.utilities as ut

FONT_PIXEL = "assets/font/punk_rockf.ttf"

CHARS_LOW = "azertyuiopqsdfghjklmwxcvbn1234567890"
CHARS_CAP = "AZERTYUIOPQSDFGHJKLMWXCVBN1234567890"


def mouse_on_button(mouse, button_pos, button_size):
    """Renvoie si la souris est située sur le bouton.
    mouse : int * int, position de la souris
    button_pos : int * int, position du bouton
    button_size : int * int, largeur * hauteur du bouton"""

    # Récupération de la dimension de la fenêtre
    window_dimensions = ut.get_screen_size()

    # Calcul du facteur d'échelle
    scale_factor_x = cf.SCREEN_WIDTH/window_dimensions[0]
    scale_factor_y = cf.SCREEN_HEIGHT/window_dimensions[1]

    # Position de la sourie ajustée
    new_mouse = mouse[0] * scale_factor_x, mouse[1] * scale_factor_y

    return(button_pos[0] <= new_mouse[0] <= button_pos[0] + button_size[0]
           and button_pos[1] <= new_mouse[1] <= button_pos[1] + button_size[1])


class Button:  # pylint: disable=too-few-public-methods
    """ Classe des boutons pour les menus"""
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.rect = ut.create_rect([position[0], position[1],
                                    size[0], size[1]])

    def click(self, mouse):
        """Renvoie si la souris est sur le bouton"""
        return mouse_on_button(mouse, self.position, self.size)


class ButtonText(Button):
    """Classe des boutons affichant du texte"""
    def __init__(self, position, size, text):
        super().__init__(position, size)
        self.text = text
        self.text_position = (position[0] + 10, position[1] + 10)

    def print(self, mouse):
        """Affiche le bouton"""
        if mouse_on_button(mouse, self.position, self.size):
            ut.draw_rect(cf.DISPLAYSURF, cf.HOVER, self.rect)
        else:
            ut.draw_rect(cf.DISPLAYSURF, cf.IDLE, self.rect)
        cf.DISPLAYSURF.blit(self.text, self.text_position)


class ButtonImage(Button):
    """Classe des boutons affichant une image"""
    def __init__(self, position, size, image, image_hover):
        super().__init__(position, size)
        self.image = image
        self.image_hover = image_hover

    def print(self, mouse):
        """Affiche le bouton"""
        if mouse_on_button(mouse, self.position, self.size):
            cf.DISPLAYSURF.blit(ut.load_image(self.image_hover),
                                self.position)
        else:
            cf.DISPLAYSURF.blit(ut.load_image(self.image), self.position)


class InputZone(Button):
    """Classe des zones dans lesquelles on peut entrer du texte"""
    def __init__(self, position, size,
                 font=ut.font(None, cf.INPUT_FONT_SIZE)):
        """position : int * int, position du bouton
        size : int * int, largeur * hauteur du bouton
        font : Font, la fonte"""
        super().__init__(position, size)
        self.input = ""
        self.selected = False
        self.text_position = (position[0] + 10, position[1] + 10)
        self.font = font

    def print(self):
        """Affiche la zone et le texte entré"""
        ut.draw_rect(cf.DISPLAYSURF, cf.IDLE, self.rect)
        cf.DISPLAYSURF.blit(self.font.render(self.input, True, cf.WHITE),
                            self.text_position)

    def select(self):
        """Active la sélection de la zone"""
        self.selected = True

    def deselect(self):
        """Désactive la sélection de la zone"""
        self.selected = False

    def read(self, key):
        """Lit les caractères entrés"""
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
oneplayer_button = ButtonImage((358, 323), (100, 100),
                                "assets/img/ui/oneplayer.png",
                                "assets/img/ui/oneplayerpushed.png")

multiplayer_button = ButtonImage((591, 323), (100, 100),
                                    "assets/img/ui/multiplayer.png",
                                    "assets/img/ui/multiplayerpushed.png")

settings_button = ButtonImage((824, 323), (100, 100),
                                "assets/img/ui/settings.png",
                                "assets/img/ui/settingspushed.png")

records_button = ButtonImage((358, 460), (250, 75),
                                "assets/img/ui/top5.png",
                                "assets/img/ui/top5pushed.png")

credits_button = ButtonImage((674, 460), (250, 75),
                                "assets/img/ui/credits.png",
                                "assets/img/ui/creditspushed.png")

restart_button = ButtonImage((440, 500), (401, 123),
                                "assets/img/ui/playagain.png",
                                "assets/img/ui/playagainpushed.png")

return_button = ButtonImage((20, 20), (100, 100),
                            "assets/img/ui/return.png",
                            "assets/img/ui/returnpushed.png")

# Buttons for each language
flagbutton = []
flagbutton.append(
    ButtonImage(
        (418, 369), (180, 120),
        "assets/img/ui/flag/fr.png",
        "assets/img/ui/flag/fr_hover.png"
    )
)
flagbutton.append(
    ButtonImage(
        (684, 369), (180, 120),
        "assets/img/ui/flag/en.png",
        "assets/img/ui/flag/en_hover.png"
    )
)


def print_image(image, position):
    """Affiche une image à une position donnée.
    image : string, le chemin vers l'image dans les fichiers
    position : int * int, les coordonnées du coin supérieur gauche"""
    cf.DISPLAYSURF.blit(ut.load_image(image), position)


def print_text(text, position_center, color=cf.WHITE,
               font=ut.font(None, cf.TEXT_FONT_SIZE), bold=False):
    """Affiche une surface de texte centrée sur une position.
    text : string, le texte à afficher
    position_center : int * int, la position du centre du texte
    color : int * int * int, la couleur
    font : ut.font, la fonte
    bold : bool, si la fonte doit être en gras"""
    if bold:
        font.set_bold(True)
    size_text = font.size(text)
    position = (int(position_center[0] - size_text[0]/2),
                int(position_center[1] - size_text[1]/2))
    txtgen = font.render(text, True, color)
    cf.DISPLAYSURF.blit(txtgen, position)
