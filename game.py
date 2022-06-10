import math

import pygame.image
import save
import sys
import maps
import button
import json

# cette classe défini l'écran principal du jeu, avec notamment la carte ou évolue le joueur tant qu'il n'est pas
# en combat.


class GameScreen:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        # création de la carte
        self.maps = maps.Maps("maps.json", [0, 0, "Test map 1"], self.setting)
        self.perso = save.load_save("save.json")
        self.sprite_list = []
        # création du bouton pour revenir au menu et sauvegarder
        self.button_save = button.Button(
            [self.setting.screensize[0] * 1.25 / 15, self.setting.screensize[1] * 1 / 15],
            2,
            0,
            ["Texture/Button Back up game.png", "Texture/Button Back down game.png"],
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
                        move_sprite(self.maps, self.perso, "up")
                    elif event.key == pygame.K_LEFT:
                        move_sprite(self.maps, self.perso, "left")
                    elif event.key == pygame.K_DOWN:
                        move_sprite(self.maps, self.perso, "down")
                    elif event.key == pygame.K_RIGHT:
                        move_sprite(self.maps, self.perso, "right")

            self.maps.location = self.perso.location
            self.maps.render(self.window, [self.perso, *self.sprite_list])
            self.button_save.render(self.window)
            self.window.blit(self.texture_cursor, self.cursor_coord)
            pygame.display.update()
    # chargement differentes Map
    # chargement savegarde du jeu
    # Gameloop de jeu

# Cette classe prend le relais sur la précédente lorsque le joueur entre en combat, notamment en définissant
# une nouvelle carte et de nouveau paramètre comme la limitation des mouvements etc


class FightScreen:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        self.maps = maps.Maps("maps.json", [3, 3, "Fight map"], self.setting)
        # Lecture des différentes attaques
        self.atk_list = {}
        with open("atk def.json") as file:
            datas = json.load(file)
            for data in datas:
                if "__atk_def__" in data:
                    self.atk_list[data["__atk_def__"]] = data
        # bouton sauvegarder
        self.button_save = button.Button(
            [self.setting.screensize[0] * 1.25 / 15, self.setting.screensize[1] * 1 / 15],
            2,
            0,
            ["Texture/Button Back up.png", "Texture/Button Back down.png"],
            self.button_font,
            [" ", " "],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.button_comp_1 = button.Button(
            [self.setting.screensize[0] * 1 / 5, self.setting.screensize[1] * 4 / 5],
            3,
            0,
            ["Texture/Button up.png", "Texture/Button down.png", "Texture/Button gray.png"],
            self.button_font,
            ["Up", "Down", "Gray"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.button_comp_2 = button.Button(
            [self.setting.screensize[0] * 1 / 2, self.setting.screensize[1] * 4 / 5],
            3,
            0,
            ["Texture/Button up.png", "Texture/Button down.png", "Texture/Button gray.png"],
            self.button_font,
            ["Up", "Down", "Gray"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.button_continue = button.Button(
            [self.setting.screensize[0] * 4 / 5, self.setting.screensize[1] * 4 / 5],
            3,
            0,
            ["Texture/Button up.png", "Texture/Button down.png", "Texture/Button gray.png"],
            self.button_font,
            ["Next Turn", "Next Turn", "Monster Turn"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objects
        self.cursor_coord = (0, 0)

    # Gestion du combat
    def gameloop(self, perso, monster):

        display_perso = maps.Sprite([0, 3, "Fight map"], perso.texture)
        display_monster = maps.Sprite([6, 3, "Fight map"], monster.texture)
        state = "Player"  # Ou "Monster"
        move_left = perso.mvt
        atk_perso_1 = self.atk_list[perso.atk_type[0]]
        atk_perso_1_delay = 0
        self.button_comp_1.change_text([atk_perso_1["__atk_def__"] for i in range(0, 3)])
        atk_perso_2 = self.atk_list[perso.atk_type[1]]
        atk_perso_2_delay = 0
        self.button_comp_2.change_text([atk_perso_2["__atk_def__"] for i in range(0, 3)])
        atk_monster = self.atk_list["attaque monstre"]
        atk_monster_delay = 0
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
                    if atk_perso_1_delay != 0 or state == "Monster":
                        self.button_comp_1.set_state(2)
                    else:
                        if self.button_comp_1.is_coord_on(self.cursor_coord):
                            # change l'état du bouton si la souris est dessus
                            self.button_comp_1.set_state(1)
                        else:
                            self.button_comp_1.set_state(0)
                    if atk_perso_2_delay != 0 or state == "Monster":
                        self.button_comp_2.set_state(2)
                    else:
                        if self.button_comp_2.is_coord_on(self.cursor_coord):
                            # change l'état du bouton si la souris est dessus
                            self.button_comp_2.set_state(1)
                        else:
                            self.button_comp_2.set_state(0)
                    if state == "Player":
                        if self.button_continue.is_coord_on(self.cursor_coord):
                            self.button_continue.set_state(1)
                        else:
                            self.button_continue.set_state(0)
                    else:
                        self.button_continue.set_state(2)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_save.state == 1:
                        return "menu"
                    if self.button_continue.state == 1 and state == "Player":
                        state = "Monster"
                        move_left = monster.mvt
                        self.button_continue.set_state(2)
                        self.button_comp_1.set_state(2)
                        self.button_comp_2.set_state(2)
                        atk_monster_delay = max(atk_monster_delay - 1, 0)
                        atk_perso_1_delay = max(atk_perso_1_delay - 1, 0)
                        atk_perso_2_delay = max(atk_perso_2_delay - 1, 0)
                    if self.button_comp_1.state == 1 and atk_perso_1_delay == 0:
                        if atk_perso_1["range"] == [-1, -1] or atk_perso_1["range"][0] <=\
                                dist(display_perso, display_monster) <= atk_perso_1["range"][1]:
                            monster.pv -= max(perso.atk * atk_perso_1["atk ratio"] - monster.defense, 0)
                            for element in atk_perso_1["special effect"]:
                                ...
                elif event.type == pygame.KEYDOWN and move_left > 0 and state == "Player":
                    # Mouvement de la mire + vérification si tjrs dans la carte
                    if event.key == pygame.K_UP:
                        if move_sprite(self.maps, display_perso, "up"):
                            move_left -= 1
                    elif event.key == pygame.K_LEFT:
                        if move_sprite(self.maps, display_perso, "left"):
                            move_left -= 1
                    elif event.key == pygame.K_DOWN:
                        if move_sprite(self.maps, display_perso, "down"):
                            move_left -= 1
                    elif event.key == pygame.K_RIGHT:
                        if move_sprite(self.maps, display_perso, "right"):
                            move_left -= 1
            self.maps.render(self.window, [display_perso, display_monster])
            self.button_save.render(self.window)
            self.button_comp_1.render(self.window)
            self.button_comp_2.render(self.window)
            self.button_continue.render(self.window)
            self.window.blit(self.texture_cursor, self.cursor_coord)
            pygame.display.update()


# Fonction qui déplace un sprite dans une direction donné en vérifiant si l'on peut aller sur la case de déstination
def move_sprite(maps, sprite, direction):
    if direction == "up" and sprite.location[1] > 0:
        dest = maps.map[sprite.location[2]].map[sprite.location[1] - 1][sprite.location[0]]
        is_walkable = maps.tile[dest].is_walkable
        if is_walkable:
            sprite.location[1] = sprite.location[1] - 1
            return True
    elif direction == "left" and sprite.location[0] > 0:
        dest = maps.map[sprite.location[2]].map[sprite.location[1]][sprite.location[0] - 1]
        is_walkable = maps.tile[dest].is_walkable
        if is_walkable:
            sprite.location[0] = sprite.location[0] - 1
            return True
    elif direction == "down" and sprite.location[1] < maps.map[sprite.location[2]].res[1] - 1:
        dest = maps.map[sprite.location[2]].map[sprite.location[1] + 1][sprite.location[0]]
        is_walkable = maps.tile[dest].is_walkable
        if is_walkable:
            sprite.location[1] = sprite.location[1] + 1
            return True
    elif direction == "right" and sprite.location[0] < maps.map[sprite.location[2]].res[0] - 1:
        dest = maps.map[sprite.location[2]].map[sprite.location[1]][sprite.location[0] + 1]
        is_walkable = maps.tile[dest].is_walkable
        if is_walkable:
            sprite.location[0] = sprite.location[0] + 1
            return True
    return False

# Fonction qui renvoie la distance entre deux entité
def dist(s1, s2):
    if s1.location[2] != s2.location[2]:
        return -1
    else:
        return math.sqrt(math.pow(s1.location[0]-s2.location[0], 2) + math.pow(s1.location[1]-s2.location[1], 2))
