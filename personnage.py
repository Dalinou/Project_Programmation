import json
import classe
import pygame

# Classe qui permet d'initialiser les attributs du personnage , soit en provenance de classe.json pour les premières
# puis par la suite en les récupérant directement dans la sauvegarde


class Personnage:
    def __init__(self, data):
        """
        :param data: attribut qui contient toutes les données du personnage
        """
        if "__personnage__" in data:
            self.name = data["name"]
            if self.name == "Diablo":
                self.classe = "Devil"
                self.gender = data["gender"]
                self.pv = data["pv"]
                self.pv_max = 666
                self.atk = data["atk"]
                self.defense = data["def"]
                self.mvt = 13
                self.location = data["location"]
                self.atk_type = ["Voile de tenebre", "Malediction"]
                self.texture = pygame.image.load("Texture/Diablo.png")
            else:
                self.classe = data["classe"]
                self.gender = data["gender"]
                self.pv = data["pv"]
                self.pv_max = data["pv max"]
                self.atk = data["atk"]
                self.defense = data["def"]
                self.mvt = data["mvt"]
                self.location = data["location"]
                self.atk_type = data["atk type"]
                # récupération des textures
                with open("classe.json") as data:
                    # Ouverture du fichier à l'aide du décodeur json et décoder classe.decode
                    z = json.load(data, object_hook=classe.decode)
                    # sert à désigner chaque classe par son nom, non un numéro (pas forcément fixe)
                    z = {z[i].classe_name: z[i] for i in range(z.__len__())}
                self.texture = z[self.classe].texture["face " + self.gender]

    # renvoie les données à sauvegarder
    def save(self):
        """
        :return: Les données à envoyer dans le json pour le bon fonctionnement de la sauvegarde
        """
        return {"__personnage__": True, "name": self.name, "classe": self.classe, "gender": self.gender,
                "atk": self.atk, "pv": self.pv, "pv max": self.pv_max,
                "atk type": self.atk_type, "def": self.defense,
                "mvt": self.mvt, "location": self.location}

# fonction qui gère la création d'un nouveau personnage


def gen_perso(classe_, gender, init_location, name):
    """
    :param classe_: attribut qui gère la profession du personnage
    :param gender: attribut qui gère le sexe du personnage
    :param init_location: attribut qui définit la position initiale du personnage
    :param name: attribut qui définit le nom du personnage
    :return:
    """
    with open("classe.json") as data:
        # Ouverture du fichier à l'aide du décodeur json et décoder classe.decode
        z = json.load(data, object_hook=classe.decode)
    # sert à désigner chaque classe par son nom, non un numéro (pas forcément fixe)
    z = {z[i].classe_name: z[i] for i in range(z.__len__())}
    classe_ = z[classe_]
    # retourne toutes les informations concernant le personnage
    return Personnage({"__personnage__": True, "name": name, "classe": classe_.classe_name, "gender": gender,
                       "atk": classe_.atk, "pv": classe_.pv, "pv max": classe_.pv, "atk type": classe_.atk_type,
                       "def": classe_.defense,
                       "mvt": classe_.mvt, "location": init_location})
