from pyexpat.errors import XML_ERROR_ABORTED
from webbrowser import get
import generation
import resolution
from bouton import Bouton
import os
import sys
import random
import sauvegarder

import pygame
from pygame import mixer


pygame.init()
sound = False
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
def getRealPath(folderName : str, fileName : str):
    return os.path.join(os.path.join(__location__, folderName), fileName)


#Parametres de base de la fenetre
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Deepsands Labyrinth')
icone = pygame.image.load(getRealPath("images", "maze.png"))
pygame.display.set_icon(icone)


#On charge les elements qui vont servir a faire fonctionner le jeu, son, image et matrice

#Chemin de la police
fantasyFont = getRealPath("police", "fantasy.ttf")

#Police de base
mediumFont = pygame.font.Font(fantasyFont, 60)



tile_size = 30

class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def getPos(self):
        return (self.x, self.y)

    def draw(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.image, (self.x, self.y))

     
def get_coords(matrice, elt):
    """
    Renvoie les coordonnées de la première occurence d'un élement dans une matrice
    """
    for y in range(0, len(matrice)):
        for x in range(0, len(matrice[y])):
            if matrice[y][x] == elt:
                return x, y
                
class Labyrinthe():
    def __init__(self, laby, x, y) -> None:
        self.laby = laby
        self.x = x
        self.y = y
        self.width = tile_size*len(laby[0])
        self.height = len(laby)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def affiche(self, laby : dict, player : Player):
        """
        Fonction affichant dans la fenetre le labyrinthe avec depart et arrivée visible
        """
        taille = tile_size
        
        #Images utilisées
        mur = pygame.image.load(getRealPath("images","mur_I.png"))
        chemin = pygame.image.load(getRealPath("images","dirt16x163.png"))
        arrivee = pygame.image.load(getRealPath("images","finish.png"))
        joueur_img = pygame.image.load(getRealPath("images","running.png"))
        check = pygame.image.load(getRealPath("images","check.png"))

        #On adapte la taille des elements qui servent a afficher
        # mur = pygame.transform.scale(mur, (tile_size,tile_size))
        chemin = pygame.transform.scale(chemin, (tile_size,tile_size))
        arrivee = pygame.transform.scale(arrivee, (tile_size,tile_size))
        joueur_img = pygame.transform.scale(joueur_img, (tile_size,tile_size))
        check = pygame.transform.scale(check, (tile_size,tile_size))
        
        # try:
        #     #On veut placer le joueur au milieu de l'ecran
        #     distance_x, distance_y = get_coords(laby, 3)
        #     #On recupere la distance des bords au milieu de l'ecran, position du joueur
        #     # x_joueur = int(screen.get_width()/2)
        #     # y_joueur = int(screen.get_height()/2)
        #     #On recupere les distances verticales et horizontales du debut du labyrinthe au joueur
        #     distance_x = distance_x * tile_size
        #     distance_y = distance_y * tile_size
        #     #On en deduit le point d'ou doit partir l'affichage si on veut centrer le joueur
        #     depart_x = player.x - distance_x
        #     depart_y = player.y - distance_y
        
        # #Dans le cas ou on veut afficher la solution, il n'existe plus de depart ou d'arrivée dans la matrice
        # except : 
        #     screen.fill((66, 65, 62))
        #     largeur = screen.get_width()
        #     hauteur = screen.get_height()
        #     if largeur > hauteur:
        #         taille = int(largeur/len(laby[0]))

        #     mur = pygame.transform.scale(mur, (taille,taille))
        #     chemin = pygame.transform.scale(chemin, (taille,taille))
        #     check = pygame.transform.scale(check, (taille,taille))

        #     depart_x = 0
        #     depart_y = 0
        
        
        #On parcourt toute la matrice
        depart_x = -player.rect.x
        depart_y = -player.rect.y

        for ligne in range(len(laby)):
            for colonne in range(len(laby[0])):
                #On determine la position de l'element sur l'ecran
                # if depart_x < 0 :
                #     x = colonne * taille + depart_x
                # else : x = colonne * taille


                # if depart_y >= 0 : 
                #     y = ligne * taille 
                # else : y = ligne * taille + depart_y
                x=taille*colonne+self.x
                y=taille*ligne+self.y

                #En fonction de la nature de l'element on lui attribue une image
                if laby[ligne][colonne] == 1:   #Mur
                    image = assignTexture(laby, ligne, colonne)
                    screen.blit(image, (x, y))#pygame.transform.scale(pygame.transform.rotate(mur, random.randint(0,1)*180), (taille,taille)),(x, y))

                elif laby[ligne][colonne] == 2:  #Arrivée
                    screen.blit(arrivee, (x, y))

                # elif laby[ligne][colonne] == 3:   #Joueur
                    # player.draw(x, y)

                elif laby[ligne][colonne] == 5:   #Plus court chemin
                    screen.blit(check, (x, y))

                else:
                    screen.blit(chemin, (x, y))

def is_won(laby, x, y):
    if laby[y][x] == 2:
        return True
    return False


def update_matrice(direction, maze):
    #Est inutile actuellement
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

def game():
    """
    Fonction lancant la boucle de jeu
    """
    #Message de chargement le temps de generer le labyrinthe
    screen.fill("black")

    title_font = pygame.font.Font(fantasyFont, 125)
    title = title_font.render("Deepsands Labyrinth", True, (173, 129, 9))
    title_rect = title.get_rect(center = (540, 150))

    loading_message = mediumFont.render("Loading...", True, "White")
    loading_message_rect = loading_message.get_rect(center=(540, 380))

    screen.blit(loading_message, loading_message_rect)
    screen.blit(title, title_rect)
    pygame.display.update()

    # On check l'existence de la save
    sauvegarder.verif_sauvegarde()
    # On initialise le temps de départ
    temps_debut = time.time()
    
    data = sauvegarder.charger_sauvegarde()
    niveau = data["general"][1]
    #Creation du labyrinthe
    maze = generation.to_laby(generation.creer(50+int(5*niveau-15),30+int(5*niveau-15)))
    #On prend les valeurs d'indice du joueur dans la matrice
    
    print(get_coords(maze, 3))
    print(get_coords(maze, 3)[0]*tile_size, get_coords(maze, 3)[1]*tile_size)
    #Instanciation du joueur
    joueur_img = pygame.transform.scale(pygame.image.load(getRealPath("images", "button.png")), (25, 25))
    player = Player(joueur_img, 0, 0)
    lab = Labyrinthe(maze, screen.get_width()/2-get_coords(maze, 3)[0]*tile_size, screen.get_height()/2-get_coords(maze, 3)[1]*tile_size)
    x, y = screen.get_width()/2, screen.get_height()/2
    fog = pygame.image.load(getRealPath("images", "fog.png"))

    #On affiche le labyrinthe a l'ecran
    #TODO Déplacer/Supprimer, ça ne sert à rien d'afficher avant la boucle
    screen.fill((66, 65, 62))
    lab.affiche(maze, player)
    screen.blit(joueur_img, (x, y))
    pygame.display.update()

    #Chargement et lancement de la musique
    if sound:
        mixer.music.load('v0.wav')
        mixer.music.play(-1)


    #Création de l'évènement qui revient au menu une fois la solution affichée au bout de 5 secondes
    RETURNEVENT = pygame.USEREVENT
    speed = 8

    running = True
    while running:  #Boucle infinie tant que le programme tourne
        #On recupere en permanence les touches actionnées
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            #Si on quitte la fenetre on met fin a la boucle
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    soluce(maze)
                    lab.affiche(maze, player)
                    pygame.display.update()
                    #Ici on programme l'évènement RETURNEVENT pour dans 5 secondes,
                    #et on commence une boucle qui permet juste de garder les fonctionnalités des touches
                    #echap, bouton croix, et on vérifie l'évènement RETURNEVENT pour que dès que les 5 secondes sont écoulées, on revient au menu principal
                    pygame.time.set_timer(RETURNEVENT, 5000, True)
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == RETURNEVENT:
                                waiting = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    waiting = False
                    running = False 
                    start()
                    
        key = pygame.key.get_pressed()
        haut = key[pygame.K_z] or key[pygame.K_UP]
        bas = key[pygame.K_s] or key[pygame.K_DOWN]
        gauche = key[pygame.K_q] or key[pygame.K_LEFT]
        droite = key[pygame.K_d] or key[pygame.K_RIGHT]
        
        
        
        # if is_won(maze, pos_to_coord(player, lab)[0], pos_to_coord(player, lab)[1]):
            # intermission()
        vec = pygame.math.Vector2(droite - gauche, bas - haut)
        if vec.length_squared() > 0:
            vec.scale_to_length(speed)
            
            # if player.x < screen.get_width()/2 and player.x > screen.get_width()/2 and focus == False:
            #     focus = True
            # else:
            #     focus = False
            
            # if player.y < screen.get_height()/2 and player.y > screen.get_height()/2 and focus == False:
            #     focus = True
            # else : focus = False
            if maze[pos_to_coord(x,y,lab)[1]][pos_to_coord(x,y,lab)[0]+1] == 1:
                if vec.x > 0:
                    vec.x = 0
                else:
                    vec.x = vec.x
            if maze[pos_to_coord(x,y,lab)[1]][pos_to_coord(x,y,lab)[0]] == 1:
                if vec.x < 0:
                    vec.x = 0
                else:
                    vec.x = vec.x
            if maze[pos_to_coord(x,y,lab)[1]+1][pos_to_coord(x,y,lab)[0]] == 1:
                if vec.y > 0:
                    vec.y = 0
                else:
                    vec.y = vec.y
            if maze[pos_to_coord(x,y,lab)[1]][pos_to_coord(x,y,lab)[0]] == 1:
                if vec.y < 0:
                    vec.y = 0
                else:
                    vec.y = vec.y
            else:
                vec.x = vec.x
            lab.rect.move_ip(-round(vec.x), -round(vec.y))
            lab.move(lab.rect.x, lab.rect.y)
        # print(coord_to_pos(pos_to_coord(x,y,lab)[0], pos_to_coord(x,y,lab)[1], x, y, lab), x, y)
        screen.fill((66, 65, 62))
        lab.affiche(maze, player)
        screen.blit(joueur_img, (x, y))
        screen.blit(fog, (0, 0))
        
        #pygame.time.wait(100) #On attend un peu avant de continuer
        pygame.display.update()
        pygame.time.wait(16) #Limite d'IPS

def start():
    #Chargement et lancement de la musique
    if sound:
        mixer.music.load('options.wav')
        mixer.music.play(-1)
     
    screen.fill("black")
     
    title_font = pygame.font.Font(fantasyFont, 125) 
    title = title_font.render("Deepsands Labyrinth", True, (173, 129, 9))
    title_rect = title.get_rect(center = (540, 150))
     
    fond_bouton = pygame.image.load(getRealPath("images", "black.png"))
    fond_bouton = pygame.transform.scale(fond_bouton, (200,50))
     
    bouton_start = Bouton(540,430, fond_bouton, "Start a game")
     
    bouton_stats = Bouton(540, 500, fond_bouton, "Stats")
     
    bouton_options = Bouton(540, 570, fond_bouton, "Options")
     
    bouton_credits = Bouton(1010,690, fond_bouton, "Credits")
     
    bouton_quit = Bouton(120, 690, fond_bouton, "Quit to Desktop")
     
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_start.click(pygame.mouse.get_pos()):
                    running = False
                    game()

                if bouton_quit.click(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

                if bouton_credits.click(pygame.mouse.get_pos()):
                    credits()


        screen.fill("black")

        bouton_start.afficher()
        bouton_start.hover(pygame.mouse.get_pos())

        bouton_stats.afficher()
        bouton_stats.hover(pygame.mouse.get_pos())

        bouton_options.afficher()
        bouton_options.hover(pygame.mouse.get_pos())

        bouton_credits.afficher()
        bouton_credits.hover(pygame.mouse.get_pos())

        bouton_quit.afficher()
        bouton_quit.hover(pygame.mouse.get_pos())

        screen.blit(title, title_rect)

        pygame.display.update()
        
def soluce(laby):
    path = resolution.solution(laby, (get_coords(laby, 3)), (get_coords(laby, 2)))
    for i in path:
        x = i[0]
        y = i[1]
        laby[y][x] = 5 
    return laby         

def credits():
    coding = mediumFont.render("Coding", True, (173, 129, 9))
    coding_rect = coding.get_rect(center=(540, 150))

    loup = mediumFont.render("Loup Devernay", True, "white")
    loup_rect = loup.get_rect(center=(540,220))

    zach = mediumFont.render("Zacharie Girard", True, "white")
    zach_rect = zach.get_rect(center = (540,280))
    
    paul = mediumFont.render("Paul Musial", True, "white")
    paul_rect = paul.get_rect(center = (540,340))

    music = mediumFont.render("Soundtrack", True, (173, 129, 9))
    music_rect = music.get_rect(center=(540,490))

    zac = mediumFont.render("Zacharie Girard", True, "white")
    zac_rect =zac.get_rect(center = (540,560))


    fond_bouton = pygame.image.load(getRealPath("images", "black.png"))
    fond_bouton = pygame.transform.scale(fond_bouton, (200,50))

    bouton_quit = Bouton(1030,690, fond_bouton, "Back")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quit.click(pygame.mouse.get_pos()):
                    running = False

        screen.fill("black")
        screen.blit(coding,coding_rect)
        screen.blit(loup,loup_rect)
        screen.blit(zach,zach_rect)
        screen.blit(paul,paul_rect)
        screen.blit(music,music_rect)
        screen.blit(zac,zac_rect)

        bouton_quit.afficher()
        bouton_quit.hover(pygame.mouse.get_pos())
     
        pygame.display.update()

def intermission():
    #Chargement et lancement de la musique
    if sound:
        mixer.music.load('options.wav')
        mixer.music.play(-1)
     
    screen.fill("black")
     
    fond = pygame.image.load('images/black.png')
    fond = pygame.transform.scale(fond, (150,70))
     
    start_bouton = Bouton(540,430, fond, "Continue")
     
    gg = mediumFont.render("Well Done", True, "White")
    gg_rect = gg.get_rect(center=(540, 350))
     
    quit_bouton = Bouton(540, 500, fond, "Quit to main menu")
     
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_bouton.click(pygame.mouse.get_pos()):
                    running = False
                    game()

                if quit_bouton.click(pygame.mouse.get_pos()):
                    running = False
                    start()

        screen.fill("black")

        start_bouton.afficher()
        start_bouton.hover(pygame.mouse.get_pos())

        quit_bouton.afficher()
        quit_bouton.hover(pygame.mouse.get_pos())

        screen.blit(gg, gg_rect)

        pygame.display.update()

def move(player : Player, direction : str, directionOpt : str = ""):
    # On commence par bouger le labyrinthe
    # Ensuite le joueur
    if direction == "up":
        player.draw(player.getPos()[0],player.getPos()[1]-1)
    
    elif direction == "down":
        player.draw(player.getPos()[0],player.getPos()[1]+1)
    
    elif direction == "left":
        player.draw(player.getPos()[0]-1,player.getPos()[1])
    
    elif direction == "right":
        player.draw(player.getPos()[0]+1,player.getPos()[1])

    elif direction == "down" and directionOpt == "right":
        player.draw(player.getPos()[0]+15,player.getPos()[1]+15)

def assignTexture(laby: dict, ligne: int, colonne: int):
    #Mur droit
    if ligne>0 and colonne>0 and ligne<len(laby)-1 and colonne<len(laby[ligne])-1:
        if laby[ligne][colonne+1] == 1 and laby[ligne][colonne-1] == 1 and laby[ligne-1][colonne] == 1 and laby[ligne+1][colonne] == 1: # ╬
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "button.png")), 0)
        elif laby[ligne][colonne+1] == 1 and laby[ligne][colonne-1] == 1 and laby[ligne+1][colonne] == 1: # ╦
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 270)
        elif laby[ligne][colonne+1] == 1 and laby[ligne][colonne-1] == 1 and laby[ligne-1][colonne] == 1: # ╩
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 90)
        elif laby[ligne+1][colonne] == 1 and laby[ligne-1][colonne] == 1 and laby[ligne][colonne+1] == 1: # ╠
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 0)
        elif laby[ligne+1][colonne+1] == 1 and laby[ligne-1][colonne] == 1 and laby[ligne][colonne-1] == 1: # ╣
            image =pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 180)
        elif laby[ligne-1][colonne] == 1 and laby[ligne][colonne+1] == 1: # ╚
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 0)
        elif laby[ligne+1][colonne] == 1 and laby[ligne][colonne+1] == 1: # ╔
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 270)
        elif laby[ligne+1][colonne] == 1 and laby[ligne][colonne-1] == 1: # ╗
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 180)
        elif laby[ligne-1][colonne] == 1 and laby[ligne][colonne-1] == 1: # ╝
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 90)
        elif laby[ligne+1][colonne] == 1 and laby[ligne-1][colonne] == 1: # ║
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_I.png")), 0)
        elif laby[ligne][colonne+1] == 1 and laby[ligne][colonne-1] == 1: # ═
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_I.png")), 90)
        elif laby[ligne-1][colonne] == 1: # └─┘
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_U.png")), 0)
        elif laby[ligne+1][colonne] == 1: # ┌─┐
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_U.png")), 180)
        elif laby[ligne][colonne-1] == 1: # >
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_U.png")), 90)
        elif laby[ligne][colonne+1] == 1: # <
            image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_U.png")), 270)
        else:
            image = pygame.image.load(getRealPath("images", "mur_O.png"))
    else:
        if colonne == 0:
            if laby[ligne][colonne+1]==1 and ligne > 0 and ligne+1 < len(laby): # ╠
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 0)
            elif ligne+1 < len(laby) and ligne > 0: # ║
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_I.png")), 0)
            elif laby[ligne][colonne+1]==1 and ligne == 0: #Coin supérieur gauche
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 270)
            elif laby[ligne][colonne+1]==1 and ligne == len(laby)-1: #Coin inférieur gauche
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 0)
        elif colonne == len(laby[0])-1:
            if laby[ligne][colonne-1]==1 and ligne > 0 and ligne+1 < len(laby): # ╠
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 180)
            elif ligne+1 < len(laby) and ligne > 0: # ║
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_I.png")), 0)
            elif laby[ligne][colonne-1]==1 and ligne == 0: #Coin supérieur droit
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 180)
            elif laby[ligne][colonne-1]==1 and ligne == len(laby)-1: #Coin inférieur droit
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_L.png")), 90)
        elif ligne == 0:
            if laby[ligne+1][colonne]==1 and colonne < len(laby[0])-1: # ╦
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 270)
            elif colonne+1 < len(laby[0]) and colonne > 0: # ═
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_I.png")), 90)
        else:
            if laby[ligne-1][colonne]==1 and colonne < len(laby)-1: # ╦
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_T.png")), 90)
            elif colonne-1 < len(laby[0]) and colonne > 0: # ═
                image = pygame.transform.rotate(pygame.image.load(getRealPath("images", "mur_I.png")), 90)
    return pygame.transform.scale(image, (tile_size, tile_size))


def pos_to_coord(x, y, laby): #laby : classe labyrinthe
    x_laby = laby.x
    y_laby = laby.y

    x_coord = int(abs(-x_laby + x) / tile_size)
    y_coord = int(abs(-y_laby + y) / tile_size)

    return x_coord, y_coord
def coord_to_pos(x_coord, y_coord,x, y, laby): #laby : classe labyrinthe

    x_laby= -(x_coord*tile_size - x)
    y_laby= -(y_coord*tile_size - y)

    return x_laby, y_laby
    
start()
