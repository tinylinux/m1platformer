"""Fichier de test pour score."""

import os
from hypothesis import given
from hypothesis.strategies import characters, integers, text, lists, tuples
import main
import src.score as scre

scre.FILE = os.path.join(os.path.dirname(__file__), "test_score.txt")


@given(text())
def test_onlydigits(string):
    """Test pour la fonction onlydigits."""
    digits = scre.onlydigits(string)
    assert digits == '' or digits.isnumeric()


@given(text())
def test_onlyalphanum(string):
    """Test pour la fonction onlyalphanum."""
    alphanum = scre.onlyalphanum(string)
    assert alphanum == '' or alphanum.isalnum()


@given(integers())
def test_print(number):
    """Test pour les fonctions d'affichage."""
    # Simples appels aux fonctions
    main.initialization(False)
    scre.score(number)
    scre.score_endgame(number)
    scre.winner_endgame()


alphanum_char = characters(min_codepoint=0x30,
                           max_codepoint=0x7A,
                           blacklist_characters=[':', ';', '<',
                                                 '=', '>', '?',
                                                 '@', '[', '\\',
                                                 ']', '^', '_',
                                                 '`'])
score_list = tuples(integers(min_value=0), text(alphanum_char))


@given(lists(score_list, min_size=1, max_size=5))
def test_scoreboard(scores):
    """Test pour les fonctions relatives au tableau."""
    scre.init_best_score()
    for (score, name) in scores:
        scre.PLAYER = name
        scre.set_best_score(score)
    read_scores = scre.get_scores()
    scores = list(sorted(scores, key=lambda x: -x[0]))
    assert read_scores == scores

    last_score = scre.get_last_best_score()
    assert last_score == scores[-1][0]

    scre.PLAYER = scores[0][1]
    assert scre.maj(scores[0][0] + 1)
    assert scre.get_scores()[1] == scores[0]
    for _ in range(5):
        scre.maj(10)
    assert not scre.maj(1)
    scre.init_best_score()


@given(lists(text()))
def test_corrupted_board_random(contents):
    """Test de robustesse en cas d'erreur dans le fichier des scores."""
    with open(scre.FILE, 'w') as board:
        for line in contents:
            board.write(line + '\n')
    scre.get_scores()


def test_corrupted_board():
    """Test similaire non randomisé pour assurer la couverture."""
    with open(scre.FILE, 'w') as board:
        for line in ["fsdq", "sdq;0"]:
            board.write(line + '\n')
    assert scre.get_scores() == []
