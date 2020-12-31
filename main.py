"""Module principal du jeu."""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# pylint: disable=wrong-import-position
import src.utilities as ut  # noqa: E402
import src.conf as cf  # noqa: E402
import src.lang as lg  # noqa: E402
import src.worldgen as wrld  # noqa: E402
import src.player as plyr  # noqa: E402
import src.gameloop as gml  # noqa: E402
# pylint: enable=wrong-import-position


def initialization(graphical):
    """
    Initialisation des variables et des surfaces.

    Parameters
    ----------
    graphical : bool
        Indique si le jeu doit être lancé en mode graphique ou non

    Returns
    -------
    Clock * Player list
        Une horloge pour le contrôle de la vitesse, et la liste des joueurs
    """
    # Initialisation de la fenêtre
    cf.DISPLAYSURF, cf.WINDOWSURF = \
        ut.initialize_window("assets/img/mono/mono3.png",
                             "Roll 'n' jump",
                             cf.SCREEN_WIDTH,
                             cf.SCREEN_HEIGHT,
                             graphical)

    FramePerSec = ut.initialize_clock()

    # Initialisation de la langue
    if not os.path.isfile(lg.FILE):
        lg.init_lang()
    lg.get_lang()

    # Initialisation du joueur
    players = [plyr.Player() for _ in range(cf.NB_PLAYERS)]

    # Initialisation du monde
    wrld.initgen()

    return(FramePerSec, players)


def main(graphical):
    """
    Fonction principale du jeu.

    Parameters
    ----------
    graphical : bool
        Indique si le jeu doit être lancé en mode graphique ou non
    """
    FramePerSec, players = initialization(graphical)

    while True:  # Boucle du jeu

        for event in ut.get_events():  # Gestion des événements
            players = gml.event_handling(players, event, graphical)

        wrld.update()  # Mise à jour de l'environnement

        players = gml.main_loop(players, graphical)  # Mise à jour du jeu

        # Gestion de l'affichage
        if graphical:
            dim = ut.get_screen_size()
            ut.resize(cf.DISPLAYSURF, dim, cf.WINDOWSURF)
            ut.update_screen()
        FramePerSec.tick(cf.FPS)


if __name__ == "__main__":
    main(True)
