def avancer(etape, mat, mtravail):
  """
  Fonction qui permet d'actualiser la matrice de travail par rapport à la distance avec l'origine + 1.
  Donne un parcours en largeur si répétée
  
  etape : indice de l'element sur lequel on travail, distance parcourue depuis le départ
  mat : labyrinthe originel, composé de 0 et de 1 
  mtravail : matrice de 0 de la taille de mat mais actualisée a chaque appel de cette fonction
  """
  for y in range(len(mtravail)):
    for x in range(len(mtravail[y])):
      if mtravail[y][x] == etape:  #On cherche les indices correspondant a l'etape
        
        if y>0 and mtravail[y-1][x] == 0 and mat[y-1][x] != 1:  # 3 tests : Est ce que l'elt est dans la matrice, l'a t-on deja exploré, est-il explorable
          mtravail[y-1][x] = etape + 1 #On augmente la valeur de l'elt en bas
          
        if x>0 and mtravail[y][x-1] == 0 and mat[y][x-1] != 1:
          mtravail[y][x-1] = etape + 1 #On augmente la valeur de l'elt a gauche 
          
        if y<len(mtravail)-1 and mtravail[y+1][x] == 0 and mat[y+1][x] != 1:
          mtravail[y+1][x] = etape + 1 #On augmente la valeur de l'elt en haut
          
        if x<len(mtravail[y])-1 and mtravail[y][x+1] == 0 and mat[y][x+1] != 1:
           mtravail[y][x+1] = etape + 1 #On augmente la valeur de l'elt a droite

def afficher(mat):
  """
  Fonction permettant d'afficher proprement une matrice
  """
  for i in range(len(mat)):
      for j in range(len(mat[i])):
          print( str(mat[i][j]),end=' ')
      print()

def solution(laby, depart, arrivee):
  """
  Fonction retournant le chemin de traversée d'un labyrinthe, liste de tuples de coordonnées matricielles
  
  laby : matrice de 0 et 1 , 1 pour les blocs pleins et 0 pour les utilisables
  depart : point de depart, tuple
  arrivee : point d'arrivée, tuple
  """
  
  mtravail = []
  for i in range(len(laby)):
      mtravail.append([])
      for j in range(len(laby[i])):
          mtravail[-1].append(0)
  # On crée la matrice de 0 qui nous sert a établir les distances

  x_depart, y_depart = depart[0], depart[1]  #On initialise les coordonées du départ
  mtravail[y_depart][x_depart] = 1  #On considère le départ comme la première étape

  k = 0
  while mtravail[arrivee[1]][arrivee[0]] == 0:  
      k += 1
      avancer(k, laby, mtravail)
  #Tant que le point representant l'arrivée sur mtravail n'a pas été atteint on avance 



  ##################################################### Partie II ################################################################



  #Dans cette partie on va se servir de l'ordre des indices pour remonter et etablir le chemin.

  x, y = arrivee  #On part de l'arrivée
  k = mtravail[y][x]  #On récupère l'indice max
  chemin = [(x, y)] #On inclut l'arrivée dans le chemin

  while k > 1: #Tant qu'on est à pas a la première étape (le départ), on continue de remonter
    
    if y > 0 and mtravail[y - 1][x] == k-1:  #S'il y a un élément en dessus de celui ou on est et qu'il vaut la valeur inferieure a l'elt actuel
      y, x = y-1, x                          #On se place a la postion de cet élément
      chemin.insert(0,(x, y))                #On ajoute ses coordonées au chemin
      k-=1                                   #On décremente pour pouvoir recommencer
      
    elif x > 0 and mtravail[y][x - 1] == k-1:  #Idem a gauche
      y, x = y, x-1
      chemin.insert(0,(x, y))
      k-=1
      
    elif y < len(mtravail) - 1 and mtravail[y + 1][x] == k-1:  #Idem en dessous
      y, x = y+1, x
      chemin.insert(0,(x, y))
      k-=1
      
    elif x < len(mtravail[y]) - 1 and mtravail[y][x + 1] == k-1:   #Idem a droite
      y, x = y, x+1
      chemin.insert(0,(x, y))
      k -= 1

  return chemin #On renvoie la liste contenant un des itineraires pour resoudre le labyrinthe

"""
laby, depart, arrivee = generation.creer(1000,1000)
laby = generation.to_laby(laby)

print(solution(laby, depart, arrivee))
"""