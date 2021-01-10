# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Module principal du jeu."""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# pylint: disable=wrong-import-position
import rollnjump.utilities as ut  # noqa: E402
import rollnjump.conf as cf  # noqa: E402
import rollnjump.lang as lg  # noqa: E402
import rollnjump.worldgen as wrld  # noqa: E402
import rollnjump.player as plyr  # noqa: E402
import rollnjump.key as ky  # noqa: E402
import rollnjump.gameloop as gml  # noqa: E402
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
        ut.initialize_window(os.path.join(cf.ASSETS, "img",
                                          "monogreen", "monogreen3.png"),
                             "Roll 'n' jump",
                             cf.SCREEN_WIDTH,
                             cf.SCREEN_HEIGHT,
                             graphical)

    FramePerSec = ut.initialize_clock()

    # Initialisation des modules
    wrld.init_modules()

    # Initialisation de la langue
    if not os.path.isfile(lg.FILE):
        lg.init_lang()
    lg.get_lang()

    # Initialisation des commandes
    if not os.path.isfile(ky.FILE):
        ky.init_com()
    ky.get_keys()

    # Initialisation du joueur
    players = [plyr.Player(cf.COLORS[i]) for i in range(cf.NB_PLAYERS)]

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
