"""Gestion des menus"""

import pygame
import src.conf as cf


white = (255,255,255) 
light = (170,170,170) 
dark = (100,100,100)
smallfont = pygame.font.SysFont('Corbel',35)

def mouse_on_button(mouse, button_pos, button_size):
    return(int(button_pos[0] - button_size[0]/2) <= mouse[0] <= int(button_pos[0] + button_size[0]/2)\
        and int(button_pos[1] - button_size[1]/2) <= mouse[1] <= int(button_pos[1] + button_size[1]/2))

class Button():
    """ Classe des boutons pour les menus"""
    def __init__(self, position, size, text):
        self.position = position
        self.size = size
        self.text = text
        self.rect = pygame.Rect([int(position[0] - size[0]/2), int(position[1] - size[1]/2), size[0], size[1]])
        self.text_position = (int(position[0] - size[0]/2) + 10, int(position[1] - size[1]/2) + 10)
    
    def print(self, mouse):
        """Affiche le bouton"""
        if mouse_on_button(mouse, self.position, self.size):
            pygame.draw.rect(cf.DISPLAYSURF, light, self.rect)
        else:
            pygame.draw.rect(cf.DISPLAYSURF, dark, self.rect)
        cf.DISPLAYSURF.blit(self.text, self.text_position)

    def click(self, mouse):
        """Renvoie si la souris est sur le bouton"""
        return(mouse_on_button(mouse, self.position, self.size))

start_button = Button((int(1280/2), int(720/2)),\
    (160, 40),\
    smallfont.render('Commencer' , True , white))

restart_button = Button((int(1280/2), int(720/2)),\
    (185, 40),\
    smallfont.render('Recommencer' , True , white))