import random
import resolution

def afficher(mat):
  """
  Fonction permettant d'afficher proprement une matrice
  """
  for i in range(len(mat)):
      for j in range(len(mat[i])):
          print( str(mat[i][j]),end=' ')
      print()      

def base(x,y):
    """
    Fonction renvoyant une matrice de dimensions x et y composée de 1 sur les contours et de 0 a l'interieur
    Permet de poser un cadre infranchissable pour le labyrinthe
    """
    matrice = []
    for ligne in range(y):
        matrice.append([])
        for colonne in range(x):
            if ligne == 0 or ligne == y-1 or colonne == 0 or colonne == x-1:
                matrice[ligne].append("X")
            else : matrice[ligne].append(".")
    return matrice

def generation(matrice, x_debut, y_debut, x_fin, y_fin):
    """
    Fonction récursive permettant a partir d'une matrice de 0 de générer un labyrinthe 
    #TODO : args
    """     
    
    distance_x = x_fin - x_debut
    distance_y = y_fin - y_debut
    if distance_x > 1 and distance_y > 1: 
        if distance_x > distance_y:       #Coupe verticale
            if distance_x > 2:              #On verifie qu'on a assez de p^lace pour couper
                x_coupe = random.randint(x_debut + 1, x_fin - 1) #On choisit l'emplacement du mur
                ouverture = random.randint(y_debut, y_fin)      #On choisit l'endroit de de l'ouverture dans le mur
                for ligne in range(y_debut, y_fin):   #On crée le mur
                    if ligne == ouverture:      #Si on tombe sur l indice de l'ouverture on cree une ouverture et on donne le meme statut au cases adjacentes (droite/gauche)
                        matrice[ligne][x_coupe] = "," 
                        if x_coupe + 1 < x_fin :
                            matrice[ligne][x_coupe + 1] = ","
                        if x_coupe - 1 > x_debut:
                            matrice[ligne][x_coupe - 1] = ","
                    
                    else :      
                        if matrice[ligne][x_coupe] != "," :      #Si la case n'est pas une ouverture On place un mur
                            matrice[ligne][x_coupe] = "X"  
                generation(matrice, x_debut, y_debut, x_coupe - 1, y_fin) #On rappelle la fonction a droite et a gauche
                generation(matrice, x_coupe + 1, y_debut, x_fin, y_fin)
            return matrice
                
        elif distance_x < distance_y:     #Coupe horizontale
            if distance_y > 2:
                y_coupe = random.randint(y_debut + 1, y_fin - 1)
                ouverture = random.randint(x_debut, x_fin)
                for colonne in range(x_debut, x_fin):
                    if colonne == ouverture:
                        matrice[y_coupe][colonne] = ","
                        if y_coupe - 1 > y_debut :
                            matrice[y_coupe - 1][colonne] = ","
                        if y_coupe + 1 < y_fin :
                            matrice[y_coupe + 1][colonne] = ","
                    
                    else :
                        if matrice[y_coupe][colonne] != ",":
                            matrice[y_coupe][colonne] = "X"
                generation(matrice, x_debut, y_debut, x_fin, y_coupe - 1)
                generation(matrice, x_debut, y_coupe + 1, x_fin, y_fin)
            return matrice
        
        else : 
            rand = random.randint(0,1)
            
            if rand == 0: #Coupe verticale
                if distance_x > 2:
                    x_coupe = random.randint(x_debut + 1, x_fin - 1)
                    ouverture = random.randint(y_debut, y_fin)
                    for ligne in range(y_debut, y_fin):
                        if ligne == ouverture:
                            matrice[ligne][x_coupe] = "," 
                            if x_coupe + 1 < x_fin :
                                matrice[ligne][x_coupe + 1] = ","
                            if x_coupe - 1 > x_debut:
                                matrice[ligne][x_coupe - 1] = ","

                        else : 
                            if matrice[ligne][x_coupe] != ",":
                                matrice[ligne][x_coupe] = "X"  
                    generation(matrice, x_debut, y_debut, x_coupe - 1, y_fin) 
                    generation(matrice, x_coupe + 1, y_debut, x_fin, y_fin) 
                return matrice
            
            else : #Coupe horizontale    
                if distance_y > 2:
                    y_coupe = random.randint(y_debut + 1, y_fin - 1)
                    ouverture = random.randint(x_debut, x_fin)
                    for colonne in range(x_debut, x_fin):
                        if colonne == ouverture:
                            matrice[y_coupe][colonne] = ","
                            if y_coupe - 1 > y_debut :
                                matrice[y_coupe - 1][colonne] = ","
                            if y_coupe + 1 < y_fin :
                                matrice[y_coupe + 1][colonne] = ","
                    
                        else :
                            if matrice[y_coupe][colonne] != ",":
                                matrice[y_coupe][colonne] = "X"
                                
                    generation(matrice, x_debut, y_debut, x_fin, y_coupe - 1)
                    generation(matrice, x_debut, y_coupe + 1, x_fin, y_fin)
                return matrice
            
def select(matrice):
    """
    Fonction ajoutant un depart et une arrivée dans la matrice
    """
    x_depart = random.randint(1,(len(matrice[0])-2)//4)
    y_depart = random.randint(1,(len(matrice)-2)//4)
    
    depart = (x_depart, y_depart)  #On place le depart dans le quart superieur gauche du labyrinthe
    
    borne_x = 3*(len(matrice[0])//4)
    borne_y = 3*(len(matrice)//4)
    
    x_arrivee = random.randint(1,len(matrice[0])-2)
    if x_arrivee >= borne_x:
        y_arrivee = random.randint(1,len(matrice)-2)
    else : y_arrivee = random.randint(borne_y, len(matrice)-2)
    
    arrivee = (x_arrivee, y_arrivee)
    
    matrice[y_depart][x_depart] = "D"
    matrice[y_arrivee][x_arrivee] = "A"
    
    return matrice, depart, arrivee
    
def creer(x, y):
    """
    Fonction qui utilise les precedentes afin de creer une matrice interpretable et jouable
    """
    matrice = base(x, y)
    maze = select(generation(matrice, 1, 1, len(matrice[0])-1, len(matrice)-1)) #On recupere la matrice créée le depart et l'arrivée
    if resolution.solution(maze[0], maze[1], maze[2]):
        return maze[0]      #On teste si il existe une solution a ce labyrinthe (pour des raisons obscures, il arrive que certaines parties soit inaccessibles)
    else : creer(x, y)      #Si le labyrinthe n'est pas viable on en recrée un   

def to_laby(matrice):
    """
    Fonction convertissant la matrice de génération en une autre de 0 et 1, interpretable par les fonctions de résolution et autres 
    """
    laby = []
    for i in range(len(matrice)):
        laby.append([])
        for j in range(len(matrice[i])):
            if matrice[i][j] == "X" :
                laby[i].append(1)
            elif matrice[i][j] == "A" : 
                laby[i].append(2)
            elif matrice[i][j] == "D":
                laby[i].append(3)
            else: laby[i].append(0)
    return laby
