import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))

start = pygame.image.load('images/black.png')
start = pygame.transform.scale(start,(256,128))

font = pygame.font.Font("police/fantasy.ttf", 40)

class Bouton():
    def __init__(self, x, y, image, texte_input):
        self.image = image
        self.image_rect = self.image.get_rect(center=(x, y))
        
        self.texte_input = texte_input
        self.texte = font.render(self.texte_input, True, "white")
        self.texte_rect = self.texte.get_rect(center=(x, y))
        
        
    def afficher(self):
        screen.blit(self.image, self.image_rect)
        screen.blit(self.texte, self.texte_rect)
        
    def click(self, position):
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):
            return True
        
    def hover(self, position):
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):
          self.texte = font.render(self.texte_input, True, "yellow")  
        else : self.texte = font.render(self.texte_input, True, "white")
        

"""  
start_bouton = Bouton(100,200, start,"play")

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_bouton.click(pygame.mouse.get_pos())
            
    screen.fill("white")
    
    start_bouton.afficher()
    start_bouton.hover(pygame.mouse.get_pos())
    
    pygame.display.update()
"""