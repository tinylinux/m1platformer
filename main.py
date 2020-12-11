""" Fichier principal du jeu """

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# pylint: disable=wrong-import-position
import src.utilities as ut  # noqa: E402
ut.initialize()
import src.conf as cf  # noqa: E402
import src.worldgen as wrld  # noqa: E402
import src.player as plyr  # noqa: E402
import src.gameloop as gml  # noqa: E402
# pylint: enable=wrong-import-position


# Initialisation de la fenêtre
cf.DISPLAYSURF, cf.WINDOWSURF = \
    ut.initialize_window("assets/img/mono/mono3.png",
                         "Roll 'n' jump",
                         cf.SCREEN_WIDTH,
                         cf.SCREEN_HEIGHT)

FPS = 60
FramePerSec = ut.initialize_clock()

# Initialisation du joueur
players = [plyr.Player()]

# Initialisation du monde
wrld.initgen()

while True:  # Boucle du jeu

    for event in ut.get_events():  # Gestion des événements
        players = gml.event_handling(players, event)

    wrld.update()  # Mise à jour de l'environnement

    players = gml.main_loop(players)  # Mise à jour du jeu

    # Gestion de l'affichage
    dim = ut.get_screen_size()
    ut.resize(cf.DISPLAYSURF, dim, cf.WINDOWSURF)
    ut.update_screen()
    FramePerSec.tick(FPS)
