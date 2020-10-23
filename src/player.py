"""Contient la classe Player, permettant de gérer le personnage."""

import pygame
import src.conf as cf
# Pour créer des vecteurs de dimension 2
vec = pygame.math.Vector2

# Dimensions
WIDTH = 20
HEIGHT = 30
# Position initiale
X_INIT = 100
Y_INIT = 100
# Vitesse initiale
V_0 = 0
# Vitesse initiale lors d'un saut
V_JMP = 100
# Accélération initiale
A_0 = 0
# Accélération due à la gravité
G = 10

class Player(pygame.sprite.Sprite):
    """Gestion du personnage, par les méthodes jump(self) et move(self)."""
    def __init__(self):
        # Initialisation de la classe parent
        #pygame.sprite.Sprite.__init__(self, cf.player_sprite)
        super().__init__()
        # Dimensions et couleur de l'objet
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill([255, 140, 25])
        # Création de l'objet
        self.shape = self.image.get_rect()

        # Position
        self.pos = vec(X_INIT, Y_INIT)
        self.shape.midbottom = self.pos

        # Vitesse
        self.vel = vec(V_0, 0)
        # Accélération
        self.acc = vec(A_0, G)

    def jump(self):
        """Lance le saut du personnage."""
        self.vel.y -= V_JMP

    def move(self):
        """Modifie les vecteurs position, vitesse et accélération si nécessaire."""
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.shape.midbottom = self.pos
