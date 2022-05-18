import pygame
import os
import button
import text_render
# TODO penser à changer le 'save.txt' en 'save.json'


# Classe pour l'écran de menu
# Reste dans la classe jusqu'à changement d'écran
# Revoie l'écran à charger ou "exit"
class Menu:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        self.text_font = pygame.font.Font("Game_font.TTF", 72)

        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Background 2.png")
        # Chargement des boutons
        self.button_continue = button.Button(
            [self.setting.screensize[0] * 1 / 5, self.setting.screensize[1] * 2 / 5],
            3,
            0 if os.path.exists("save.txt") else 2,
            ["Texture/Button up 2.png", "Texture/Button down 2.png", "Texture/Button gray 2.png"],
            self.button_font,
            ["Continue", "Continue", "Continue"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.button_new_game = button.Button(
            [self.setting.screensize[0] * 1 / 5, self.setting.screensize[1] * 4 / 5],
            2,
            0,
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
            self.button_font,
            ["New Game", "New Game"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.button_setting = button.Button(
            [self.setting.screensize[0] * 4 / 5, self.setting.screensize[1] * 2 / 5],
            2,
            0,
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
            self.button_font,
            ["Settings", "Settings"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        self.button_exit = button.Button(
            [self.setting.screensize[0] * 4/5, self.setting.screensize[1] * 4 / 5],
            2,
            0,
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
            self.button_font,
            ["Exit", "Exit"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Création de texte
        self.Text = text_render.Text(
            self.setting,
            [self.setting.screensize[0] / 2, self.setting.screensize[1] / 5],
            self.text_font,
            "Game of the programmation project ",
            pygame.Color("#0080ff"),
        )
        # Curseur
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objets
        self.cursor_coord = (0, 0)

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
                        self.button_continue.set_state(2)
                    # regarde si la souris est sur le bouton continue
                    elif self.button_continue.is_coord_on(self.cursor_coord):
                        self.button_continue.set_state(1)
                    else:
                        self.button_continue.set_state(0)
                    # regarde si la souris est sur le bouton new game
                    if self.button_new_game.is_coord_on(self.cursor_coord):
                        self.button_new_game.set_state(1)
                    else:
                        self.button_new_game.set_state(0)
                    # regarde si la souris est sur le bouton setting
                    if self.button_setting.is_coord_on(self.cursor_coord):
                        self.button_setting.set_state(1)
                    else:
                        self.button_setting.set_state(0)
                    # regarde si la souris est sur le bouton exit
                    if self.button_exit.is_coord_on(self.cursor_coord):
                        self.button_exit.set_state(1)
                    else:
                        self.button_exit.set_state(0)

                # Si Click de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_continue.state == 1:
                        return "game"
                    if self.button_new_game.state == 1:
                        if not os.path.exists("save.txt"):
                            return "create"
                        else:
                            return "warning"
                    if self.button_setting.state == 1:
                        return "paramètre"
                    if self.button_exit.state == 1:
                        return "exit"

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage de texte
            self.Text.render(self.window)
            # Affichage des boutons
            self.button_continue.render(self.window)
            self.button_new_game.render(self.window)
            self.button_setting.render(self.window)
            self.button_exit.render(self.window)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()
