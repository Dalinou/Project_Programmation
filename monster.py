import json

import pygame


# classe qui gère les statistiques des monstres ainsi que leur mouvements
class Monster:
    def __init__(self, data):
        # création des variables pour les statistiques des monstres + leur texture
        if "__monster__" in data:
            self.type = data["type"]
            self.pv = data["pv"]
            self.atk = data["atk"]
            self.defense = data["def"]
            self.mvt = data["mvt"]
            self.location = data["location"]
            self.texture = pygame.image.load(data["texture"])

    def save(self):
        return {"__monster__": True, "type": self.type, "atk": self.atk, "pv": self.pv, "pv max": self.pv,
                "def": self.defense, "mvt": self.mvt, "location": self.location}


def gen_monster(type_, init_location):
    # look in monster.json
    with open("monster.json") as data:
        z = json.load(data)
        z = {z[i]["type"]: z[i] for i in range(z.__len__())}
        if type_ in z:
            data = z[type_]
            data["location"] = init_location
            return Monster(data)
