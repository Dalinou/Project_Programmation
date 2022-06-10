import json
import classe

# Classe qui permet d'initialiser les attributs du personnage , soit en provenance de classe.json pour les premières
# puis par la suite en les récupérant directement dans la sauvegarde


class Personnage:
    def __init__(self, data):
        if "__personnage__" in data:
            self.name = data["name"]
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

    # permet de sauvegarder les valeurs des différentes variables

    def save(self):
        return {"__personnage__": True, "name": self.name, "classe": self.classe, "gender": self.gender,
                "atk": self.atk, "pv": self.pv, "pv max": self.pv,
                "atk type": self.atk_type, "def": self.defense,
                "mvt": self.mvt, "location": self.location}

# fonction qui gère la création d'un nouveau personnage


def gen_perso(classe_, gender, init_location, name):
    with open("classe.json") as data:
        # Ouverture du fichier à l'aide du décodeur json et décoder classe.decode
        z = json.load(data, object_hook=classe.decode)
    # sert à désigner chaque classe par son nom, non un numéro (pas forcément fixe)
    z = {z[i].classe_name: z[i] for i in range(z.__len__())}
    classe_ = z[classe_]
    return Personnage({"__personnage__": True, "name": name, "classe": classe_.classe_name, "gender": gender,
                       "atk": classe_.atk, "pv": classe_.pv, "pv max": classe_.pv, "atk type": classe_.atk_type,
                       "def": classe_.defense,
                       "mvt": classe_.mvt, "location": init_location})
