import pygame
import os


# Classe pour l'écran de menu
# Reste dans la classe jusqu'à changement d'écran
# Revoie l'écran à charger ou "exit"
class Menu:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Menu/Background.png")
        # Bouton 1 pour continuer sur la partie
        self.texture_button_1 = (self.setting.get_texture("Texture/Menu/Button 1 up.png"),
                                 self.setting.get_texture("Texture/Menu/Button 1 down.png"),
                                 self.setting.get_texture("Texture/Menu/Button 1 gray.png"))
        # Bouton 2 pour les paramètres
        self.texture_button_2 = (self.setting.get_texture("Texture/Menu/Button 2 up.png"),
                                 self.setting.get_texture("Texture/Menu/Button 2 down.png"))
        # Bouton 3 pour accéder à la création de personnage
        self.texture_button_3 = (self.setting.get_texture("Texture/Menu/Button 3 up.png"),
                                 self.setting.get_texture("Texture/Menu/Button 3 down.png"))
        # Curseur
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objets
        self.cursor_coord = (0, 0)
        self.button_1_coord = (
            self.setting.screensize[0]/2-self.texture_button_1[0].get_width()/2,
            self.setting.screensize[1]/4-self.texture_button_1[0].get_height()/2,
        )  # En haut centré
        self.button_2_coord = (
            self.setting.screensize[0] / 2 - self.texture_button_2[0].get_width() / 2,
            self.setting.screensize[1] / 2 - self.texture_button_2[0].get_height() / 2,
        )  # Au millieu centré
        self.button_3_coord = (
            self.setting.screensize[0] / 2 - self.texture_button_3[0].get_width() / 2,
            self.setting.screensize[1] * 3 / 4 - self.texture_button_3[0].get_height() / 2,
        )  # En bas centré
        # Etat des boutons
        self.button_1_state = "up" if os.path.exists("save.txt") else "gray"
        self.button_2_state = "up"
        self.button_3_state = "up"

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
                    # regarde si une sauvegarde existe
                    if not os.path.exists("save.txt"):
                        self.button_1_state = "gray"
                    # regarde si la souris est sur le boutton 1
                    elif self.button_1_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_1_coord[0] + self.texture_button_1[0].get_width() and \
                            self.button_1_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_1_coord[1] + self.texture_button_1[0].get_height():
                        self.button_1_state = "down"
                    else:
                        self.button_1_state = "up"
                    # regarde si la souris est sur le bouton 2
                    if self.button_2_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_2_coord[0] + self.texture_button_2[0].get_width() and \
                            self.button_2_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_2_coord[1] + self.texture_button_2[0].get_height():
                        self.button_2_state = "down"
                    else:
                        self.button_2_state = "up"
                    # regarde si la souris est sur le bouton 3
                    if self.button_3_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_3_coord[0] + self.texture_button_3[0].get_width() and \
                            self.button_3_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_3_coord[1] + self.texture_button_3[0].get_height():
                        self.button_3_state = "down"
                    else:
                        self.button_3_state = "up"
                # Si Click de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_1_state == "down":
                        return "game"
                    if self.button_2_state == "down":
                        return "paramètre"
                    if self.button_3_state == "down":
                        if not os.path.exists("save.txt"):
                            return "create"
                        else:
                            return "warning"

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage des boutons en fonction de son état
            # Bouton 1
            if self.button_1_state == "up":
                self.window.blit(self.texture_button_1[0], self.button_1_coord)
            elif self.button_1_state == "down":
                self.window.blit(self.texture_button_1[1], self.button_1_coord)
            elif self.button_1_state == "gray":
                self.window.blit(self.texture_button_1[2], self.button_1_coord)
            # Bouton 2
            if self.button_2_state == "up":
                self.window.blit(self.texture_button_2[0], self.button_2_coord)
            elif self.button_2_state == "down":
                self.window.blit(self.texture_button_2[1], self.button_2_coord)
            # Bouton 3
            if self.button_3_state == "up":
                self.window.blit(self.texture_button_3[0], self.button_3_coord)
            elif self.button_3_state == "down":
                self.window.blit(self.texture_button_3[1], self.button_3_coord)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()
