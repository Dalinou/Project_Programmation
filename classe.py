import json
# pour recupérer les classes
''' 
# Ouverture du fichier
with open("classe.json") as data:
    # Ouverture du fichier à l'aide du décodeur json et décoder classe.decode
    z = json.load(data, object_hook=classe.decode)
# sert à désigner chaque classe par son nom, non un numéro (pas forcément fixe)
z = {z[i].classe_name: z[i] for i in range(z.__len__())}
'''


class Classe:
    def __init__(self, classe_name, defense, atk, pv, description, atk_type):
        self.classe_name = classe_name
        self.defense = defense
        self.atk = atk
        self.pv = pv
        self.description = description
        self.atk_type = atk_type


def decode(dct):
    if "__classe__" in dct:
        return Classe(dct["classe name"], dct["def"], dct["atk"], dct["pv"], dct["description"], dct["atk type"])
    return dct

