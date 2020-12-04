""" Fichier principal du jeu """

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# pylint: disable=wrong-import-position
import pygame  # noqa: E402
pygame.init()
import src.conf as cf  # noqa: E402
import src.worldgen as wrld  # noqa: E402
import src.player as plyr  # noqa: E402
import src.gameloop as gml  # noqa: E402
# pylint: enable=wrong-import-position


# Initialisation de la fenêtre
cf.DISPLAYSURF = pygame.Surface((cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
cf.WINDOWSURF = pygame.display.set_mode((cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT),
                                        flags=pygame.RESIZABLE)

FPS = 60
FramePerSec = pygame.time.Clock()

pygame.display.set_icon(
    pygame.image.load("assets/img/mono/mono3.png"))
pygame.display.set_caption("Roll 'n' jump")

# Initialisation du joueur
P = plyr.Player()

# Initialisation du monde
wrld.initgen()

while True:  # Boucle du jeu

    for event in pygame.event.get():  # Gestion des événements
        P = gml.event_handling(P, event)

    wrld.update()  # Mise à jour de l'environnement

    P = gml.main_loop(P)  # Mise à jour du jeu

    # Gestion de l'affichage
    dim = pygame.display.get_surface().get_size()
    pygame.transform.scale(cf.DISPLAYSURF, dim, cf.WINDOWSURF)
    pygame.display.flip()
    FramePerSec.tick(FPS)
