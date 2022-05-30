import json
import pygame.image

import save
import settings
import sys
import maps


class GameScreen:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.maps = maps.Maps("maps.json", [0, 0, "Test map 1"], self.setting)
        self.perso = save.load_save("save.json")

    def gameloop(self):
        while True:
            # clock.tick pour respecter le fps
            self.clock.tick(self.setting.fps)
            for event in pygame.event.get():
                # Lecture des entrées et interprétation
                # Si alt-f4 ou croix rouge
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Mouvement de la mire + vérification si tjrs dans la carte
                    if event.key == pygame.K_UP:
                        self.perso.coord[1] = self.perso.coord[1] - 1 if self.perso.coord[1] > 0 else 0
                    elif event.key == pygame.K_LEFT:
                        self.perso.coord[0] = self.perso.coord[0] - 1 if self.perso.coord[0] > 0 else 0
                    elif event.key == pygame.K_DOWN:
                        self.perso.coord[1] = self.perso.coord[1] + 1 if self.perso.coord[1] < self.maps.map[self.perso.coord[2]].res[1] - 1 \
                            else self.maps.map[self.perso.coord[2]].res[1] - 1
                    elif event.key == pygame.K_RIGHT:
                        self.perso.coord[0] = self.perso.coord[0] + 1 if self.perso.coord[0] < self.maps.map[self.perso.coord[2]].res[0] - 1 \
                            else self.maps.map[self.perso.coord[2]].res[0] - 1
            self.maps.coord = self.perso.coord
            self.maps.render(self.window, [self.perso])
            pygame.display.update()
    # chargement differentes Map
    # chargement savegarde du jeu
    # Gameloop de jeu


class Map:
    ...
    # Gestion de la carte et affichage
    # Liste sprite

