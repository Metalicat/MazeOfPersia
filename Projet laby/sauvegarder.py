import json
import os
import time

def taille_sauvegarde():
    taille = os.path.getsize('save_file.json')
    return taille

def verif_sauvegarde():
    # On regarde si la save est vide
    if taille_sauvegarde() == 0:
        # Si elle est vite on met dedans les paramettres par défaut
        data = {"general":[100,1],"specific":[[1,0]]}
        with open('save_file.json', 'w') as file:
        # On remplace le contenu du fichier par celui de la variable
            json.dump(data, file)

def charger_sauvegarde():
    # On ouvre le fichier de save
    f = open('save_file.json')
    # On met le fichier contenu dans une variable (sous forme de dico)
    data = json.load(f)
    f.close
    return data

def sauvegarder(niveau,chrono):
    # On ouvre le fichier de save
    f = open('save_file.json')
    # On met le fichier contenu dans une variable (sous forme de dico)
    data = json.load(f)
    # On effectue les modifications souhaitées sur la variable
    if niveau == data["general"][1] :
        data["specific"][niveau-1][1]=chrono
    data["specific"].append([niveau,chrono])
    f.close
    with open('save_file.json', 'w') as file:
        # On remplace le contenu du fichier par celui de la variable
        json.dump(data, file)


# QUAND START :

# On check l'existence de la save
verif_sauvegarde()
# On initialise le temps de départ
temps_debut = time.time()


# QUAND QUITTER

#On récupère le temps d'arret
temps_fin = time.time()
# On charge la save
data = charger_sauvegarde()
# On init le chrono à la valeur du chrono de la partie précédente et on lui ajoute le temps effectué
chrono = data["specific"][data["general"][1]-1][1] + int(temps_fin - temps_debut)
# On l'insère dans le fichier de save 
sauvegarder(niveau,chrono)

# QUAND GG :

#On récupère le temps d'arret
temps_fin = time.time()
# On charge la save
data = charger_sauvegarde()
# On init le chrono à la valeur du chrono de la partie précédente et on lui ajoute le temps effectué
chrono = data["specific"][data["general"][1]-1][1] + int(temps_fin - temps_debut)
# On l'insère dans le fichier de save 
sauvegarder(niveau,chrono)
# On créé la nouvelle save pour le futur niveau
sauvegarder(niveau+1,0)


