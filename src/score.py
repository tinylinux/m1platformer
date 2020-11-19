""" Gestion du score """
import os
import pygame
import src.conf as cf
import src.menu as mn

FILE = "score.txt"


def init_best_score():
    """
    Initialiser le fichier score.txt
    """
    with open(FILE, "w") as empty_board:
        empty_board.write("0")


if not os.path.isfile(FILE):
    init_best_score()


def score(pts):
    """
    Afficher le score actuel durant la partie en cours
    """
    font = pygame.font.Font(mn.FONT_PIXEL, 25)
    font.set_bold(True)
    text = font.render("Score: " + str(pts), True, (255, 255, 255))
    cf.DISPLAYSURF.blit(text, (0, 0))


def score_endgame(pts):
    """
    Affiche le score à la fin de la partie
    """
    mn.print_text("Score : " + str(pts), (640, 300), (240, 240, 240),
                  pygame.font.Font(mn.FONT_PIXEL, 50), True)


def get_scores():
    """
    Récuperer le score sauvegardé dans le scoreboard
    """
    with open(FILE) as board:
        try:
            scores = board.readlines()
            if len(scores) < 2:
                return [[], []]
            scores[0].split(";")
            scores[1].split(";")
            scores[1] = map(int, scores[1])
            ordered_val = list(reversed(sorted(scores[1])))
            ordered_i = []
            for i in range(len(scores[0])):
                ordered_i.append(ordered_val.index(scores[1][i]))
            ordered_names = []
            for i in range(len(scores[0])):
                ordered_names.append(scores[0][ordered_i[i]])
            return [ordered_names, ordered_val]
        except ValueError:
            board.close()
            init_best_score()
            return [[], []]


def get_last_best_score():
    """Renvoie le plus petit score du leaderboard"""
    scores = get_scores()
    if len(scores[0]) == 0:
        return 0
    last = min(scores[1])
    return last


def set_best_score(value):
    """
    Met à jour le score dans le fichier défini
    """
    with open(FILE, "w") as board:
        board.write(str(value))


def maj(pts):
    """
    Check si le score obtenu est un High-score
    Si oui, il retourne True et modifie le High-Score
    Si non, il retourne False
    """
    if get_last_best_score() < pts:
        set_best_score(pts)
        return True
    return False
