"""Gestion du score."""
import os
import re
import src.conf as cf
import src.menu as mn
import src.utilities as ut
import src.player as plyr

PLAYER = "Player"
"""Nom par défaut du joueur"""


def onlydigits(value):
    """
    Filtre `value` pour ne garder que les chiffres.

    On peut ainsi retirer toutes les sauts de lignes présents
    dans le fichier `score.txt`.

    Parameters
    ----------
    value : str
        La chaîne à filtrer

    Returns
    -------
    str
        La chaîne obtenue après filtrage
    """
    final_chain = ""
    for i in value:
        if '0' <= i <= '9':
            final_chain += i
    return final_chain


def onlyalphanum(value):
    """
    Filtre `value` pour ne garder que les caractères alphanumériques.

    Parameters
    ----------
    value : str
        La chaîne à filtrer

    Returns
    -------
    str
        La chaîne obtenue après filtrage
    """
    return re.sub(r'[^A-Za-z0-9]+', '', value)


def init_best_score():
    """Initialise le fichier `score.txt`."""
    open(cf.SCORES, "w").close()


def score(pts):
    """
    Afficher le score durant la partie.

    Parameters
    ----------
    pts : int
        Nombre de points du joueur
    """
    font = ut.font(mn.FONT_PIXEL, cf.SCORE_FONT_SIZE)
    font.set_bold(True)
    text = font.render("Score: " + str(pts), True, cf.BLACK)
    cf.DISPLAYSURF.blit(text, (0, 0))


def score_endgame(pts):
    """
    Affiche le score à la fin de la partie.

    Parameters
    ----------
    pts : int
        Nombre de points du joueur
    """
    mn.print_text("Score : " + str(pts), (640, 300), cf.GREY,
                  ut.font(mn.FONT_PIXEL, cf.RESULT_FONT_SIZE), True)


def winner_endgame(player_number):
    """
    Affiche le gagnant à la fin de la partie.

    Parameters
    ----------
    player_number : int
        Numéro du gagnant
    """
    mono = "mono" + plyr.COLORS[player_number]
    img_path = os.path.join(cf.ASSETS, "img", mono, mono + "3.png")
    img = ut.load_image(img_path)
    w, h = img.get_rect().size
    scale_factor = 8
    position = (int(cf.SCREEN_WIDTH / 2 - scale_factor * (w / 2)),
                int(cf.SCREEN_HEIGHT / 2 - scale_factor * (h / 2)))
    mn.print_image(img_path, position, scale_factor)


def get_scores():
    """
    Récupère le score sauvegardé dans le scoreboard.

    Returns
    -------
    (int * str) list
        Une liste contenant un score et un nom de joueur associé
    """
    with open(cf.SCORES) as board:
        try:
            scores = board.readlines()
            if len(scores) < 2:
                return []
            scores[0] = scores[0].split(";")
            scores[1] = scores[1].split(";")
            ordered_list = []
            for duo in range(len(scores[0])):
                if onlydigits(scores[1][duo]) != '':
                    score_value = int(onlydigits(scores[1][duo]))
                    score_name = onlyalphanum(scores[0][duo])
                    element = (score_value, score_name)
                    ordered_list.append(element)
            ordered_list = list(sorted(ordered_list, key=lambda x: -x[0]))
            return ordered_list
        except (ValueError, IndexError):
            board.close()
            init_best_score()
            return []


def get_last_best_score():
    """
    Renvoie le plus petit score du leaderboard.

    Returns
    -------
    int
        Le score recherché
    """
    scores = get_scores()
    if len(scores) == 0:
        return 0
    last = min(scores)
    return last[0]


def set_best_score(value):
    """
    Ajoute un score au leaderboard.

    Parameters
    ----------
    value : int
        Score à ajouter
    """
    scores_board = get_scores()
    with open(cf.SCORES, "w") as board:
        must_be_added = True
        new_scores = ""
        new_players = ""
        if len(scores_board) == 0:
            board.write(PLAYER + "\n" + str(value))
        else:
            for i in range(min(len(scores_board), 4)):
                if must_be_added and scores_board[i][0] < value:
                    new_scores += str(value) + ";"
                    new_players += PLAYER + ";"
                    must_be_added = False
                new_scores += str(scores_board[i][0]) + ";"
                new_players += scores_board[i][1] + ";"
            if must_be_added:
                new_scores += str(value)
                new_players += PLAYER
        board.write(new_players + "\n" + new_scores)


def maj(pts):
    """
    Si le score obtenu est parmi les meilleurs, met à jour le leaderboard.

    Parameters
    ----------
    pts : int
        Le score obtenu

    Returns
    -------
    bool
        `True` si le score a été ajouté, `False` sinon
    """
    minimal_score = get_last_best_score()
    if len(get_scores()) < 5 or minimal_score < pts:
        set_best_score(pts)
        return True
    return False


if not os.path.isfile(cf.SCORES):  # pragma: no cover
    init_best_score()
