"""Fichier de test pour gameloop."""

import os
import main
import src.score as scre
import src.menu as mn
import src.conf as cf
import src.utilities as ut
import src.player as plyr
import src.gameloop as gml
import src.sprites as spt
import src.lang as lg

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
    cf.STATE = cf.State.menu
    players[0].jump()  # Pour tester move
    players = gml.main_loop(players, (0, 0))
    assert players[0].vel.y != 0

    # Languages
    cf.STATE = cf.State.languages
    players = gml.main_loop(players, (0, 0))

    # In game
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
    cf.LANG = "fr"
    players[0].pos = ut.Vec(-100, -100)
    cf.SECONDS = 30  # Record pour l'étape suivante
    players = gml.main_loop(players, (0, 0))
    players = gml.main_loop(players, (0, 0))
    assert cf.STATE == cf.State.gameover

    # Game over
    cf.STATE = cf.State.gameover
    cf.CAPT = False
    scre.PLAYER = "test"
    scre.set_best_score(cf.SECONDS)
    players = gml.main_loop(players, (0, 0))
    assert cf.NEWHS
    assert scre.get_scores()[0][0] == 30

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
    players = gml.reset_world()

    # Setup (simple appel pour créer les boutons)
    cf.STATE = cf.State.setup
    players = gml.main_loop(players, (0, 0))
    players = gml.reset_world()

    # Langchange
    cf.STATE = cf.State.langchange
    players = gml.main_loop(players, (0, 0))
    players = gml.reset_world()


def test_event():
    """Test pour la fonction event_handling."""
    _, players = main.initialization(False)

    # Test INC_SPEED
    cf.STATE = cf.State.ingame
    init_speed = cf.SPEED
    players = gml.event_handling(players, ut.make_event(ut.INC_SPEED), (0, 0))
    assert cf.SPEED == init_speed + 0.5
    players = gml.event_handling(players,
                                 ut.make_event(ut.KEYDOWN,
                                               {'key': ut.K_SPACE}),
                                 (0, 0))
    assert cf.SPEED == init_speed + 0.5

    players = gml.reset_world()

    # Test pour KEY_DOWN
    cf.STATE = cf.State.ingame
    for i, P in enumerate(players):
        event = ut.make_event(ut.KEYDOWN, {'key': plyr.JUMP_KEYS[i]})
        players = gml.event_handling(players, event, (0, 0))
        assert P.vel.y == -cf.V_JMP

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

    cf.STATE = cf.State.setup
    players = gml.event_handling(players, event, mn.Return_pos)
    assert cf.STATE == cf.State.menu
