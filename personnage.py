class Personnage:
    def __init__(self, data):
        if "__personnage__" in data:
            self.classe = data["classe"]
            self.gender = data["gender"]
            self.pv = data["pv"]
            self.pv_max = data["pv max"]
            self.atk = data["atk"]
            self.defense = data["def"]

    def save(self):
        return{
            "__personnage__": True,
            "classe": self.classe,
            "gender": self.gender,
            "pv": self.pv,
            "pv max": self.pv_max,
            "atk": self.atk

        }




