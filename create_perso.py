import pygame
import os


class CreateWarning:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        # Chargement des textures
        self.texture_background = pygame.image.load("Texture/Menu/Background.png")
        # Bouton pour continuer
        self.texture_button_Continue_up = pygame.image.load("Texture/Menu/Button 2 up.png")
        self.texture_button_Continue_down = pygame.image.load("Texture/Menu/Button 2 down.png")
        # Bouton pour retourner au menu
        self.texture_button_Back_up = pygame.image.load("Texture/Menu/Button 3 up.png")
        self.texture_button_Back_down = pygame.image.load("Texture/Menu/Button 3 down.png")
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objets
        self.cursor_coord = (0, 0)
        # bouton pour valider la suppression de la sauvegarde
        self.button_Continue_coord = (
            self.setting.screensize[0] / 2 - self.texture_button_Continue_up.get_width() / 2,
            self.setting.screensize[1] * 3 / 4 - self.texture_button_Continue_up.get_height() / 2,
        )
        # bouton pour annuler et revenir au menu
        self.button_Back_coord = (
            self.setting.screensize[0] / 2 - self.texture_button_Back_up.get_width() / 2,
            self.setting.screensize[1] / 2 - self.texture_button_Back_up.get_height() / 2,
        )
        # défini l'état initial des boutons
        self.button_Continue_state = "up"
        self.button_Back_state = "up"

    def gameloop(self):
        while True:
            self.clock.tick(self.setting.fps)
            for event in pygame.event.get():
                # pour gérer la fermeture du jeu
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEMOTION:
                    # récupération des coordonnées de la souris
                    self.cursor_coord = event.pos
                    # regarde si la souris est sur le bouton pour continuer
                    if self.button_Continue_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_Continue_coord[0] + self.texture_button_Continue_up.get_width() and \
                            self.button_Continue_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_Continue_coord[1] + self.texture_button_Continue_up.get_height():
                        self.button_Continue_state = "down"
                    else:
                        self.button_Continue_state = "up"
                    # regarde si la souris est sur le bouton pour revenir au menu
                    if self.button_Back_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_Back_coord[0] + self.texture_button_Back_up.get_width() and \
                            self.button_Back_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_Back_coord[1] + self.texture_button_Back_up.get_height():
                        self.button_Back_state = "down"
                    else:
                        self.button_Back_state = "up"
                # gère les cliques de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor_coord = event.pos
                    if self.button_Continue_state == "down":
                        # détruit le fichier de sauvegarde
                        os.remove("save.txt")
                        # renvoies la valeur permettant d'aller à l'écran de création de personnage
                        return "create"
                    if self.button_Back_state == "down":
                        # renvoies la valeur permettant de retourner au menu
                        return "menu"

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage des boutons en fonction de leur état
            if self.button_Continue_state == "up":
                self.window.blit(self.texture_button_Continue_up, self.button_Continue_coord)
            elif self.button_Continue_state == "down":
                self.window.blit(self.texture_button_Continue_down, self.button_Continue_coord)
            if self.button_Back_state == "up":
                self.window.blit(self.texture_button_Back_up, self.button_Back_coord)
            elif self.button_Back_state == "down":
                self.window.blit(self.texture_button_Back_down, self.button_Back_coord)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()


class CreatePerso:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        # Chargement des textures
        self.texture_background = pygame.image.load("Texture/Menu/Background.png")

    def gameloop(self):
        ...
