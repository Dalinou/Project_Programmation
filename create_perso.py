import pygame
import os
import button


class CreateWarning:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.font = pygame.font.Font("Game_font.TTF", 48)
        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Background.png")
        # Bouton pour continuer
        self.button_continue = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] * 3 / 4],
            2,
            0,
            ["Texture/Button up.png", "Texture/Button down.png"],
            self.font,
            ["Continue", "Continue"],
            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")],
            screensize_adaption=True, screensize=self.setting.screensize
        )
        # Bouton pour retourner au menu
        self.button_back = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] / 2],
            2,
            0,
            ["Texture/Button up.png", "Texture/Button down.png"],
            self.font,
            ["Back", "Back"],
            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")],
            screensize_adaption=True, screensize=self.setting.screensize
        )
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objets
        self.cursor_coord = (0, 0)

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
                    if self.button_continue.is_coord_on(self.cursor_coord):
                        self.button_continue.set_state(1)
                    else:
                        self.button_continue.set_state(0)
                    # regarde si la souris est sur le bouton pour revenir au menu
                    if self.button_back.is_coord_on(self.cursor_coord):
                        self.button_back.set_state(1)
                    else:
                        self.button_back.set_state(0)
                # gère les cliques de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor_coord = event.pos
                    if self.button_continue.state == 1:
                        # détruit le fichier de sauvegarde
                        os.remove("save.txt")
                        # renvoies la valeur permettant d'aller à l'écran de création de personnage
                        return "create"
                    if self.button_back.state == 1:
                        # renvoies la valeur permettant de retourner au menu
                        return "menu"

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage des boutons en fonction de leur état
            self.button_continue.render(self.window)
            self.button_back.render(self.window)
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
        self.texture_background = self.setting.get_texture("Texture/Menu/Background.png")

    def gameloop(self):
        ...
