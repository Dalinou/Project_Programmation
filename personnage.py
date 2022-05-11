class Personnage:
    def __init__(self, data):
        if "__personnage__" in data:
            self.classe_type = data["classe type"]
            self.gender = data["gender"]
            self.pv = data["pv"]
            self.pv_max = data["pv_max"]
            self.atk = data["atk"]
            self.defense = data["def"]



