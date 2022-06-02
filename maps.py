import json
import pygame.image


# TODO Commentaire !!!
# Classe Maps sert à stocké les informations de cartes, elle fait aussi la gestion de son affichage
class Maps:
    def __init__(self, filename, coord_init, setting):
        self.setting = setting
        self.filename = filename
        self.coord = coord_init
        self.map = {}
        self.tile = {}
        self.tilesize = None
        # fait le décodage de maps.json
        self.decode()

    # Fonction pour fait le rendu de la carte, centré autour du perso
    def render(self, window, sprite_list):
        # selectionne la carte à utilisé
        map_ = self.map[self.coord[2]]
        # définit l'offset minimun par rapport au bord avant de bougé
        off = [3, 3]
        # définit les coordonées de la case en (0, 0)
        coord0 = [self.setting.screensize[0] / 2 - map_.res[0] * self.tilesize[0] / 2,
                  self.setting.screensize[1] / 2 - map_.res[1] * self.tilesize[1] / 2]

        # vérifie si coord0 respecte l'offset et le rectifie si besoin
        if coord0[0] + self.tilesize[0] * (self.coord[0] - off[0]) < 0:
            coord0[0] = 0 - (0 if self.coord[0] <= off[0] else self.coord[0] - 3) * self.tilesize[0]
        elif coord0[0] + self.tilesize[0] * (self.coord[0] + off[0] + 1) >= self.setting.screensize[0]:
            coord0[0] = max(self.setting.screensize[0] / self.tilesize[0] - self.coord[0] - off[0] - 1,
                            self.setting.screensize[0] / self.tilesize[0] - map_.res[0]) * self.tilesize[0]
        if coord0[1] + self.tilesize[1] * (self.coord[1] - off[1]) < 0:
            coord0[1] = 0 - (0 if self.coord[1] <= off[1] else self.coord[1] - 3) * self.tilesize[1]
        elif coord0[1] + self.tilesize[1] * (self.coord[1] + off[1] + 1) >= self.setting.screensize[1]:
            coord0[1] = max(self.setting.screensize[1]/self.tilesize[1] - self.coord[1] - off[1] - 1,
                            self.setting.screensize[1] / self.tilesize[1] - map_.res[1]) * self.tilesize[1]
        # affiche le fond d'écran
        window.blit(map_.background, (0, 0))
        # affichage les tuiles de la carte
        for i in range(0, map_.res[1]):
            for j in range(0, map_.res[0]):
                window.blit(self.tile[map_.map[i][j]].texture,
                            [j * self.tilesize[0] + coord0[0], i * self.tilesize[1] + coord0[1]])
        # affichage de la liste de sprite donnée, un sprite doit avoir comme donnée : une coordonée et une texture
        for el in sprite_list:
            if el.coord[2] == self.coord[2] and 0 <= el.coord[0] < map_.res[0] and 0 <= el.coord[1] < map_.res[1]:
                window.blit(el.texture, [self.tilesize[0] * el.coord[0] + coord0[0],
                                         self.tilesize[1] * el.coord[1] + coord0[1]])

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


class Tile:
    def __init__(self, data):
        if "__tile__" in data:
            self.texture = pygame.image.load(data["texture"])
            self.is_walkable = data["is walkable"]
        else:
            self.texture = pygame.image.load("Texture/Default.png")
            self.is_walkable = True


# class type pour ce qu'il faut comment attribut
class Sprite:
    def __init__(self, coord, texture):
        self.coord = coord
        self.texture = texture
