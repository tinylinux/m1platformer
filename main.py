""" Fichier principal du jeu """

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# pylint: disable=wrong-import-position
import pygame  # noqa: E402
pygame.init()
import src.conf as cf  # noqa: E402
import src.worldgen as wrld  # noqa: E402
import src.player as plyr  # noqa: E402
import src.menu as mn  # noqa: E402
import src.score as scre  # noqa: E402
# pylint: enable=wrong-import-position

# Initialisation de la fenêtre
cf.DISPLAYSURF = pygame.display.set_mode((cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))

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
SECONDS = 0
FRAMES = 0

# États du jeu :
# 1 : menu de départ
# 2 : jeu en cours
# 3 : menu de fin (scores)
# 4 : affichage des meilleurs scores
STATE = 1

while True:  # Boucle du jeu

    for event in pygame.event.get():

        if event.type == INC_SPEED:
            if STATE == 2:  # Si on est in game
                cf.SPEED += 0.5

        if event.type == pygame.KEYDOWN:
            if STATE == 2 and event.key == pygame.K_SPACE:  # Saut
                P.jump()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if STATE == 1 and mn.start_button.click(pygame.mouse.get_pos()):
                # Clic de la souris sur le bouton "Commencer"
                STATE = 2
                wrld.stop_sol()  # Arrêt de la création du sol du menu

            elif STATE == 1 and mn.records_button.click(pygame.mouse.get_pos()):
                # Clic de la souris sur le bouton "Records"
                STATE = 4

            elif STATE == 3 and mn.return_button.click(pygame.mouse.get_pos()):
                # Clic de la souris sur le bouton "Retour"
                P = plyr.Player()
                cf.SPEED = cf.INITIAL_SPEED
                SECONDS = 0
                FRAMES = 0
                cf.sol = pygame.sprite.Group()
                cf.nuages = pygame.sprite.Group()
                cf.arbres = pygame.sprite.Group()
                wrld.initgen()
                STATE = 1

            elif STATE == 4 and mn.return_button.click(pygame.mouse.get_pos()):
                # Clic de la souris sur le bouton "Records"
                STATE = 1

            elif STATE == 3 and\
                    mn.restart_button.click(pygame.mouse.get_pos()):
                # Clic sur recommencer, on réinitialise le monde
                P = plyr.Player()
                cf.SPEED = cf.INITIAL_SPEED
                SECONDS = 0
                FRAMES = 0
                cf.sol = pygame.sprite.Group()
                cf.nuages = pygame.sprite.Group()
                cf.arbres = pygame.sprite.Group()
                wrld.initgen()
                STATE = 2
                wrld.stop_sol()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    wrld.update()  # Mise à jour de l'environnement

    if STATE == 1:  # On est dans le menu
        cf.DISPLAYSURF.blit(pygame.image.load
                            ("assets/img/ui/title.png"), (357, 132))
        P.move()
        mn.start_button.print(pygame.mouse.get_pos())
        mn.records_button.print(pygame.mouse.get_pos())

    elif STATE == 2:  # On est en jeu

        # Décompte des secondes
        FRAMES += 1
        if FRAMES == 60:
            FRAMES = 0
            SECONDS += 1
        scre.score(SECONDS)

        # Déplacement du joueur
        P.move()

        # Gestion de la mort
        if P.death():
            STATE = 3
            NEWHS = scre.maj(SECONDS)

    elif STATE == 3:  # Menu de fin

        scre.score_endgame(SECONDS)
        if NEWHS:  # Nouveau record
            cf.DISPLAYSURF.blit(pygame.image.load
                                ("assets/img/ui/highscore.png"), (428, 350))
        cf.DISPLAYSURF.blit(pygame.image.load
                            ("assets/img/ui/gameover.png"), (395, 100))
        mn.restart_button.print(pygame.mouse.get_pos())
        mn.return_button.print(pygame.mouse.get_pos())

    elif STATE == 4: # Affichage des meilleurs scores

        # Récupération des meilleurs scores
        records = scre.get_scores()
        number_scores = len(records)
        size_height = 36 * 2 * number_scores
        print(number_scores)
        print(records)
        if number_scores == 0:
            mn.print_text("Pas de scores", (640, 360), (240, 240, 240),
                          pygame.font.Font(mn.FONT_PIXEL, 36), True)
        else:
            for best_score in range(number_scores):
                position_score = 360 - (size_height//2) + best_score*2*36 + 18
                mn.print_text(records[best_score][1] + " : " + str(records[best_score][0]),
                              (640, position_score), (240, 240, 240),
                              pygame.font.Font(mn.FONT_PIXEL, 36), True)
        mn.return_button.print(pygame.mouse.get_pos())

    pygame.display.flip()
    FramePerSec.tick(FPS)
