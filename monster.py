import json
import math
import pygame


# classe qui gère les statistiques des monstres ainsi que leur mouvements, en récupérant les valeurs de base dans
# le .json
class Monster:
    def __init__(self, data):
        """
        :param data: attribut qui contient toutes les données du monstre
        """
        # création des variables pour les statistiques des monstres + leur texture
        if "__monster__" in data:
            self.type = data["type"]
            self.pv = data["pv"]
            if "pv max" in data:
                self.pv_max = data["pv max"]
            else:
                self.pv_max = data["pv"]
            self.atk = data["atk"]
            self.defense = data["def"]
            self.mvt = data["mvt"]
            self.location = data["location"]
            if "texture" in data:
                self.texture = pygame.image.load(data["texture"])
            else:
                with open("monster.json") as data:
                    z = json.load(data)
                    z = {z[i]["type"]: z[i] for i in range(z.__len__())}
                    if self.type in z:
                        self.texture = pygame.image.load(z[self.type]["texture"])

    # renvoie les données à sauvegarder
    def save(self):
        return {"__monster__": True, "type": self.type, "atk": self.atk, "pv": self.pv, "pv max": self.pv_max,
                "def": self.defense, "mvt": self.mvt, "location": self.location}

# fonction qui permet de générer un monstre sur la carte


def gen_monster(type_, init_location):
    """
    :param type_: attribut qui définit la race du monstre
    :param init_location: attribut qui définit la position initiale du monstre
    :return: renvoie les données concernant le monstre
    """
    # look in monster.json
    with open("monster.json") as data:
        z = json.load(data)
        z = {z[i]["type"]: z[i] for i in range(z.__len__())}
        if type_ in z:
            data = z[type_]
            data["location"] = init_location
            return Monster(data)

# Fonction qui renvoie la distance entre deux entité
def dist(s1, s2):
    if s1.location[2] != s2.location[2]:
        return -1
    else:
        return math.sqrt(math.pow(s1.location[0]-s2.location[0], 2) + math.pow(s1.location[1]-s2.location[1], 2))

# Fonction qui fait se déplacer le monstre vers le joueur
def move_forward_player(maps, monster_, player, traget_dist):
    if monster_.location[2] == player.location[2]:
        ...
    else:
        return -1
