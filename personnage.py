import json
import classe

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
            self.coord = data["location"]
            with open("classe.json") as data:
                # Ouverture du fichier à l'aide du décodeur json et décoder classe.decode
                z = json.load(data, object_hook=classe.decode)
                # sert à désigner chaque classe par son nom, non un numéro (pas forcément fixe)
                z = {z[i].classe_name: z[i] for i in range(z.__len__())}
            self.texture = z[self.classe].texture["face " + self.gender]

    def save(self):
        return{
            "__personnage__": True,
            "classe": self.classe,
            "gender": self.gender,
            "pv": self.pv,
            "pv max": self.pv_max,
            "atk": self.atk,
            "mvt": self.mvt

        }




