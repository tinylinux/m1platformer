import pygame
import src.conf as cf

BlueSky = (0,210,255)


class Background():
      def __init__(self):
            #self.bg = pygame.image.load('assets/img/fond.jpg')
            self.bg = pygame.Surface([cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT])
            self.bg.fill(BlueSky)
            self.rectbg = self.bg.get_rect()
 
            self.bgX1 = 0
            self.bgY1 = 0
 
            self.bgX2 = self.rectbg.width
            self.bgY2 = 0
         
      def update(self):
            self.bgX1 -= cf.SPEED
            self.bgX2 -= cf.SPEED
            if self.bgX1 <= -self.rectbg.width:
                  self.bgX1 = self.rectbg.width
            if self.bgX2 <= -self.rectbg.width:
                  self.bgX2 = self.rectbg.width
            cf.DISPLAYSURF.blit(self.bg, (self.bgX1, self.bgY1))
            cf.DISPLAYSURF.blit(self.bg, (self.bgX2, self.bgY2))

class cloud():
    def __init__(self,i,bg):
        self.image = pygame.image.load('assets/img/nuages/nuage'+str(i)+'.png')
        self.rect = self.image.get_rect()
        bg.blit(self.image,self.rect)