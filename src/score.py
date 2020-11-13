import os
import pygame
import src.conf as cf
import src.menu as mn

file = "score.txt"

def score(n):
    font = pygame.font.Font(mn.font_pixel, 25)
    font.set_bold(True)
    text = font.render("Score: " + str(n), True, (255, 255, 255))
    cf.DISPLAYSURF.blit(text,(0,0))

def score_endgame(n):
    mn.print_text("Score : " + str(n), (640, 300), (240,240,240), pygame.font.Font(mn.font_pixel, 50), True)

if not os.path.isfile(file):
    with open(file, "w") as f:
        f.write("0")

def get_best_score():
    """
    Récuperer le score sauvegardé dans le scoreboard
    """
    global file
    with open(file) as f:
        return int(f.read().strip().replace("\n", ""))

def set_best_score(value):
    """
    Met à jour le score dans le fichier défini
    """
    global file
    with open(file, "w") as f:
        f.write(str(value))

def maj(score):
    """
    Check si le score obtenu est un High-score
    Si oui, il retourne True et modifie le High-Score
    Si non, il retourne False
    """
    if get_best_score() < score:
        set_best_score(score)
        return True
    return False
