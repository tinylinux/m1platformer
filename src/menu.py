"""Gestion des menus"""

import pygame
import src.conf as cf


white = (255,255,255) 
idle = (170,170,170) 
hover = (100,100,100)
smallfont = pygame.font.SysFont(None,35)

def mouse_on_button(mouse, button_pos, button_size):
    return(int(button_pos[0] - button_size[0]/2) <= mouse[0] <= int(button_pos[0] + button_size[0]/2)\
        and int(button_pos[1] - button_size[1]/2) <= mouse[1] <= int(button_pos[1] + button_size[1]/2))

class Button:
    """ Classe des boutons pour les menus"""
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.rect = pygame.Rect([int(position[0] - size[0]/2), int(position[1] - size[1]/2), size[0], size[1]])

    def click(self, mouse):
        """Renvoie si la souris est sur le bouton"""
        return(mouse_on_button(mouse, self.position, self.size))

class Button_text(Button):
    """Classe des boutons affichant du texte"""
    def __init__(self, position, size, text):
        super().__init__(position, size)
        self.text = text
        self.text_position = (int(position[0] - size[0]/2) + 10, int(position[1] - size[1]/2) + 10)
    
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
            cf.DISPLAYSURF.blit(self.image_hover, self.position)
        else:
            cf.DISPLAYSURF.blit(self.image, self.position)


start_button = Button_text((int(1280/2), int(720/2)),\
    (160, 40),\
    smallfont.render('Commencer' , True , white))

restart_button = Button_text((int(1280/2), int(720/2)),\
    (185, 40),\
    smallfont.render('Recommencer' , True , white))