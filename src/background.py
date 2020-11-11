import pygame, random
import src.conf as cf

class Nuage(cf.GameObject):
    def __init__(self,x,y,i):
        super().__init__(x,y,0.2,cf.nuage_img[i],cf.SCREEN_WIDTH*0.8)
        pygame.sprite.Sprite.__init__(self, cf.nuages)
        
    def update(self):
        """ Fait se déplacer la plateforme selon la variable SPEED du module conf.
        Suprrime la plateforme si celle-ci sort de l'écran, et demande
        la création d'une nouvelle plateforme si nécessaire"""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH and self.pasencorecree:
            i = random.randint(0,3)
            x = random.randint(cf.SCREEN_WIDTH,int(cf.SCREEN_WIDTH*1.4))
            y = random.randint(0,cf.SCREEN_HEIGHT//2)
            Nuage(x,y,i)
            self.pasencorecree = False    # On en met un nouveau juste après
        
# class building(GameObject):
#     def __init__(self,i,bg):
#         pass


# class Background():
#       def __init__(self):
#             #self.bg = pygame.image.load('assets/img/fond.jpg')
#             self.bg = pygame.Surface([cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT])
#             self.bg.fill(BlueSky)
#             self.rectbg = self.bg.get_rect()
#             cf.DISPLAYSURF.blit(self.bg, (0,0))
 
#             # self.bgX1 = 0
#             # self.bgY1 = 0
 
#             # self.bgX2 = self.rectbg.width
#             # self.bgY2 = 0
         
#       def update(self):
#           cf.DISPLAYSURF.blit(self.bg, (0,0))
#           cf.DISPLAYSURF.fill(BlueSky)
#       #       self.bgX1 -= cf.SPEED
#       #       self.bgX2 -= cf.SPEED
#       #       if self.bgX1 <= -self.rectbg.width:
#       #             self.bgX1 = self.rectbg.width
#       #       if self.bgX2 <= -self.rectbg.width:
#       #             self.bgX2 = self.rectbg.width
#       #       cf.DISPLAYSURF.blit(self.bg, (self.bgX1, self.bgY1))
#       #       cf.DISPLAYSURF.blit(self.bg, (self.bgX2, self.bgY2))
      
      

