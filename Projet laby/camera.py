import pygame

class Camera():
    def __init__(self, largeur, hauteur):
        self.camera = pygame.Rect(largeur, hauteur)
        self.largeur = largeur
        self.hauteur = hauteur
        
    def apply(self, elt):
        return elt.rect.move(self.camera.topleft)
    
    """ def update(self, point):
        x = -point.rect.x + int(WIDTH/2)"""