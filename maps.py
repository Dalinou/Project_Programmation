import json
import pygame.image


# Classe Maps sert à stocker les informations des cartes, elle fait aussi la gestion de son affichage
class Maps:
    def __init__(self, filename, init_location, setting):
        self.setting = setting
        self.filename = filename
        self.location = init_location
        self.map = {}
        self.tile = {}
        self.tilesize = None
        # fait le décodage de maps.json
        self.decode()

    # Fonction pour faire le rendu de la carte, centré autour du perso
    def render(self, window, sprite_list):
        # selectionne la carte à utiliser
        map_ = self.map[self.location[2]]
        # définit l'offset minimun par rapport au bord avant de bouger
        off = [3, 3]
        # définit les coordonées de la case en (0, 0)
        location0 = [self.setting.screensize[0] / 2 - map_.res[0] * self.tilesize[0] / 2,
                  self.setting.screensize[1] / 2 - map_.res[1] * self.tilesize[1] / 2]

        # vérifie si location0 respecte l'offset et le rectifie si besoin
        if location0[0] + self.tilesize[0] * (self.location[0] - off[0]) < 0:
            location0[0] = 0 - (0 if self.location[0] <= off[0] else self.location[0] - 3) * self.tilesize[0]
        elif location0[0] + self.tilesize[0] * (self.location[0] + off[0] + 1) >= self.setting.screensize[0]:
            location0[0] = max(self.setting.screensize[0] / self.tilesize[0] - self.location[0] - off[0] - 1,
                            self.setting.screensize[0] / self.tilesize[0] - map_.res[0]) * self.tilesize[0]
        if location0[1] + self.tilesize[1] * (self.location[1] - off[1]) < 0:
            location0[1] = 0 - (0 if self.location[1] <= off[1] else self.location[1] - 3) * self.tilesize[1]
        elif location0[1] + self.tilesize[1] * (self.location[1] + off[1] + 1) >= self.setting.screensize[1]:
            location0[1] = max(self.setting.screensize[1]/self.tilesize[1] - self.location[1] - off[1] - 1,
                            self.setting.screensize[1] / self.tilesize[1] - map_.res[1]) * self.tilesize[1]
        # affiche le fond d'écran
        window.blit(map_.background, (0, 0))
        # affichage les tuiles de la carte
        for i in range(0, map_.res[1]):
            for j in range(0, map_.res[0]):
                window.blit(self.tile[map_.map[i][j]].texture,
                            [j * self.tilesize[0] + location0[0], i * self.tilesize[1] + location0[1]])
        # affichage de la liste de sprite donnée, un sprite doit avoir comme donnée : une coordonée et une texture
        for el in sprite_list:
            if el.location[2] == self.location[2] and 0 <= el.location[0] < map_.res[0] and 0 <= el.location[1] < map_.res[1]:
                window.blit(el.texture, [self.tilesize[0] * el.location[0] + location0[0],
                                         self.tilesize[1] * el.location[1] + location0[1]])

    # Fonction pour lire le maps.json
    def decode(self):
        # lit le fichier
        data = json.load(open(self.filename))
        if "__maps__" in data:
            # récupération de la tile des textures
            self.tilesize = data["tilesize"]
            # récupère en fonction une donnée de carte ou de tuile
            for element in data["data"]:
                if "__map__" in element:
                    self.map[element["__map__"]] = Map(self.setting, element)
                elif "__tile__" in element:
                    self.tile[element["__tile__"]] = Tile(element)


# Classe qui stocke les données d'une carte
class Map:
    def __init__(self, setting, data):
        if "__map__" in data:
            self.res = data["res"]
            self.map = data["map data"]
            self.background = setting.get_texture(data["background"])
        else:
            self.res = [0, 0]
            self.map = [[]]
            self.background = pygame.image.load("Texture/Default.png")


# définit les cases qui compose la carte, leur texture et si le personnage peut marcher dessus
class Tile:
    def __init__(self, data):
        """

        :param data: Toute les données de la tuile
        """
        if "__tile__" in data:
            self.texture = pygame.image.load(data["texture"])
            self.is_walkable = data["is walkable"]
        else:
            self.texture = pygame.image.load("Texture/Default.png")
            self.is_walkable = True


# class minimun pour être affiché sur la carte
class Sprite:
    def __init__(self, location, texture):
        self.location = location
        self.texture = texture
