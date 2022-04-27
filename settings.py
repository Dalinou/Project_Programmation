import os
import pygame


# Classe de lecture des parametres
class SettingReader:
    def __init__(self):
        self.filename = "setting.txt"
        # Paramètre par défaut
        self.default_screensize = (1344, 704)
        self.default_fps = 120
        # Paremètre
        self.screensize = self.default_screensize
        self.fps = self.default_fps
        if os.path.exists(self.filename):
            self.read_file()
        else:
            print("Setting file does not exist, using default setting")
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
        file.close()

    # écrit le fichier avec les diifférent paramètre
    def write_file(self):
        file = open(self.filename, 'w')
        file.write("screensize: %(1)s, %(2)s\nfps: %(3)s" %
                   {'1': self.screensize[0], '2': self.screensize[1], '3': self.fps})
        file.close()

    # renvoie lit le fichier et renvoie le paramètre demandé
    def get_screensize(self):
        self.read_file()
        return self.screensize

    def get_fps(self):
        self.read_file()
        return self.fps

    # change la valeur du paramètre et réecrit le fichier
    def set_screensize(self, screensize=(1344, 704)):
        self.screensize = screensize
        self.write_file()

    def set_fps(self, fps=120):
        self.fps = fps
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
        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Menu/Background.png")
        # Chargement bouton back
        self.texture_button_back = (
            self.setting.get_texture("Texture/Paramètre/Button Back up.png"),
            self.setting.get_texture("Texture/Paramètre/Button Back down.png"))
        # Chargement bouton sreensize
        self.texture_button_screensize = (
            (self.setting.get_texture("Texture/Paramètre/Button 800_576 up.png"),
             self.setting.get_texture("Texture/Paramètre/Button 800_576 down.png")),
            (self.setting.get_texture("Texture/Paramètre/Button 1024_786 up.png"),
             self.setting.get_texture("Texture/Paramètre/Button 1024_786 down.png")),
            (self.setting.get_texture("Texture/Paramètre/Button 1280_800 up.png"),
             self.setting.get_texture("Texture/Paramètre/Button 1280_800 down.png")),
            (self.setting.get_texture("Texture/Paramètre/Button 1344_704 up.png"),
             self.setting.get_texture("Texture/Paramètre/Button 1344_704 down.png")))
        # Chargement bouton fps
        self.texture_button_fps = (
            (self.setting.get_texture("Texture/Paramètre/Button fps 30 up.png"),
             self.setting.get_texture("Texture/Paramètre/Button fps 30 down.png")),
            (self.setting.get_texture("Texture/Paramètre/Button fps 60 up.png"),
             self.setting.get_texture("Texture/Paramètre/Button fps 60 down.png")),
            (self.setting.get_texture("Texture/Paramètre/Button fps 120 up.png"),
             self.setting.get_texture("Texture/Paramètre/Button fps 120 down.png")))
        # Curseur
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objects
        self.cursor_coord = (0, 0)
        self.button_back_coord = (
            self.setting.screensize[0] / 2 - self.texture_button_back[0].get_width() / 2,
            self.setting.screensize[1] * 3 / 4 - self.texture_button_back[0].get_height() / 2,
        )  # En-bas centré
        self.button_screensize_coord = (
            self.setting.screensize[0] / 4 - self.texture_button_screensize[0][0].get_width() / 2,
            self.setting.screensize[1] / 2 - self.texture_button_screensize[0][0].get_height() / 2,
        )  # Millieu gauche
        self.button_fps_coord = (
            self.setting.screensize[0] * 3 / 4 - self.texture_button_fps[0][0].get_width() / 2,
            self.setting.screensize[1] / 2 - self.texture_button_fps[0][0].get_height() / 2,
        )  # Millieu droite
        # Etat des différents boutons
        self.button_back_state = "up"
        self.button_screensize_state = "up"
        self.button_fps_state = "up"
        # Liste des différentes valeurs pour screen_size et fps
        # Doivent être dans le même ordre que les textures
        self.fps_list = (30, 60, 120)
        self.screensize_list = ((800, 576), (1024, 786), (1280, 800), (1344, 704))

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
                    # regarde si la souris est sur le boutton
                    if self.button_back_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_back_coord[0] + self.texture_button_back[0].get_width() and \
                            self.button_back_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_back_coord[1] + self.texture_button_back[0].get_height():
                        self.button_back_state = "down"
                    else:
                        self.button_back_state = "up"
                    if self.button_screensize_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_screensize_coord[0] + self.texture_button_screensize[0][0].get_width() and \
                            self.button_screensize_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_screensize_coord[1] + self.texture_button_screensize[0][0].get_height():
                        self.button_screensize_state = "down"
                    else:
                        self.button_screensize_state = "up"
                    if self.button_fps_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_fps_coord[0] + self.texture_button_fps[0][0].get_width() and \
                            self.button_fps_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_fps_coord[1] + self.texture_button_fps[0][0].get_height():
                        self.button_fps_state = "down"
                    else:
                        self.button_fps_state = "up"
                # Si click de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back_state == "down":
                        return "menu"
                    if self.button_screensize_state == "down":
                        i = -1
                        for _ in range(0, self.screensize_list.__len__()):
                            if self.screensize_list[_] == self.setting.screensize:
                                i = _
                                break
                        if i != -1:
                            self.setting.set_screensize(self.screensize_list[(i + 1) % 4])
                        else:
                            self.setting.set_screensize(self.setting.default_screensize)
                        self.window = pygame.display.set_mode(self.setting.screensize)
                        return "paramètre"
                    if self.button_fps_state == "down":
                        i = -1
                        for _ in range(0, self.fps_list.__len__()):
                            if self.fps_list[_] == self.setting.fps:
                                i = _
                                break
                        if i != -1:
                            self.setting.set_fps(self.fps_list[(i+1) % 3])
                        else:
                            self.setting.set_fps(self.setting.default_fps)

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage des boutons en fonction de leur état
            if self.button_back_state == "up":
                self.window.blit(self.texture_button_back[0], self.button_back_coord)
            elif self.button_back_state == "down":
                self.window.blit(self.texture_button_back[1], self.button_back_coord)
            i = -1
            for _ in range(0, self.screensize_list.__len__()):
                if self.screensize_list[_] == self.setting.screensize:
                    i = _
                    break
            if self.button_screensize_state == "up":
                self.window.blit(self.texture_button_screensize[i][0], self.button_screensize_coord)
            elif self.button_screensize_state == "down":
                self.window.blit(self.texture_button_screensize[i][1], self.button_screensize_coord)
            i = -1
            for _ in range(0, self.fps_list.__len__()):
                if self.fps_list[_] == self.setting.fps:
                    i = _
                    break
            if self.button_fps_state == "up":
                self.window.blit(self.texture_button_fps[i][0], self.button_fps_coord)
            elif self.button_fps_state == "down":
                self.window.blit(self.texture_button_fps[i][1], self.button_fps_coord)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()
