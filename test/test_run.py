"""Fichier de test d'un run."""

import os
import rollnjump.main as main
import rollnjump.menu as mn
import rollnjump.utilities as ut
import rollnjump.conf as cf
import rollnjump.gameloop as gml
import rollnjump.worldgen as wrld

cf.SCORES = os.path.join(os.path.dirname(__file__), "test_score.txt")
open(cf.SCORES, 'w').close()


def jump():
    """Simule un saut."""
    return ut.make_event(ut.KEYDOWN, {'key': ut.K_SPACE})


def clic(pos):
    """
    Simule un clic de souris.
    Parameters
    ----------
    pos : int * int
        la position de la souris
    """
    return ut.make_event(ut.MOUSEBUTTONDOWN, {"pos" : pos})


def do_event(players, event):
    """gère l'event simulé."""
    return gml.event_handling(players, event, (0,0))


def test_run():
    """
    Fais un test de run classique.
    Lance le jeu, clique sur jouer,
    et simule des sauts et des doubles sauts
    Parameters
    ----------
    nstep : int
        le nombre de secondes à effectuer
    """
    cf.NB_PLAYERS = 1
    # timer pour faire un double saut
    timer = 0
    _, players = main.initialization(False)
    # clique sur jouer à un joueur
    pos = mn.oneplayer_button.position
    players = gml.event_handling(players, clic(pos), pos)
    # boucle de jeu
    while players[0].alive:

        # Si on peut sauter, on saute
        if players[0].FLAG_JUMP:
            players = do_event(players, jump())
            timer = 20
        # Puis on fait un double saut 10 frames plus tard
        if timer == 0 and players[0].FLAG_JUMP_2:
            players = do_event(players, jump())
        else:
            timer-=1

        wrld.update()  # Mise à jour de l'environnement

        players = gml.main_loop(players, (0,0))

        assert cf.STATE == cf.State.ingame
    # on est mort
    players = gml.main_loop(players, (0,0))
    assert cf.STATE == cf.State.gameover

if __name__ == "__main__":
    test_run()
