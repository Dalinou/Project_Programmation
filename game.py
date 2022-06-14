import math

import pygame.image

import monster
import personnage
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
        # initialise l'écran de combat
        self.fight_screen = FightScreen(window, clock, setting)
        # création de la carte
        self.maps = maps.Maps("maps.json", [0, 0, "Test map 1"], self.setting)
        # Chargement de la sauvegarde et recupération du personnage et des monstres
        # Chargement de la sauvegarde
        # Donnée brut, a renvoyer lors d'un sauvegarde
        self.raw_data = save.load_save("save.json")
        # Récupération du personnage et de la liste des monstres
        self.perso = None
        self.monster_list = []
        if "personnage" in self.raw_data:
            if self.raw_data["personnage"].__class__ == personnage.Personnage:
                self.perso = self.raw_data["personnage"]
        if "monster_list" in self.raw_data:
            for element in self.raw_data["monster_list"]:
                if element.__class__ == monster.Monster:
                    self.monster_list.append(element)
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
                        save.dump_save("save.json", self.raw_data)
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
                    # gère l'entrée dans le combat si perso proche du monstre
                    for i in self.monster_list:
                        if dist(self.perso, i) == 1:
                            self.fight_screen.gameloop(self.perso, i)

            self.maps.location = self.perso.location
            self.maps.render(self.window, [self.perso, *self.monster_list])
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
        monster_action_delay_max = self.setting.fps/30 * 6  # en nombre de frame
        monster_action_delay = monster_action_delay_max
        while True:
            # clock.tick pour respecter le fps
            self.clock.tick(self.setting.fps)
            # Fait jouer le monstre
            if state == "Monster":
                next = False
                monster_action_delay -= 1
                if monster_action_delay == 0:
                    monster_action_delay = monster_action_delay_max
                    temp = move_forward_player(self.maps, display_monster, display_perso, atk_monster["range"])
                    if temp == -1:
                        next = True
                    elif temp == 0:
                        fight(monster, display_monster, perso, display_perso, atk_monster)
                        next = True
                    elif temp == 1:
                        move_left -= 1
                if move_left == 0:
                    next = True
                    fight(monster, display_monster, perso, display_perso, atk_monster)
                if next:
                    state = "Player"
                    move_left = perso.mvt
                    self.button_continue.set_state(2)
                    self.button_comp_1.set_state(2)
                    self.button_comp_2.set_state(2)
            # Gestion des entrer de l'utilisateur
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
                        if atk_perso_1["range"] == [-1, -1] or atk_perso_1["range"][0] <= \
                                dist(display_perso, display_monster) <= atk_perso_1["range"][1]:
                            if self.button_comp_1.is_coord_on(self.cursor_coord):
                                # change l'état du bouton si la souris est dessus
                                self.button_comp_1.set_state(1)
                            else:
                                self.button_comp_1.set_state(0)
                        else:
                            self.button_comp_1.set_state(2)
                    if atk_perso_2_delay != 0 or state == "Monster":
                        if atk_perso_2["range"] == [-1, -1] or atk_perso_2["range"][0] <= \
                                dist(display_perso, display_monster) <= atk_perso_2["range"][1]:
                            if self.button_comp_2.is_coord_on(self.cursor_coord):
                                # change l'état du bouton si la souris est dessus
                                self.button_comp_2.set_state(1)
                            else:
                                self.button_comp_2.set_state(0)
                        else:
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
                    if self.button_comp_1.state == 1 and atk_perso_1_delay == 0 and state == "Player":
                        if fight(perso, display_perso, monster, display_monster, atk_perso_1) == 0:
                            atk_perso_1_delay = atk_perso_1["delay"]
                            atk_perso_2_delay = max(atk_perso_2_delay, 1)
                            state = "Monster"
                            move_left = monster.mvt
                            self.button_continue.set_state(2)
                            self.button_comp_1.set_state(2)
                            self.button_comp_2.set_state(2)
                            atk_monster_delay = max(atk_monster_delay - 1, 0)
                            atk_perso_1_delay = max(atk_perso_1_delay - 1, 0)
                            atk_perso_2_delay = max(atk_perso_2_delay - 1, 0)
                    if self.button_comp_2.state == 1 and atk_perso_2_delay == 0 and state == "Player":
                        if fight(perso, display_perso, monster, display_monster, atk_perso_2) == 0:
                            atk_perso_2_delay = atk_perso_2["delay"]
                            atk_perso_1_delay = max(atk_perso_1_delay, 1)
                            state = "Monster"
                            move_left = monster.mvt
                            self.button_continue.set_state(2)
                            self.button_comp_1.set_state(2)
                            self.button_comp_2.set_state(2)
                            atk_monster_delay = max(atk_monster_delay - 1, 0)
                            atk_perso_1_delay = max(atk_perso_1_delay - 1, 0)
                            atk_perso_2_delay = max(atk_perso_2_delay - 1, 0)
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
            # Affichage
            self.maps.render(self.window, [display_perso, display_monster])
            self.button_save.render(self.window)
            self.button_comp_1.render(self.window)
            self.button_comp_2.render(self.window)
            self.button_continue.render(self.window)
            self.window.blit(self.texture_cursor, self.cursor_coord)
            pygame.display.update()


# Fonction qui déplace un sprite dans une direction donné en vérifiant si l'on peut aller sur la case de déstination
def move_sprite(maps, sprite, direction):
    """

    :param maps: attribut étant la carte
    :param sprite: attribut étant la case qu'on souhaite déplacer
    :param direction: attribut étant la direction qu'on souhaite prendre (en haut, à droite, ...)
    :return: un booléen (true or false) en fonction de si la sprite destination est marchable ou non
    """
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
    """

    :param s1: attribut étant la sprite qu'on veut comparer à s2
    :param s2: attribut étant une sprite qu'on compare à s1
    :return: retourne le nombre de sprite (cases) qu'il y a entre s1 et s2
    """
    if s1.location[2] != s2.location[2]:
        return -1
    else:
        return math.sqrt(math.pow(s1.location[0]-s2.location[0], 2) + math.pow(s1.location[1]-s2.location[1], 2))


# Fonction qui gère l'attaque
#  -1 si erreur, 0 sinon
def fight(atk, display_atk, target, display_target, atk_type):
    if atk_type["range"] == [-1, -1] or atk_type["range"][0] <= \
            dist(display_atk, display_target) <= atk_type["range"][1]:
        target.pv -= max(atk.atk * atk_type["atk ratio"] - target.defense, 0)
        for element in atk_type["special effect"]:
            pass
        return 0
    else:
        return -1


# Fonction qui fait se déplacer le monstre vers le joueur
# -1 si erreur, 0 si dans la target_dist, 1 si à boucher
def move_forward_player(maps, monster_, player, target_dist):
    if monster_.location[2] == player.location[2]:
        dir_set = ["right", "up", "left", "down"]  # right 0+, up 1-
        d0 = monster_.location[0] - player.location[0]
        d1 = monster_.location[1] - player.location[1]
        dir0 = "0" if d0 > d1 else "1"
        dir1 = 1
        if target_dist[0] <= dist(monster_, player) <= target_dist[1]:
            return 0
        elif target_dist[0] > dist(monster_, player):
            if dir0 == "0":
                if d1 < 0:
                    dir1 = 1
                else:
                    dir1 = 3
            elif dir0 == "1":
                if d1 < 0:
                    dir1 = 2
                else:
                    dir1 = 0
        elif target_dist[1] < dist(monster_, player):
            if dir0 == "0":
                if d0 == 0:
                    if d1 == 0:
                        return 0
                    if d1 < 0:
                        dir1 = 3
                    elif d1 > 0:
                        dir1 = 1
                elif d0 < 0:
                    dir1 = 0
                elif d0 > 0:
                    dir1 = 2
            elif dir0 == "1":
                if d1 == 0:
                    if d0 == 0:
                        return 0
                    elif d0 < 0:
                        dir1 = 0
                    elif d0 > 0:
                        dir1 = 2
                if d1 < 0:
                    dir1 = 3
                elif d1 > 0:
                    dir1 = 1
        have_mov = False
        i = 0
        while not have_mov and i < 4:
            if move_sprite(maps, monster_, dir_set[(dir1 + i) % 4]):
                have_mov = True
            else:
                i += 1
        if have_mov:
            return 1
        else:
            return -1
    else:
        return -1
