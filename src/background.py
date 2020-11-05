import pygame
import src.conf as cf


class Background():
      def __init__(self):
            self.bg = pygame.image.load('assets/img/fond.jpg')
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
