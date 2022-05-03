import os
import pygame
import button
import text_render


# Classe de lecture des parametres
class SettingReader:
    def __init__(self):
        self.filename = "setting.txt"
        # Paramètre par défaut
        self.fullscreen_resolution = [
            pygame.display.set_mode([0, 0], pygame.FULLSCREEN).get_width(),
            pygame.display.set_mode([0, 0], pygame.FULLSCREEN).get_height()]
        self.default_screensize = [1344, 704]
        self.default_fps = 120
        self.default_fullscreen = False
        # Paremètre
        self.screensize = self.default_screensize
        self.fps = self.default_fps
        self.fullscreen = self.default_fullscreen
        if os.path.exists(self.filename):
            self.read_file()
        else:
            self.write_file()

    # lis le fichier et extrait les différents paramètre
    def read_file(self):
        file = open(self.filename, 'r')
        data = file.read().split('\n')
        for d in data:
            if d.split(':')[0] == "screensize":
                self.screensize = [
                    int(d.split(':')[1].split(',')[0]),
                    int(d.split(':')[1].split(',')[1])
                ]
            elif d.split(':')[0] == "fps":
                self.fps = int(d.split(':')[1])
            elif d.split(':')[0] == "fullscreen":
                self.fullscreen = d.split(':')[1] == " True"
        if self.fullscreen:
            self.screensize = self.fullscreen_resolution
        file.close()

    # écrit le fichier avec les diifférent paramètre
    def write_file(self):
        file = open(self.filename, 'w')
        file.write("screensize: %(1)s, %(2)s\nfps: %(3)s\nfullscreen: %(4)s" %
                   {'1': self.screensize[0], '2': self.screensize[1], '3': self.fps, '4': self.fullscreen})
        file.close()

    # change la valeur du paramètre et réecrit le fichier
    def set_screensize(self, screensize=(1344, 704)):
        self.screensize = screensize
        self.write_file()

    def set_fps(self, fps=120):
        self.fps = fps
        self.write_file()

    def set_fullscreen(self, fullscreen=False):
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.screensize = self.fullscreen_resolution
        else:
            self.screensize = self.default_screensize
        self.write_file()

    # Charge la texture et l'adapte à la taille de l'écran
    def get_texture(self, filename):
        texture = pygame.image.load(filename)
        newsize = (
            self.screensize[0] * texture.get_width() / self.default_screensize[0],
            self.screensize[1] * texture.get_height() / self.default_screensize[1])
        return pygame.transform.scale(texture, newsize)


class SettingScreen:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        self.text_font = pygame.font.Font("Game_font.TTF", 72)

        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Setting background.png")
        # Chargement bouton back
        self.button_back = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] * 4 / 5],
            2,
            0,
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
            self.button_font,
            ["Back", "Back"],
            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")],
            self.setting
        )
        # Chargement bouton sreensize
        self.button_screensize = button.Button(
            [self.setting.screensize[0] / 4, self.setting.screensize[1] * 2 / 5],
            2,
            0,
            ["Texture/Button up setting.png", "Texture/Button down setting.png"],
            self.button_font,
            ["%(1)s*%(2)s" % {'1': self.setting.screensize[0], '2': self.setting.screensize[1]},
             "%(1)s*%(2)s" % {'1': self.setting.screensize[0], '2': self.setting.screensize[1]}],
            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")],
            self.setting
        )
        # Chargement bouton fps
        self.button_fps = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] * 2 / 5],
            2,
            0,
            ["Texture/Button up setting.png", "Texture/Button down setting.png"],
            self.button_font,
            ["Fps: %s" % self.setting.fps, "Fps: %s" % self.setting.fps],
            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")],
            self.setting
        )
        # Chargement bouton fullscreen
        self.button_fullscreen = button.Button(
            [self.setting.screensize[0] * 3 / 4, self.setting.screensize[1] * 2 / 5],
            2,
            0,
            ["Texture/Button up setting.png", "Texture/Button down setting.png"],
            self.button_font,
            ["Fullscreen: On", "Fullscreen: On"] if self.setting.fullscreen else ["Fullscreen: Off", "Fullscreen: Off"],
            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")],
            self.setting
        )
        # Curseur
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objects
        self.cursor_coord = (0, 0)
        # Liste des différentes valeurs pour screen_size et fps
        # Doivent être dans le même ordre que les textures
        self.fps_list = (30, 60, 120)
        self.screensize_list = ([800, 576], [1024, 786], [1280, 800], [1344, 704])

    def gameloop(self):
        while True:
            # clock.tick pour respecter le fps
            self.clock.tick(self.setting.fps)
            for event in pygame.event.get():
                # Lecture des entrées et interprétation
                # Si alt-f4 ou croix rouge
                if event.type == pygame.QUIT:
                    return "exit"
                # Si mouvement de la souris
                if event.type == pygame.MOUSEMOTION:
                    # récupération des coordonnées de la souris
                    self.cursor_coord = event.pos
                    # regarde si la souris est sur le bouton
                    if self.button_back.is_coord_on(self.cursor_coord):
                        self.button_back.set_state(1)
                    else:
                        self.button_back.set_state(0)
                    if self.button_screensize.is_coord_on(self.cursor_coord):
                        self.button_screensize.set_state(1)
                    else:
                        self.button_screensize.set_state(0)
                    if self.button_fps.is_coord_on(self.cursor_coord):
                        self.button_fps.set_state(1)
                    else:
                        self.button_fps.set_state(0)
                    if self.button_fullscreen.is_coord_on(self.cursor_coord):
                        self.button_fullscreen.set_state(1)
                    else:
                        self.button_fullscreen.set_state(0)
                # Si click de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back.state == 1:
                        return "menu"
                    if self.button_screensize.state == 1:
                        if self.setting.fullscreen:
                            self.setting.set_fullscreen(False)
                            self.button_fullscreen.change_text(
                                self.button_font,
                                ["Fullscreen: Off", "Fullscreen: Off"],
                                [pygame.Color("#CB4F00"), pygame.Color("#FE6400")]
                            )
                        else:
                            i = -1
                            for _ in range(0, self.screensize_list.__len__()):
                                if self.screensize_list[_] == self.setting.screensize:
                                    i = _
                                    break
                            if i != -1:
                                self.setting.set_screensize(self.screensize_list[(i + 1) % 4])
                            else:
                                self.setting.set_screensize(self.setting.default_screensize)
                        self.button_screensize.change_text(
                            self.button_font,
                            ["%(1)s*%(2)s" % {'1': self.setting.screensize[0],
                                                          '2': self.setting.screensize[1]},
                             "%(1)s*%(2)s" % {'1': self.setting.screensize[0],
                                                          '2': self.setting.screensize[1]}],
                            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")]
                        )
                        self.window = pygame.display.set_mode(self.setting.screensize)
                        return "paramètre"
                    if self.button_fps.state == 1:
                        i = -1
                        for _ in range(0, self.fps_list.__len__()):
                            if self.fps_list[_] == self.setting.fps:
                                i = _
                                break
                        if i != -1:
                            self.setting.set_fps(self.fps_list[(i+1) % 3])
                        else:
                            self.setting.set_fps(self.setting.default_fps)
                        self.button_fps.change_text(
                            self.button_font,
                            ["Fps: %s" % self.setting.fps, "Fps: %s" % self.setting.fps],
                            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")]
                        )
                    if self.button_fullscreen.state == 1:
                        self.setting.set_fullscreen(not self.setting.fullscreen)
                        if self.setting.fullscreen:
                            self.window = pygame.display.set_mode(self.setting.screensize, pygame.FULLSCREEN)
                        else:
                            self.window = pygame.display.set_mode(self.setting.screensize)
                        self.button_fullscreen.change_text(
                            self.button_font,
                            ["Fullscreen: On", "Fullscreen: On"] if self.setting.fullscreen else ["Fullscreen: Off",
                                                                                                  "Fullscreen: Off"],
                            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")]
                        )
                        self.button_screensize.change_text(
                            self.button_font,
                            ["%(1)s*%(2)s" % {'1': self.setting.screensize[0],
                                              '2': self.setting.screensize[1]},
                             "%(1)s*%(2)s" % {'1': self.setting.screensize[0],
                                              '2': self.setting.screensize[1]}],
                            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")]
                        )
                        return "paramètre"

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage de texte
            text_render.render_text(
                self.window,
                [self.setting.screensize[0] / 2, self.setting.screensize[1] / 5],
                self.text_font,
                "Settings",
                pygame.Color("#36B500"),
                screensize_adaption=True, screensize=self.setting.screensize
            )
            # Affichage des boutons en fonction de leur état
            self.button_back.render(self.window)
            self.button_screensize.render(self.window)
            self.button_fps.render(self.window)
            self.button_fullscreen.render(self.window)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()
