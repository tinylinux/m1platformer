import os
import pygame
import src.conf as cf

file = "score.txt"

def score(n):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(n), True, (255, 255, 255))
    cf.DISPLAYSURF.blit(text,(0,0))

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
