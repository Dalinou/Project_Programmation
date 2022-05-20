import pygame


# classe qui gère les statistiques des monstres ainsi que leur mouvements
class Monster:
    def __init__(self, name, pv, atk, defense, texture):
        # création des variables pour les statistiques des monstres + leur texture
        self.name = name
        self.pv = pv
        self.atk = atk
        self.defense = defense
        self.texture = pygame.image.load(texture)

    # permet de récuperer les informations contenus dans le json
    def decode(dct):
        if "__monster__" in dct:
            return Monster(dct["name"], dct["def"], dct["atk"], dct["pv"],
                           dct["texture"])
        return dct
