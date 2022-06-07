import json
import pygame.image

import save
import settings
import sys
import maps
import button


class GameScreen:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        self.maps = maps.Maps("maps.json", [0, 0, "Test map 1"], self.setting)
        self.perso = save.load_save("save.json")
        self.button_save = button.Button(
            [self.setting.screensize[0] * 1.25 / 15, self.setting.screensize[1] * 1 / 15],
            2,
            0,
            ["Texture/Button Back up.png", "Texture/Button Back down.png"],
            self.button_font,
            [" ", " "],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objects
        self.cursor_coord = (0, 0)

    def gameloop(self):
        while True:
            # clock.tick pour respecter le fps
            self.clock.tick(self.setting.fps)
            for event in pygame.event.get():
                # Lecture des entrées et interprétation
                # Si alt-f4 ou croix rouge
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    # récupération des coordonnées de la souris
                    self.cursor_coord = event.pos
                    if self.button_save.is_coord_on(self.cursor_coord):
                        # change l'état du bouton si la souris est dessus
                        self.button_save.set_state(1)
                    else:
                        self.button_save.set_state(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_save.state == 1:
                        return "menu"
                elif event.type == pygame.KEYDOWN:
                    # Mouvement du joueur + vérification si tjrs dans la carte
                    if event.key == pygame.K_UP:
                        dest = self.maps.map[self.perso.coord[2]].map[self.perso.coord[0]][self.perso.coord[1]-1]
                        is_walkable = self.maps.tile[dest].is_walkable
                        print(is_walkable)
                        if is_walkable:
                            self.perso.coord[1] = self.perso.coord[1] - 1 if self.perso.coord[1] > 0 else 0
                    elif event.key == pygame.K_LEFT:
                        dest = self.maps.map[self.perso.coord[2]].map[self.perso.coord[0]][self.perso.coord[1] - 1]
                        is_walkable = self.maps.tile[dest].is_walkable
                        self.perso.coord[0] = self.perso.coord[0] - 1 if self.perso.coord[0] > 0 else 0

                    elif event.key == pygame.K_DOWN:
                        dest = self.maps.map[self.perso.coord[2]].map[self.perso.coord[0]][self.perso.coord[1] - 1]
                        is_walkable = self.maps.tile[dest].is_walkable
                        self.perso.coord[1] = self.perso.coord[1] + 1 if self.perso.coord[1] < self.maps.map[self.perso.coord[2]].res[1] - 1 \
                        else self.maps.map[self.perso.coord[2]].res[1] - 1

                    elif event.key == pygame.K_RIGHT:
                        dest = self.maps.map[self.perso.coord[2]].map[self.perso.coord[0]][self.perso.coord[1] - 1]
                        is_walkable = self.maps.tile[dest].is_walkable
                        self.perso.coord[0] = self.perso.coord[0] + 1 if self.perso.coord[0] < self.maps.map[self.perso.coord[2]].res[0] - 1 \
                        else self.maps.map[self.perso.coord[2]].res[0] - 1

            self.maps.coord = self.perso.coord
            self.maps.render(self.window, [self.perso])
            self.button_save.render(self.window)
            self.window.blit(self.texture_cursor, self.cursor_coord)
            pygame.display.update()
    # chargement differentes Map
    # chargement savegarde du jeu
    # Gameloop de jeu


class Map:
    ...
    # Gestion de la carte et affichage
    # Liste sprite

