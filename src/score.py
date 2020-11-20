""" Gestion du score """
import os
import re
import pygame
import src.conf as cf
import src.menu as mn

FILE = "score.txt"
PLAYER = "Player"


def onlydigits(value):
    """
    Fonction qui permet de filtrer uniquement les caractères chiffres,
    Cela va permettre de retirer toutes les sauts de lignes présents
    dans le fichier score.txt
    """
    final_chain = ""
    for i in value:
        if '0' <= i <= '9':
            final_chain += i
    return final_chain


def onlyalphanum(value):
    """
    Fonction qui permet de filtrer uniquement les caractères
    alphanumériques (pour le nom du joueur)
    """
    return re.sub(r'[^A-Za-z0-9]+', '', value)


def init_best_score():
    """
    Initialiser le fichier score.txt
    """
    with open(FILE, "w") as empty_board:
        empty_board.write("")


if not os.path.isfile(FILE):
    print('fichier non trouvé')
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
                return []
            scores[0] = scores[0].split(";")
            scores[1] = scores[1].split(";")
            print(scores[0], scores[1])
            ordered_list = []
            for duo in range(len(scores[0])):
                if onlydigits(scores[1][duo]) != '':
                    element = (int(onlydigits(scores[1][duo])), onlyalphanum(scores[0][duo]))
                    ordered_list.append(element)
            ordered_list = list(reversed(sorted(ordered_list)))
            return ordered_list
        except ValueError:
            board.close()
            init_best_score()
            return []


def get_last_best_score():
    """Renvoie le plus petit score du leaderboard"""
    scores = get_scores()
    if len(scores) == 0:
        return 0
    last = min(scores)
    return last[0]


def set_best_score(value):
    """
    Met à jour le score dans le fichier défini
    """
    scores_board = get_scores()
    with open(FILE, "w") as board:
        must_be_added = True
        new_scores = ""
        new_players = ""
        if len(scores_board) == 0:
            board.write(PLAYER + "\n" + str(value))
        else:
            print(scores_board)
            for i in range(len(scores_board)):
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
    Check si le score obtenu est un High-score
    Si oui, il retourne True et modifie le High-Score
    Si non, il retourne False
    """
    minimal_score = get_last_best_score()
    if len(get_scores()) < 5 or minimal_score < pts:
        set_best_score(pts)
        return True
    return False
