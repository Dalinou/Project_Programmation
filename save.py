import json
import personnage


# Chargement de la sauvergarde, renvoie un object Map
def load_save(filename):
    with open(filename) as file:
        datas = json.load(file)
    perso = None
    quest_adv = None
    map_list = []
    for data in datas:
        if "__personnage__" in data:
            if perso is None:
                perso = personnage.Personnage(data)
        if "__quest_advencement__" in data:
            if quest_adv is None:
                quest_adv = ...   # charge l'état des quêtes
        if "__map_data__" in data:
            ...
            # map_list.append(map.Map(data))
    # return map object

# Sauvegarde la sauvegarde de data dans filename
def dump_save(filename, data):
    ...
    # sauvegarde les donnés


# Initialisation de la sauvegarde
# Data doit comptenir les données de classe
# gender de genre et location les coordonnées initials
def init_save(filename, classe, gender, location_init, name):
    data = json.dumps([{"__personnage__": True, "name": name, "class": classe.classe_name, "gender": gender, "def": classe.defense,
             "atk": classe.atk, "pv": classe.pv, "pvmax": classe.pv, "atk type": classe.atk_type,
             "location": location_init}], indent=2)
    open(filename, 'w').write(data)
