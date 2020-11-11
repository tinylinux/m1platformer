""" Gère la création et les déplacements des plateformes """
import pygame
import src.conf as cf

class Platform(cf.GameObject):
    def __init__(self,x):
        #self.surf = pygame.Surface((cf.SOL_LONG, cf.SOL_HAUT))        # Hit-box
        super().__init__(x,cf.SOL_HAUT,1,cf.SOL_IMG,cf.SCREEN_WIDTH)
        pygame.sprite.Sprite.__init__(self, cf.sol)
        
        
    def update(self):
        """ Fait se déplacer la plateforme selon la variable SPEED du module conf.
        Suprrime la plateforme si celle-ci sort de l'écran, et demande
        la création d'une nouvelle plateforme si nécessaire"""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH and self.pasencorecree:
            # si le dernier ne couvre plus tout sur la droite,
            # il faut ajouter un nouveau
            Platform(self.rect.right)
            self.pasencorecree = False    # On en met un nouveau juste après
        
        
        
        
        

# class Platform(pygame.sprite.Sprite):
#     """ Gère les plateformes """
#     def __init__(self, x=1, y=cf.SOL_HAUT, haut=cf.SOL_HAUT,
#                  length=cf.SOL_LONG, image=cf.SOL_IMG):
#         super().__init__()
#         self.haut = haut
#         self.length = length
#         self.image = pygame.image.load(image)  # Image de la plateforme
#         self.surf = pygame.Surface((length, haut))        # Hit-box
#         self.rect = self.surf.get_rect(topleft=(x, y))
#         pygame.sprite.Sprite.__init__(self, cf.sol)
#         # Ajoute notre plateforme au groupe "sol".
#         # sol.sprites() est la liste des plateformes
#         self.pasencorecree = True

#     def move(self):
#         """ Fait se déplacer la plateforme selon la variable SPEED du module conf.
#         Suprrime la plateforme si celle-ci sort de l'écran, et demande
#         la création d'une nouvelle plateforme si nécessaire"""
#         self.rect.move_ip(-cf.SPEED, 0)
#         # Défile à la vitesse SPEED
#         # (positive, donc on met un - pour aller à gauche)
#         if self.rect.right < 0:     # si on est sorti de l'écran
#             self.kill()              # on le supprime
#         if cf.SCREEN_WIDTH - cf.SOL_LONG < self.rect.right < cf.SCREEN_WIDTH \
#            and self.pasencorecree:
#             # si le dernier ne couvre plus tout sur la droite,
#             # il faut ajouter un nouveau
#             Platform(self.rect.right)
#             self.pasencorecree = False    # On en met un nouveau juste après
