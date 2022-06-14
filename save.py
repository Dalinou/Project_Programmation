import json

import monster
import personnage

# permet de gérer la sauvegarde et de la lire, notamment grâce à un .json


# Chargement de la sauvergarde, renvoie un object sauvegard
''' code à mettre pour charger la sauvergarde
# Chargement de la sauvegarde
# Donnée brut, a renvoyer lors d'un sauvegarde
raw_data = save.load_save("save.json")
# Récupération du personnage et de la liste des monstres
perso = None
monster_list = []
if "personnage" in raw_data:
    if raw_data["personnage"].__class__ == personnage.Personnage:
        perso = raw_data["personnage"]
if "monster_list" in raw_data:
    for element in raw_data["monster_list"]:
        if element.__class__ == monster.Monster:
            monster_list.append(element)
'''
def load_save(filename):
    """

    :param filename: attribut qui est le nom du fichier de sauvegarde dans lequel on souhaite prendre les informations
    :return: retourne les infos contenu dans le fichier
    """
    with open(filename) as file:
        file_data = json.load(file)
    out_data = {"monster_list": []}
    for data in file_data:
        if "__personnage__" in data:
            if not "personnage" in out_data:
                out_data["personnage"] = personnage.Personnage(data)
        if "__monster__" in data:
            out_data["monster_list"].append(monster.Monster(data))
    return out_data


# Sauvegarde la sauvegarde de data dans filename
def dump_save(filename, in_data):
    """

    :param filename: attribut qui est le nom du fichier de sauvegarde existant qu'on souhaite modifier
    :param in_data: attribut qui sont les données à sauvegarder
    """
    data = []
    if "personnage" in in_data:
        if in_data["personnage"].__class__ == personnage.Personnage:
            data.append(in_data["personnage"].save)
    if "monster_list" in in_data:
        for element in in_data["monster_list"]:
            if element.__class__ == monster.Monster:
                data.append(element.save)
    data = json.dumps(data, indent=2)
    open(filename, 'w').write(data)


# Initialisation de la sauvegarde
# Data doit comptenir les données de classe
# gender de genre et location les coordonnées initials
def init_save(filename, classe, gender, init_location, name):
    """
    :param filename: attribut qui gère le nom du fichier de sauvegarde
    :param classe: attribut qui gère la profession du personnage
    :param gender: attribut qui gère le sexe du personnage
    :param init_location: attribut qui définit la position initiale du personnage sur la carte
    :param name: attribut qui définit le nom du personnage
    """
    data = [personnage.gen_perso(classe, gender, init_location, name).save,
            monster.gen_monster("Orc", [29, 15, "Test map 1"]).save,
            monster.gen_monster("Gobelin", [5, 5, "Test map 1"]).save,
            monster.gen_monster("Gobelin", [42, 26, "Test map 1"]).save,
            monster.gen_monster("Loup", [33, 5, "Test map 1"]).save]
    data = json.dumps(data, indent=2)
    open(filename, 'w').write(data)
