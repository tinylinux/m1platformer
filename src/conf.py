""" Stocke des variables partagées entre les différents fichiers """
import pygame

ch, cw = pygame.display.Info().current_h, pygame.display.Info().current_w

SCREEN_WIDTH = (cw * 5)//7
SCREEN_HEIGHT = min((ch * 8)//9, 9*SCREEN_WIDTH//16)
SPEED = 5           # vitesse initiale de défilement du sol
SOL_HAUT = (SCREEN_HEIGHT - 117)      # La hauteur du sol en général
SOL_LONG = 609      # La longueur d'un bloc du sol en général
SOL_IMG = "assets/img/plantes.png"

ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
sol = pygame.sprite.Group()

background = pygame.image.load("assets/img/fond.jpg")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
