import pygame, random
import src.conf as cf

class Nuage(cf.GameObject):
    def __init__(self,x,y,i):
        super().__init__(x,y,0.2*random.random()+0.1,cf.nuage_img[i])
        pygame.sprite.Sprite.__init__(self, cf.nuages)
        
    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.pasencorecree:
            i = random.randint(0,cf.n_nuage-1)
            x = random.randint(cf.SCREEN_WIDTH,int(cf.SCREEN_WIDTH*2))
            y = random.randint(0,cf.SCREEN_HEIGHT//2)
            Nuage(x,y,i)
            self.pasencorecree = False    # On en met un nouveau juste après
        
class Arbre(cf.GameObject):
    def __init__(self,x,i):
        img = cf.arbre_img[i]
        w,h = img.get_rect().size
        super().__init__(x,cf.SCREEN_HEIGHT-h,0.6,img)
        pygame.sprite.Sprite.__init__(self, cf.arbres)
        
    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.pasencorecree:
            i = random.randint(0,cf.n_arbre-1)
            x = random.randint(cf.SCREEN_WIDTH,int(cf.SCREEN_WIDTH*2))
            Arbre(x,i)
            self.pasencorecree = False    # On en met un nouveau juste après
