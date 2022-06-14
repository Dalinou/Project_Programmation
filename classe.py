import json
import pygame
# pour recupérer les classes
''' 
# Ouverture du fichier
with open("classe.json") as data:
    # Ouverture du fichier à l'aide du décodeur json et décoder classe.decode
    z = json.load(data, object_hook=classe.decode)
# sert à désigner chaque classe par son nom, non un numéro (pas forcément fixe)
z = {z[i].classe_name: z[i] for i in range(z.__len__())}
'''
# cette classe permet de récuperer les statistiques de base de chaque classe qui ont été fixées dans le
# .json et de les associer à une variable, ce qui permet de modifier ces valeurs sans toucher à la valeur de base


class Classe:
    def __init__(self, classe_name, defense, atk, pv, mvt, description, atk_type, texture):
        """
        :param classe_name: nom du personnage
        :param defense: attribut qui définit la protection du personnage
        :param atk: attribut qui définit la protection du personnage
        :param pv: attribut qui définit les points de vie du personnage
        :param mvt: attribut qui définit les mouvements du personnage
        :param description: //
        :param atk_type: attribut qui définit les différents types d'attaque du personnage
        :param texture: attribut qui définit la texture du personnage
        """
        # Recuperation des variables
        self.classe_name = classe_name
        self.defense = defense
        self.atk = atk
        self.pv = pv
        self.mvt = mvt
        self.description = description
        self.atk_type = atk_type
        self.texture = texture
        # Recuperation des textures
        for name in self.texture:
            self.texture[name] = pygame.image.load(self.texture[name])


# permet de récuperer les informations contenus dans le json
def decode(dct):
    if "__classe__" in dct:
        return Classe(dct["classe name"], dct["def"], dct["atk"], dct["pv"], dct["mvt"],
                      dct["description"], dct["atk type"], dct["texture"])
    return dct

