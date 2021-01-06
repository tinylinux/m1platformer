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


def initialization(graphical, music=False):
    """
    Initialisation des variables et des surfaces.

    Parameters
    ----------
    graphical : bool
        Indique si le jeu doit être lancé en mode graphique ou non
    music : bool, optionnel
        Indique si on lance la musique

    Returns
    -------
    Clock * Player list
        Une horloge pour le contrôle de la vitesse et la liste des joueurs
    """
    # Initialisation de la fenêtre
    cf.DISPLAYSURF, cf.WINDOWSURF = \
        ut.initialize_window("assets/img/monogreen/monogreen3.png",
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
    players = [plyr.Player(plyr.COLORS[i]) for i in range(cf.NB_PLAYERS)]

    # Initialisation du monde
    wrld.initgen()

    # Lance la musique
    if music:
        ut.load_music(cf.MUSIC)
        ut.play_music()

    return(FramePerSec, players)


def main():
    """Fonction principale du jeu."""
    FramePerSec, players = initialization(True, True)

    while True:  # Boucle du jeu

        for event in ut.get_events():  # Gestion des événements
            players = gml.event_handling(players, event)

        wrld.update()  # Mise à jour de l'environnement

        players = gml.main_loop(players)  # Mise à jour du jeu

        # Gestion de l'affichage
        dim = ut.get_screen_size()
        ut.resize(cf.DISPLAYSURF, dim, cf.WINDOWSURF)
        ut.update_screen()
        FramePerSec.tick(cf.FPS)


if __name__ == "__main__":
    main()
