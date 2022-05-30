import json
import pygame.image
import settings
import sys


# TODO Commentaire !!!
class Maps:
    def __init__(self, filename, coord_init, setting):
        self.setting = setting
        self.filename = filename
        self.coord = coord_init
        self.map = {}
        self.tile = {}
        self.tilesize = None
        self.decode()

    def render(self, window, sprite_list):
        map_ = self.map[self.coord[2]]
        off = [3, 3]
        coord0 = [self.setting.screensize[0] / 2 - map_.res[0] * self.tilesize[0] / 2,
                  self.setting.screensize[1] / 2 - map_.res[1] * self.tilesize[1] / 2]

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
        window.blit(map_.background, (0, 0))
        for i in range(0, map_.res[1]):
            for j in range(0, map_.res[0]):
                window.blit(self.tile[map_.map[i][j]],
                            [j * self.tilesize[0] + coord0[0], i * self.tilesize[1] + coord0[1]])
        for el in sprite_list:
            if el.coord[2] == self.coord[2] and 0 <= el.coord[0] < map_.res[0] and 0 <= el.coord[1] < map_.res[1]:
                window.blit(el.texture, [self.tilesize[0] * el.coord[0] + coord0[0],
                                         self.tilesize[1] * el.coord[1] + coord0[1]])

    def decode(self):
        data = json.load(open(self.filename))
        if "__maps__" in data:
            self.tilesize = data["tilesize"]
            for element in data["data"]:
                if "__map__" in element:
                    self.map[element["__map__"]] = Map(self.setting, element)
                elif "__tile__" in element:
                    self.tile[element["__tile__"]] = pygame.image.load(element["texture"])


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


class Sprite:
    def __init__(self, coord, texture):
        self.coord = coord
        self.texture = texture


'''
# initiation de pygame
pygame.font.init()
pygame.init()
# Mise en invisible du curseur de windows
# pygame.mouse.set_visible(False)
# changement du nom de la fenêtre et de l'icone
pygame.display.set_caption("Nom du jeu")
pygame.display.set_icon(pygame.image.load("Texture/Game Icon.png"))

# Paramètre
setting = settings.SettingReader()

# Création de la fenetre
if setting.fullscreen:
    window = pygame.display.set_mode(setting.fullscreen_resolution, pygame.FULLSCREEN)
else:
    window = pygame.display.set_mode(setting.screensize)
clock = pygame.time.Clock()
origine = [0, 0, "Test map 1"]
s_list = []
s_list.append(Sprite([3, 9, "Test map 1"], pygame.image.load('Texture/Guerrier_m.png')))
s_list.append(Sprite(origine, pygame.image.load('Texture/Mire 1.png')))
s_list.append(Sprite([4, 7, "Test map 1"], pygame.image.load('Texture/Mage_m.png')))
map = Maps("maps.json", origine)
# Warning : Ici origine est copié dans s.list[1] et dans map, les valeurs des 2 sont donc liée
# (si l'une change l'autre aussi)
print(setting.screensize[0]/32)
while True:
    # clock.tick pour respecter le fps
    clock.tick(setting.fps)
    for event in pygame.event.get():
        # Lecture des entrées et interprétation
        # Si alt-f4 ou croix rouge
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Mouvement de la mire + vérification si tjrs dans la carte
            if event.key == pygame.K_UP:
                map.coord[1] = map.coord[1]-1 if map.coord[1] > 0 else 0
            elif event.key == pygame.K_LEFT:
                map.coord[0] = map.coord[0]-1 if map.coord[0] > 0 else 0
            elif event.key == pygame.K_DOWN:
                map.coord[1] = map.coord[1]+1 if map.coord[1] < map.map[map.coord[2]].res[1] - 1 \
                    else map.map[map.coord[2]].res[1] - 1
            elif event.key == pygame.K_RIGHT:
                map.coord[0] = map.coord[0]+1 if map.coord[0] < map.map[map.coord[2]].res[0] - 1 \
                    else map.map[map.coord[2]].res[0] - 1
    map.render(window, setting, s_list)
    pygame.display.update()
'''
