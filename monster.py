import json

import pygame


# classe qui gère les statistiques des monstres ainsi que leur mouvements
class Monster:
    def __init__(self, data):
        # création des variables pour les statistiques des monstres + leur texture
        if "__monster__" in data:
            self.name = data["name"]
            self.pv = data["pv"]
            self.atk = data["atk"]
            self.defense = data["defense"]
            self.texture = data["pygame.image.load(texture)"]

    def monster(type):
        # look in monster.json
        with open("monster.json") as data:
            z = json.load(data)
            z = {z[i]["type"]: z[i] for i in range(z.__len__())}
            if type in z:
                data = z[type]
                return Monster(data)
