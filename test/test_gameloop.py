# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Fichier de test pour gameloop."""

import os
import rollnjump.main as main
import rollnjump.score as scre
import rollnjump.menu as mn
import rollnjump.conf as cf
import rollnjump.utilities as ut
import rollnjump.player as plyr
import rollnjump.gameloop as gml
import rollnjump.sprites as spt
import rollnjump.lang as lg
import rollnjump.key as ky

cf.SCORES = os.path.join(os.path.dirname(__file__), "test_score.txt")
lg.FILE = os.path.join(os.path.dirname(__file__), "test_lang.txt")
scre.init_best_score()


# Test pour main_loop

def test_main_loop_event():
    """Test pour la fonction main_loop."""
    cf.NB_PLAYERS = 3
    _, players = main.initialization(False)
    assert len(players) == 3

    # Menu
    cf.LANG = "fr"
    cf.STATE = cf.State.menu
    players[0].jump()  # Pour tester move
    players = gml.main_loop(players, (0, 0))
    assert players[0].vel.y != 0

    # Setup (simple appel pour créer les boutons)
    cf.STATE = cf.State.setup
    players = gml.main_loop(players, (0, 0))
    players = gml.reset_world()

    # Languages
    cf.STATE = cf.State.languages
    players = gml.main_loop(players, (0, 0))

    # Langchange
    cf.STATE = cf.State.langchange
    players = gml.main_loop(players, (0, 0))
    players = gml.reset_world()

    # Multiplayer_set
    cf.STATE = cf.State.multiplayer_set
    players = gml.main_loop(players, (0, 0))
    players = gml.reset_world()

    # Keyset
    cf.STATE = cf.State.keyset
    players = gml.main_loop(players, (0, 0))
    cf.CAPT = True
    players = gml.main_loop(players, (0, 0))

    cf.NB_PLAYERS = 3
    players = gml.reset_world()

    # In game
    cf.FRAMES = 0
    cf.STATE = cf.State.ingame
    for _ in range(60):
        players = gml.main_loop(players, (0, 0))
    assert cf.FRAMES == 60
    assert cf.SECONDS == 1
    players[0].pos = ut.Vec(-100, -100)  # Joueur 1 a perdu
    players = gml.main_loop(players, (0, 0))
    assert not players[0].alive
    assert cf.STATE == cf.State.ingame
    players[1].pos = ut.Vec(-100, -100)  # Joueur 2 a perdu
    players = gml.main_loop(players, (0, 0))
    players = gml.main_loop(players, (0, 0))
    assert not players[1].alive
    assert cf.STATE == cf.State.gameover_multi
    assert plyr.WINNER == 2

    cf.NB_PLAYERS = 1
    cf.STATE = cf.State.ingame
    players = gml.reset_world()
    assert len(players) == 1
    players[0].pos = ut.Vec(-100, -100)
    cf.SECONDS = 30  # Record pour l'étape suivante
    players = gml.main_loop(players, (0, 0))
    players = gml.main_loop(players, (0, 0))
    assert cf.STATE == cf.State.gameover

    # Game over
    cf.CAPT = True
    players = gml.main_loop(players, (0, 0))
    cf.CAPT = False
    scre.PLAYER = "test"
    scre.set_best_score(cf.SECONDS)
    players = gml.main_loop(players, (0, 0))
    assert cf.NEWHS
    assert cf.NEWRC
    assert scre.get_scores()[0][0] == 30
    assert scre.get_best_score() == 30
    players = gml.reset_world()
    cf.STATE = cf.State.ingame
    cf.SECONDS = 29
    players[0].alive = False
    players = gml.main_loop(players, (0, 0))
    assert cf.STATE == cf.State.gameover
    cf.CAPT = False
    scre.PLAYER = "test"
    scre.set_best_score(cf.SECONDS)
    players = gml.main_loop(players, (0, 0))
    assert scre.get_best_score() == 30
    assert cf.NEWHS
    assert not cf.NEWRC
    assert scre.get_scores()[1][0] == 29

    # Game over multi
    cf.STATE = cf.State.gameover_multi
    # Simple appel à la fonction
    players = gml.main_loop(players, (0, 0))

    # Highscores
    cf.STATE = cf.State.highscore
    # Appel avec un tableau non vide
    players = gml.main_loop(players, (0, 0))
    scre.init_best_score()  # Suppression du contenu
    # Appel avec un tableau vide
    players = gml.main_loop(players, (0, 0))


def test_event():
    """Test pour la fonction event_handling."""
    _, players = main.initialization(False)

    # Test pour KEY_DOWN
    cf.STATE = cf.State.ingame
    for i, P in enumerate(players):
        event = ut.make_event(ut.KEYDOWN, {'key': plyr.JUMP_KEYS[i]})
        players = gml.event_handling(players, event, (0, 0))
        assert P.vel.y == -cf.V_JMP

    cf.CAPT = True
    cf.STATE = cf.State.keyset
    players = gml.event_handling(players,
                                 ut.make_event(ut.KEYDOWN,
                                               {'key': ut.K_ESCAPE}),
                                 (0, 0))
    assert not cf.CAPT

    cf.CAPT_PLYR = 1
    cf.CAPT = True
    players = gml.event_handling(
        players, ut.make_event(ut.KEYDOWN, {'key': ut.K_s}), (0, 0))
    assert not cf.CAPT
    assert plyr.JUMP_KEYS[1] == ut.K_s

    cf.STATE = cf.State.gameover
    cf.CAPT = True
    mn.player_name_area.select()
    players = gml.event_handling(
        players, ut.make_event(ut.KEYDOWN, {'key': ut.K_s}), (0, 0))
    assert mn.player_name_area.input == 'S'
    players = gml.event_handling(
        players, ut.make_event(ut.KEYDOWN, {'key': ut.K_RETURN}), (0, 0))
    assert scre.PLAYER == 'S'
    assert not cf.CAPT
    assert not mn.player_name_area.selected

    cf.NB_PLAYERS = 3
    players = gml.reset_world()

    # Tests pour MOUSEBUTTONDOWN
    cf.STATE = cf.State.menu
    players[0].jump()
    event = ut.make_event(ut.MOUSEBUTTONDOWN)
    players = gml.event_handling(players, event, mn.Oneplayer_pos)
    assert cf.NB_PLAYERS == 1
    assert players[0].vel.y == 0
    assert cf.STATE == cf.State.ingame
    for bloc in spt.ground:
        assert not bloc.FLAG_creation

    cf.STATE = cf.State.menu
    players = gml.event_handling(players, event, mn.Multiplayer_pos)
    players = gml.event_handling(players, event,
                                 mn.Multi_pos[cf.NB_PLAYERS_MAX - 2])
    assert cf.NB_PLAYERS == 4
    players = gml.event_handling(players, event, mn.Start_pos)
    assert players[0].vel.y == 0
    assert cf.STATE == cf.State.ingame
    for bloc in spt.ground:
        assert not bloc.FLAG_creation

    cf.STATE = cf.State.menu
    players = gml.event_handling(players, event, mn.Records_pos)
    assert cf.STATE == cf.State.highscore

    cf.STATE = cf.State.menu
    players = gml.event_handling(players, event, mn.Settings_pos)
    assert cf.STATE == cf.State.setup

    cf.STATE = cf.State.languages
    lg.set_lang(lg.AVAILABLE[0])
    players = gml.event_handling(players, event, mn.Flag_pos[1])
    assert cf.STATE == cf.State.menu
    assert cf.LANG == lg.AVAILABLE[1]

    cf.STATE = cf.State.languages
    lg.set_lang(lg.AVAILABLE[1])
    players = gml.event_handling(players, event, mn.Flag_pos[0])
    assert cf.STATE == cf.State.menu
    assert cf.LANG == lg.AVAILABLE[0]

    cf.STATE = cf.State.multiplayer_set
    players = gml.event_handling(players, event, mn.Multi_pos[1])
    assert cf.NB_PLAYERS == 3
    players = gml.event_handling(players, event, mn.Return_pos)
    assert cf.STATE == cf.State.menu
    cf.STATE = cf.State.multiplayer_set
    players = gml.event_handling(players, event, mn.Start_pos)
    assert cf.STATE == cf.State.ingame

    cf.STATE = cf.State.langchange
    players = gml.event_handling(players, event, mn.Flag_pos[0])
    assert cf.STATE == cf.State.setup
    assert cf.LANG == lg.AVAILABLE[0]

    cf.STATE = cf.State.langchange
    players = gml.event_handling(players, event, mn.Flag_pos[1])
    assert cf.STATE == cf.State.setup
    assert cf.LANG == lg.AVAILABLE[1]

    cf.STATE = cf.State.langchange
    lg.set_lang(lg.AVAILABLE[0])
    players = gml.event_handling(players, event, mn.Return_pos)
    assert cf.STATE == cf.State.setup
    assert cf.LANG == lg.AVAILABLE[0]

    cf.STATE = cf.State.gameover
    players[0].jump()
    players = gml.event_handling(players, event, mn.Return_pos)
    assert players[0].vel.y == 0
    assert cf.STATE == cf.State.menu

    cf.STATE = cf.State.gameover
    players[0].jump()
    players = gml.event_handling(players, event, mn.Restart_pos)
    assert players[0].vel.y == 0
    for bloc in spt.ground:
        assert not bloc.FLAG_creation
    assert cf.STATE == cf.State.ingame

    cf.STATE = cf.State.highscore
    players = gml.event_handling(players, event, mn.Return_pos)
    assert cf.STATE == cf.State.menu

    cf.STATE = cf.State.setup
    players = gml.event_handling(players, event, mn.Language_pos)
    assert cf.STATE == cf.State.langchange

    cf.CAPT = True
    cf.STATE = cf.State.setup
    players = gml.event_handling(players, event, mn.Commands_pos)
    assert cf.STATE == cf.State.keyset
    assert not cf.CAPT

    cf.STATE = cf.State.setup
    players = gml.event_handling(players, event, mn.Return_pos)
    assert cf.STATE == cf.State.menu

    cf.STATE = cf.State.keyset
    players = gml.event_handling(players, event, mn.Return_pos)
    assert cf.STATE == cf.State.setup

    cf.CAPT = False
    cf.STATE = cf.State.keyset
    players = gml.event_handling(players, event, ky.Modify_pos[2])
    assert cf.CAPT
    assert cf.CAPT_PLYR == 2
