""" Gère la création et les déplacements des plateformes """
import pygame
import src.conf as cf


class Platform(pygame.sprite.Sprite):
    """ Gère les plateformes """
    def __init__(self, x=1, y=1, haut=3,
                 length=8, image=cf.PLTFRM_IMG, speed = cf.SPEED):
        super().__init__()
        self.haut = haut
        self.length = length
        self.surf = pygame.Surface((length, haut))        # Hit-box
        self.image = pygame.image.load(image)  # Image de la plateforme
        self.image = pygame.transform.scale(self.image, (length, haut))
        self.rect = self.surf.get_rect(topleft=(x, y))
        pygame.sprite.Sprite.__init__(self, cf.sol)
        self.speed = speed
        # Ajoute notre plateforme au groupe "sol".
        # sol.sprites() est la liste des plateformes

    def move(self):
        """ Fait se déplacer la plateforme à la vitesse speed.
        Suprrime la plateforme si celle-ci sort de l'écran"""
        self.rect.move_ip(-self.speed, 0)
        # Défile à la vitesse speed
        # (positive, donc on met un - pour aller à gauche)
        if self.rect.right < 0:     # si on est sorti de l'écran
            self.kill()              # on le supprime


class Sol(Platform):
    def __init__(self, x=1, y=cf.SOL_HAUT, haut=cf.SOL_HAUT, length=cf.SOL_LONG, image=cf.SOL_IMG):
        super().__init__(x=x, y=y, haut=haut, length=length, image=image)
        self.pasencorecree = True

    def move(self):
        super().move()
        if cf.SCREEN_WIDTH - self.length < self.rect.right < cf.SCREEN_WIDTH \
           and self.pasencorecree:
            # si le dernier ne couvre plus tout sur la droite,
            # il faut ajouter un nouveau
            Sol(self.rect.right) # On en met un nouveau juste après
            self.stop_creation()
    def stop_creation(self):
        self.pasencorecree = False

class Batiment(Platform):
    def __init__(self, x=1, y=1, haut=cf.SCREEN_HEIGHT, length=8, image=cf.BAT_IMG, speed=cf.SPEED):
        super().__init__(x=x, y=y, haut=haut, length=length, image=image, speed=speed)