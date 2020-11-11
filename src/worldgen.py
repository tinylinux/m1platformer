""" Gère la génération du monde """
import pygame, random
# Import classes
import src.platform as plt
import src.conf as cf
import src.background as bg


def initgen():
    #Lance la création du sol
    
    # on rajoute des bouts de sol, on additionne leur longueur
    # et quand on a couvert tout l'écran on s'arrête.
    longueur_totale=0
    while longueur_totale < cf.SCREEN_WIDTH:
        # On en met un nouveau à la position x = longueur_totale.
        plt.Platform(longueur_totale)
        longueur_totale += cf.SOL_LONG
    #Crée quelques nuages
    for k in range(4) :
        x = random.randint(0,cf.SCREEN_WIDTH)
        y = random.randint(0,cf.SCREEN_HEIGHT//2)
        i = random.randint(0,3)
        bg.Nuage(x,y,i)

def update():
    for nuage in cf.nuages :
        nuage.update()
    for bloc in cf.sol:
        bloc.update()     # On déplace chaque bloc

        
