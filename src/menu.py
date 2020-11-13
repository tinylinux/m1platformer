"""Gestion des menus"""

import pygame
import src.conf as cf


white = (255,255,255)
idle = (170,170,170)
hover = (100,100,100)
font = pygame.font.SysFont(None,35)

def mouse_on_button(mouse, button_pos, button_size):
    return(button_pos[0] <= mouse[0] <= button_pos[0] + button_size[0]\
        and button_pos[1] <= mouse[1] <= button_pos[1] + button_size[1])

class Button:
    """ Classe des boutons pour les menus"""
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.rect = pygame.Rect([position[0], position[1], size[0], size[1]])

    def click(self, mouse):
        """Renvoie si la souris est sur le bouton"""
        return(mouse_on_button(mouse, self.position, self.size))

class Button_text(Button):
    """Classe des boutons affichant du texte"""
    def __init__(self, position, size, text):
        super().__init__(position, size)
        self.text = text
        self.text_position = (position[0] + 10, position[1] + 10)

    def print(self, mouse):
        """Affiche le bouton"""
        if mouse_on_button(mouse, self.position, self.size):
            pygame.draw.rect(cf.DISPLAYSURF, hover, self.rect)
        else:
            pygame.draw.rect(cf.DISPLAYSURF, idle, self.rect)
        cf.DISPLAYSURF.blit(self.text, self.text_position)

class Button_image(Button):
    """Classe des boutons affichant une image"""
    def __init__(self, position, size, image, image_hover):
        super().__init__(position, size)
        self.image = image
        self.image_hover = image_hover

    def print(self, mouse):
        """Affiche le bouton"""
        if mouse_on_button(mouse, self.position, self.size):
            cf.DISPLAYSURF.blit(pygame.image.load(self.image_hover), self.position)
        else:
            cf.DISPLAYSURF.blit(pygame.image.load(self.image), self.position)

start_button = Button_image((440,300), (401,123), "assets/img/ui/begin.png", "assets/img/ui/beginpushed.png")

restart_button = Button_image((440,450), (401,123), "assets/img/ui/playagain.png", "assets/img/ui/playagainpushed.png")

def print_image(image, position):
    """Affiche une image à une position donnée.
    image : string, le chemin vers l'image dans les fichiers
    position : int * int, les coordonnées du coin supérieur gauche"""
    cf.DISPLAYSURF.blit(pygame.image.load(image), position)

def print_text(text, position_center, color = white, font = pygame.font.SysFont(None, 25)):
    """Affiche une surface de texte centrée sur une position.
    text : string, le texte à afficher
    position_center : int * int, la position du centre du texte
    color : int * int * int, la couleur
    font : pygame.font.Font, la fonte"""
    size_text = font.size(text)
    position = (int(position_center[0] - size_text[0]/2), int(position_center[1] - size_text[1]/2))
    cf.DISPLAYSURF.blit(font.render(text, True, color), position)