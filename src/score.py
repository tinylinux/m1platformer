""" Gestion du score """
import os
import pygame
import src.conf as cf
import src.menu as mn

FILE = "score.txt"

if not os.path.isfile(FILE):
    with open(FILE, "w") as empty_board:
        empty_board.write("0")


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


def get_best_score():
    """
    Récuperer le score sauvegardé dans le scoreboard
    """
    with open(FILE) as board:
        return int(board.read().strip().replace("\n", ""))


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
    if get_best_score() < pts:
        set_best_score(pts)
        return True
    return False
