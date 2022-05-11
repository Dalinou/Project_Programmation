import json


class classe:
    def __init__(self, classe_name, defense, atk, pv, description, atk_type):
        self.classe_name = classe_name
        self.defense = defense
        self.atk = atk
        self.pv = pv
        self.description = description
        self.atk_type = atk_type


def decode(dct):
    if "__classe__" in dct:
        return classe(dct["classe name"], dct["def"], dct["atk"], dct["pv"], dct["description"], dct["atk_type"])
    return dct

