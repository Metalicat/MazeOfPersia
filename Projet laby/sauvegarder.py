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
