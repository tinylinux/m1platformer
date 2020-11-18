""" Fichier principal du jeu """

import os
import pygame
import sys
pygame.init()
import src.conf as cf  # noqa: E402
import src.worldgen as wrld  # noqa: E402
import src.player as plyr  # noqa: E402
import src.menu as mn  # noqa: E402
import src.score as scre  # noqa: E402

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

FPS = 60
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Platformer")

# Initialisation du monde
wrld.initgen()

# Crée un nouvel event, le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1

# Toutes les secondes on augmente la vitesse
pygame.time.set_timer(INC_SPEED, 1000)

# Initialisation du joueur
P = plyr.Player()

# Compteurs pour le score
seconds = 0
count_frames = 0

# États du jeu :
# 1 : menu de départ
# 2 : jeu en cours
# 3 : menu de fin (scores)
state = 1

while True:  # Boucle du jeu

    for event in pygame.event.get():

        if event.type == INC_SPEED:
            if state == 2:  # Si on est in game
                cf.SPEED += 0.5

        if event.type == pygame.KEYDOWN:
            if state == 2 and event.key == pygame.K_SPACE:  # Saut
                P.jump()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if state == 1 and mn.start_button.click(pygame.mouse.get_pos()):
                # Clic de la souris sur le bouton "Commencer"
                state = 2
                wrld.stop_sol()  # Arrêt de la création du sol du menu

            elif state == 3 and\
                    mn.restart_button.click(pygame.mouse.get_pos()):
                # Clic sur recommencer, on réinitialise le monde
                P = plyr.Player()
                cf.SPEED = cf.INITIAL_SPEED
                seconds = 0
                count_frames = 0
                cf.sol = pygame.sprite.Group()
                cf.nuages = pygame.sprite.Group()
                cf.arbres = pygame.sprite.Group()
                wrld.initgen()
                state = 2
                wrld.stop_sol()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    cf.DISPLAYSURF.fill(cf.BlueSky)  # Fond

    wrld.update()  # Mise à jour de l'environnement

    if state == 1:  # On est dans le menu
        mn.start_button.print(pygame.mouse.get_pos())
        P.move()

    elif state == 2:  # On est en jeu

        # Décompte des secondes
        count_frames += 1
        if count_frames == 60:
            count_frames = 0
            seconds += 1
        scre.score(seconds)

        # Déplacement du joueur
        P.move()

        # Gestion de la mort
        if P.death():
            state = 3
            newhs = scre.maj(seconds)

    elif state == 3:  # Menu de fin

        scre.score_endgame(seconds)
        if newhs:  # Nouveau record
            cf.DISPLAYSURF.blit(pygame.image.load
                                ("assets/img/ui/highscore.png"), (428, 350))
        cf.DISPLAYSURF.blit(pygame.image.load
                            ("assets/img/ui/gameover.png"), (395, 100))
        mn.restart_button.print(pygame.mouse.get_pos())

    pygame.display.flip()
    FramePerSec.tick(FPS)
