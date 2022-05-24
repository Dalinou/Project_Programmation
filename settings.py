import os
import pygame
import button
import text_render
import json


# Classe de lecture/écriture des parametres depuis le fichier de paramètrage setting.json
class SettingReader:
    def __init__(self):
        # Nom du fichier
        self.filename = "setting.json"
        # Récupère les coordonnées  du plein écran
        self.fullscreen_resolution = [
            pygame.display.set_mode([0, 0], pygame.FULLSCREEN).get_width(),
            pygame.display.set_mode([0, 0], pygame.FULLSCREEN).get_height()]
        # Paramètre par défaut
        self.default_screensize = [1344, 704]
        self.default_fps = 120
        self.default_fullscreen = False
        # Paremètre
        self.screensize = self.default_screensize
        self.fps = self.default_fps
        self.fullscreen = self.default_fullscreen
        # Vérifie l'existance du fichier de paramètre puis lit ou écrit le fichier
        if os.path.exists(self.filename):
            self.read_file()
        else:
            self.write_file()

    # lis le fichier .json et en ressort les données de paramètrage
    def read_file(self):
        # Charge le contenuedu fichier et le mets dans un tableau
        data = json.load(open(self.filename))
        # Récupère chaque paramètre ou mets les valeurs par defaut si le paramètre n'est pas présicé
        self.screensize = data["screensize"] if "screensize" in data else self.default_screensize
        self.fps = data["fps"] if "fps" in data else self.default_fps
        self.fullscreen = data["fullscreen"] if "fullscreen" in data else self.default_fullscreen
        # Réécrit le fichier pour mettre les valeurs par default si besoin
        self.write_file()

    # écrit le fichier .json avec les données de paramètrage
    def write_file(self):
        # Crée un tableau avec le bon format de tableau
        data = {
            "screensize": self.screensize,
            "fps": self.fps,
            "fullscreen": self.fullscreen
        }
        # Ecrit le fichier en format json
        # json.dumps sert à transformé le tableau en chaine de caractère, il fait aussi de l'indentation
        open(self.filename, 'w').write(json.dumps(data, indent=2, sort_keys=True))

    # change la valeur d'un des paramètres et change le fichier .json
    def set_screensize(self, screensize=(1344, 704)):
        self.screensize = screensize
        self.write_file()

    def set_fps(self, fps=120):
        self.fps = fps
        self.write_file()

    def set_fullscreen(self, fullscreen=False):
        self.fullscreen = fullscreen
        # fullscreen doit aussi change la resolution de l'écran
        if self.fullscreen:
            # resolution du plein écran si en plein écran
            self.screensize = self.fullscreen_resolution
        else:
            # sinon résolution par défault
            self.screensize = self.default_screensize
        self.write_file()

    # Charge la texture et l'adapte à la taille de l'écran
    def get_texture(self, filename, adapt_texture=True):
        # chargement de la texture
        texture = pygame.image.load(filename)
        # Change la résolution de la texture et la renvoie
        return self.adapt_texture(texture) if adapt_texture else texture

    # Change la résolution de la texture en fonction de la résolution de l'écran
    def adapt_texture(self, texture):
        # Calcule la nouvelle résolution en fct de la résolution de l'écran
        newsize = (
            self.screensize[0] * texture.get_width() / self.default_screensize[0],
            self.screensize[1] * texture.get_height() / self.default_screensize[1])
        # Renvoie la texture
        # pygame.transform.scale sert à mettre la texture à une nouvelle resolution
        return pygame.transform.scale(texture, newsize)



class SettingScreen:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        # Charge les différente police de charactère
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        self.text_font = pygame.font.Font("Game_font.TTF", 72)
        # Chargement de la texture du fond d'écran avec redimentionnement
        self.texture_background = self.setting.get_texture("Texture/Setting background.png")
        # Chargement bouton back
        self.button_back = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] * 4 / 5],
            2,
            0,
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
            self.button_font,
            ["Back", "Back"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
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
            [pygame.Color("#FF7F00"), pygame.Color("#FF7F00")],
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
            [pygame.Color("#FF7F00"), pygame.Color("#FF7F00")],
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
            [pygame.Color("#FF7F00"), pygame.Color("#FF7F00")],
            self.setting
        )
        # Charge la texture du curseur sans redimentionnement
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objets
        self.cursor_coord = (0, 0)
        # Liste des différentes valeurs pour screen_size et fps
        self.fps_list = (30, 60, 120)
        self.screensize_list = ([800, 576], [1024, 786], [1280, 800], [1344, 704])
        # Création du texte
        self.text = text_render.Text(
            self.setting,
            [self.setting.screensize[0] / 2, self.setting.screensize[1] / 5],
            self.text_font,
            "Settings",
            pygame.Color("#4C0099"),
        )

    # boucle de l'écran
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
                    # regarde si la souris est sur le bouton et le mets en fct dans un état
                    # Bouton back
                    if self.button_back.is_coord_on(self.cursor_coord):
                        self.button_back.set_state(1)
                    else:
                        self.button_back.set_state(0)
                    # Bouton screensize
                    if self.button_screensize.is_coord_on(self.cursor_coord):
                        self.button_screensize.set_state(1)
                    else:
                        self.button_screensize.set_state(0)
                    # Bouton fps
                    if self.button_fps.is_coord_on(self.cursor_coord):
                        self.button_fps.set_state(1)
                    else:
                        self.button_fps.set_state(0)
                    # Bouton fullscreen
                    if self.button_fullscreen.is_coord_on(self.cursor_coord):
                        self.button_fullscreen.set_state(1)
                    else:
                        self.button_fullscreen.set_state(0)
                # Si click de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Regarde si chaque bouton est dans l'état 1 ( curseur dessus)
                    # Bouton back => retour au menu principal
                    if self.button_back.state == 1:
                        return "menu"
                    # Bouton screensize => change la resolution et recharge l'écran de paramètrage
                    if self.button_screensize.state == 1:
                        # Si en plein écran
                        if self.setting.fullscreen:
                            # quitte le mode plein écran
                            self.setting.set_fullscreen(False)
                        else:
                            # Regarde quel est la resolution actuel
                            i = -1
                            for _ in range(0, self.screensize_list.__len__()):
                                if self.screensize_list[_] == self.setting.screensize:
                                    i = _
                                    break
                            # mets à l'état suivant si texture dans la liste (mod la longueur de la liste)
                            if i != -1:
                                self.setting.set_screensize(self.screensize_list[(i + 1) %
                                                                                 self.screensize_list.__len__()])
                            # sinon resolution par defaut
                            else:
                                self.setting.set_screensize(self.setting.default_screensize)
                        # change la fenètre
                        self.window = pygame.display.set_mode(self.setting.screensize)
                        # recharge l'écran
                        return "paramètre"
                    # Bouton fps => change les fps et change le texte du bouton
                    if self.button_fps.state == 1:
                        # Regarde quel est le fps  actuel
                        i = -1
                        for _ in range(0, self.fps_list.__len__()):
                            if self.fps_list[_] == self.setting.fps:
                                i = _
                                break
                        # si le fps dans la liste, mets le fps suivant
                        if i != -1:
                            self.setting.set_fps(self.fps_list[(i+1) % self.fps_list.__len__()])
                        # sinon fps par défaut
                        else:
                            self.setting.set_fps(self.setting.default_fps)
                        # Change le texte du bouton
                        self.button_fps.change_text(
                            ["Fps: %s" % self.setting.fps, "Fps: %s" % self.setting.fps],
                        )
                    # Bouton fullscreen => passe en fullscreen et recharge la fenêtre, puis recharge l'écran
                    if self.button_fullscreen.state == 1:
                        # inverse la valeur de fullscreen
                        self.setting.set_fullscreen(not self.setting.fullscreen)
                        # si fullscreen, charge un fenêtre en plein écran
                        if self.setting.fullscreen:
                            self.window = pygame.display.set_mode(self.setting.screensize, pygame.FULLSCREEN)
                        # sinon charge un fenêtre en mode fenêtré
                        else:
                            self.window = pygame.display.set_mode(self.setting.screensize)
                        # recharge l'écran
                        return "paramètre"

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage de texte
            self.text.render(self.window)
            # Affichage des boutons en fonction de leur état
            self.button_back.render(self.window)
            self.button_screensize.render(self.window)
            self.button_fps.render(self.window)
            self.button_fullscreen.render(self.window)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()
