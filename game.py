import pygame.image
import save
import sys
import maps
import button

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
                        dest = self.maps.map[self.perso.location[2]]\
                            .map[self.perso.location[1] - 1 if self.perso.location[1] > 0 else 0][self.perso.location[0]]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            self.perso.location[1] = self.perso.location[1] - 1 if self.perso.location[1] > 0 else 0
                    elif event.key == pygame.K_LEFT:
                        dest = self.maps.map[self.perso.location[2]]\
                            .map[self.perso.location[1]][self.perso.location[0] - 1 if self.perso.location[0] > 0 else 0]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            self.perso.location[0] = self.perso.location[0] - 1 if self.perso.location[0] > 0 else 0
                    elif event.key == pygame.K_DOWN:
                        dest = self.maps.map[self.perso.location[2]]\
                            .map[self.perso.location[1] + 1 if self.perso.location[1] <
                                self.maps.map[self.perso.location[2]].res[1] - 1 else
                                self.maps.map[self.perso.location[2]].res[1] - 1][self.perso.location[0]]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            self.perso.location[1] = self.perso.location[1] + 1 if self.perso.location[1] <\
                                self.maps.map[self.perso.location[2]].res[1] - 1 else\
                                self.maps.map[self.perso.location[2]].res[1] - 1
                    elif event.key == pygame.K_RIGHT:
                        dest = self.maps.map[self.perso.location[2]].map[self.perso.location[1]]\
                            [self.perso.location[0] + 1 if self.perso.location[0] <
                                self.maps.map[self.perso.location[2]].res[0] - 1
                                else self.maps.map[self.perso.location[2]].res[0] - 1]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            self.perso.location[0] = self.perso.location[0] + 1 if self.perso.location[0] <\
                                self.maps.map[self.perso.location[2]].res[0] - 1 \
                                else self.maps.map[self.perso.location[2]].res[0] - 1

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
            ["Up", "Down", "Gray"],
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
        is_comp_use = False
        move_left = perso.mvt
        while True:
            active_disp = display_perso if state == "Player" else display_monster
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
                elif event.type == pygame.KEYDOWN and move_left > 0:
                    # Mouvement de la mire + vérification si tjrs dans la carte
                    if event.key == pygame.K_UP:
                        dest = self.maps.map[active_disp.location[2]] \
                            .map[active_disp.location[1] - 1 if active_disp.location[1] >0 else 0][active_disp.location[0]]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            move_left -= 1
                            active_disp.location[1] = active_disp.location[1] - 1 if active_disp.location[1] > 0 else 0
                    elif event.key == pygame.K_LEFT:
                        dest = self.maps.map[active_disp.location[2]] \
                            .map[active_disp.location[1]][active_disp.location[0] - 1 if active_disp.location[0] > 0 else 0]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            move_left -= 1
                            active_disp.location[0] = active_disp.location[0] - 1 if active_disp.location[0] > 0 else 0
                    elif event.key == pygame.K_DOWN:
                        dest = self.maps.map[active_disp.location[2]] \
                            .map[active_disp.location[1] + 1 if active_disp.location[1] <
                                                            self.maps.map[active_disp.location[2]].res[1] - 1 else
                        self.maps.map[active_disp.location[2]].res[1] - 1][active_disp.location[0]]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            move_left -= 1
                            active_disp.location[1] = active_disp.location[1] + 1 if active_disp.location[1] < \
                                                                             self.maps.map[active_disp.location[2]].res[
                                                                                 1] - 1 else \
                                self.maps.map[active_disp.location[2]].res[1] - 1
                    elif event.key == pygame.K_RIGHT:
                        dest = self.maps.map[active_disp.location[2]].map[active_disp.location[1]] \
                            [active_disp.location[0] + 1 if active_disp.location[0] <
                                                        self.maps.map[active_disp.location[2]].res[0] - 1
                            else self.maps.map[active_disp.location[2]].res[0] - 1]
                        is_walkable = self.maps.tile[dest].is_walkable
                        if is_walkable:
                            move_left -= 1
                            active_disp.location[0] = active_disp.location[0] + 1 if active_disp.location[0] < \
                                                                             self.maps.map[active_disp.location[2]].res[
                                                                                 0] - 1 \
                                else self.maps.map[active_disp.location[2]].res[0] - 1
            self.maps.render(self.window, [display_perso, display_monster])
            self.button_save.render(self.window)
            self.button_comp_1.render(self.window)
            self.button_comp_2.render(self.window)
            self.button_continue.render(self.window)
            self.window.blit(self.texture_cursor, self.cursor_coord)
            pygame.display.update()
