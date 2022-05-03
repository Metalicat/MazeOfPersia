import generation
import resolution
from bouton import Bouton

import pygame
from pygame import RESIZABLE, mixer

pygame.init()

#Parametres de base de la fenetre
screen = pygame.display.set_mode((1080, 720), RESIZABLE)
pygame.display.set_caption('Deepsands Labyrinth')
icone = pygame.image.load('images/maze.png')
pygame.display.set_icon(icone)


#On charge les elements qui vont servir a faire fonctionner le jeu, son, image et matrice

#Police de base
font = pygame.font.Font("police/fantasy.ttf", 60)

#Images utilisés
mur = pygame.image.load('images/black.png')
chemin = pygame.image.load('images/white.png')
arrivee = pygame.image.load('images/finish.png')
joueur_img = pygame.image.load('images/running.png')
check = pygame.image.load('images/check.png')

tile_size = 16

#On adapte la taille
mur = pygame.transform.scale(mur, (tile_size,tile_size))
chemin = pygame.transform.scale(chemin, (tile_size,tile_size))
arrivee = pygame.transform.scale(arrivee, (tile_size,tile_size))
joueur_img = pygame.transform.scale(joueur_img, (tile_size,tile_size))
check = pygame.transform.scale(check, (tile_size,tile_size))


def joueur(x, y):
  """
  Fonction permettant d'afficher le joueur a une position passée en parametre
  """
  screen.blit(joueur_img, (x, y))
  
def get_coords(matrice, elt):
  """
  Fonction renvoyant les coordonnées d'un element dans une matrice
  """
  for y in range(0, len(matrice)):
    for x in range(0, len(matrice[y])):
      if matrice[y][x] == elt:
        return x, y
  
def affichage(laby):
  """
  Fonction affichant dans la fenetre le labyrinthe avec depart et arrivée visible
  """
  taille = tile_size
  get_coords(laby, 3)
  #On place le joueur au milieu de l'ecran
  x_joueur = screen.get_width/2
  y_joueur = screen.get_height/2
  
  #On parcourt toute la matrice
  for ligne in range(len(laby)):
    for colonne in range(len(laby[0])):
      #On determine la position de l'element sur l'ecran
      x = colonne * taille
      y = ligne * taille
      #En fonction de la nature de l'element on lui attribue une image
      if laby[ligne][colonne] == 1:   #Mur
        screen.blit(mur,(x, y))
        
      elif laby[ligne][colonne] == 2:  #Arrivée
        screen.blit(arrivee, (x, y))
        
      elif laby[ligne][colonne] == 3:   #Joueur
        joueur(x, y)
      
      elif laby[ligne][colonne] == 5:   #Plus court chemin
        screen.blit(check, (x, y))
        
      else: screen.blit(chemin, (x, y))

def move(direction, maze):
  """
  Fonction qui permet de faire deplacer le joueur dans la matrice selon une direction donnée
  """
  #On recupere les coordonées actuelles du joueur
  x_joueur, y_joueur = get_coords(maze, 3)
  #L'operation varie en fonction de la direction mais le principe reste le meme
  if direction == 'left':
    #On verifie que la case demandée est un chemin
    if maze[y_joueur][x_joueur-1] == 0:
      #Dans ce cas on echange les elements dans la matrice afin d'actualiser
      maze[y_joueur][x_joueur-1], maze[y_joueur][x_joueur] = maze[y_joueur][x_joueur], maze[y_joueur][x_joueur-1]
    #Si jamais l'element qu'on cherche a atteindre est l'arrivée on renvoie GG, retour reutilisable par main_game() 
    elif maze[y_joueur][x_joueur-1] == 2:
      return "GG"
  
  #Meme fonctionnement pour les autres directions  
  elif direction == 'right':
    if maze[y_joueur][x_joueur+1] == 0:
      maze[y_joueur][x_joueur+1], maze[y_joueur][x_joueur] = maze[y_joueur][x_joueur], maze[y_joueur][x_joueur+1]
    elif maze[y_joueur][x_joueur+1] == 2:
      return "GG"
      
  elif direction == 'up':
    if maze[y_joueur-1][x_joueur] == 0:
      maze[y_joueur-1][x_joueur], maze[y_joueur][x_joueur] = maze[y_joueur][x_joueur], maze[y_joueur-1][x_joueur]
    elif maze[y_joueur-1][x_joueur] == 2:
      return "GG"
      
  elif direction == 'down':
    if maze[y_joueur+1][x_joueur] == 0:
      maze[y_joueur+1][x_joueur], maze[y_joueur][x_joueur] = maze[y_joueur][x_joueur], maze[y_joueur+1][x_joueur]
    elif maze[y_joueur+1][x_joueur] == 2:
      return "GG"

def main_game():
  """
  Fonction lancant la boucle de jeu
  """
  
  #Message de chargement le temps de generer le labyrinthe
  screen.fill("black")
  
  title_font = pygame.font.Font("police/fantasy.ttf", 125)
  main_title = title_font.render("Deepsands Labyrinth", True, "White")
  title_rect = main_title.get_rect(center = (540, 150))
  
  msg = font.render("Loading...", True, "White")
  msg_rect = msg.get_rect(center=(540, 380))
  
  screen.blit(msg, msg_rect)
  screen.blit(main_title, title_rect)
  pygame.display.update()
  
  
  #Creation du labyrinthe
  maze = generation.to_laby(generation.creer(200,45))
  
  #On affiche le labyrinthe a l'ecran
  screen.fill("white")
  affichage(maze)
  pygame.display.update()
  
  #Chargement et lancement de la musique
  mixer.music.load('v0.wav')
  mixer.music.play(-1)

  running = True
  #Boucle infinie tant que le programme tourne
  while running:  
    #On recupere en permanence les touches actionnées
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
      #Si on quitte la fenetre on met fin a la boucle
      if event.type == pygame.QUIT:
        running = False
        
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          soluce(maze)
          affichage(maze)
          pygame.display.update()
          pygame.time.wait(5000)
          running = False
          main_menu()  
    
    #Si dans le tableau keys on trouve une des commandes directionnelles on appelle la fonction move pour la direction correspondante    
    if keys[pygame.K_z]:
      #Si la fonction renvoie GG on considère qu'on a terminé le labyrinthe
      #La fonction de jeu s'arrete et on appelle intermission() qui permet de quitter ou de lancer une nouvelle partie
      if move('up', maze) == "GG":
        running = False
        intermission()
      affichage(maze)       #On modifie la matrice contenant le labyrinthe 
      pygame.display.update()  #On actualise ensuite la fenetre

    #Idem pour les 3 autres directions
    elif keys[pygame.K_s]:
      if move('down', maze) == "GG":
        running = False
        intermission()
      affichage(maze)
      pygame.display.update()
            
    elif keys[pygame.K_q]:
      if move('left', maze) == "GG":
        running = False
        intermission()
      affichage(maze)
      pygame.display.update()
              
    elif keys[pygame.K_d]:
      if move('right', maze) == "GG":
        running = False
        intermission()
      affichage(maze)
      pygame.display.update()
      
    pygame.time.wait(100) #On attend un peu avant de continuer
    
def main_menu():
  #Chargement et lancement de la musique
  mixer.music.load('options.wav')
  mixer.music.play(-1)
  
  screen.fill("black")
  
  title_font = pygame.font.Font("police/fantasy.ttf", 125) 
  main_title = title_font.render("Deepsands Labyrinth", True, "White")
  title_rect = main_title.get_rect(center = (540, 150))
  
  start = pygame.image.load('images/black.png')
  start = pygame.transform.scale(start, (200,50))
  
  start_bouton = Bouton(540,430, start, "Start a game")
  
  stats_bouton = Bouton(540, 500, start, "Stats")
  
  options_bouton = Bouton(540, 570, start, "Options")
  
  credits_bouton = Bouton(1010,690, start, "Credits")
  
  quit_bouton = Bouton(120, 690, start, "Quit to Desktop")
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        if start_bouton.click(pygame.mouse.get_pos()):
          running = False
          main_game()
        
        if quit_bouton.click(pygame.mouse.get_pos()):
          running = False
          
        if credits_bouton.click(pygame.mouse.get_pos()):
          running = False
          credits()
          
            
    screen.fill("black")
    
    start_bouton.afficher()
    start_bouton.hover(pygame.mouse.get_pos())
    
    stats_bouton.afficher()
    stats_bouton.hover(pygame.mouse.get_pos())
    
    options_bouton.afficher()
    options_bouton.hover(pygame.mouse.get_pos())
    
    credits_bouton.afficher()
    credits_bouton.hover(pygame.mouse.get_pos())
    
    quit_bouton.afficher()
    quit_bouton.hover(pygame.mouse.get_pos())
    
    screen.blit(main_title, title_rect)
    
    pygame.display.update()

def intermission():
  #Chargement et lancement de la musique
  mixer.music.load('options.wav')
  mixer.music.play(-1)
  
  screen.fill("black")
  
  fond = pygame.image.load('images/black.png')
  fond = pygame.transform.scale(fond, (150,70))
  
  start_bouton = Bouton(540,430, fond, "Continue")
  
  gg = font.render("Well Done", True, "White")
  gg_rect = gg.get_rect(center=(540, 350))
  
  quit_bouton = Bouton(540, 500, fond, "Quit to main menu")
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        if start_bouton.click(pygame.mouse.get_pos()):
          running = False
          main_game()
        
        if quit_bouton.click(pygame.mouse.get_pos()):
          running = False
          main_menu()
            
    screen.fill("black")
    
    start_bouton.afficher()
    start_bouton.hover(pygame.mouse.get_pos())
    
    quit_bouton.afficher()
    quit_bouton.hover(pygame.mouse.get_pos())
    
    screen.blit(gg, gg_rect)
    
    pygame.display.update()

def soluce(laby):
  path = resolution.solution(laby, (get_coords(laby, 3)), (get_coords(laby, 2)))
  for i in path:
    x = i[0]
    y = i[1]
    laby[y][x] = 5 
  return laby         

def credits():
  screen.fill("black")
  
  coding = font.render("Coding", True, (173, 129, 9))
  coding_rect = coding.get_rect(center=(540, 150))

  loup = font.render("Loup Devernay", True, "white")
  loup_rect = loup.get_rect(center=(540,220))
  
  zach = font.render("Zacharie Girard", True, "white")
  zach_rect = zach.get_rect(center = (540,280))
  
  music = font.render("Soundtrack", True, (173, 129, 9))
  music_rect = music.get_rect(center=(540,450))
  
  zac = font.render("Zacharie Girard", True, "white")
  zac_rect =zac.get_rect(center = (540,520))
  
  
  start = pygame.image.load('images/black.png')
  start = pygame.transform.scale(start, (200,50))
  
  quit = Bouton(1030,690, start, "Back")
  
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        if quit.click(pygame.mouse.get_pos()):
          running = False
          main_menu()
      
      
    screen.blit(coding,coding_rect)
    screen.blit(loup,loup_rect)
    screen.blit(zach,zach_rect)
    screen.blit(music,music_rect)
    screen.blit(zac,zac_rect)
    
    quit.afficher()
    quit.hover(pygame.mouse.get_pos())
  
    pygame.display.update()
  
main_menu()