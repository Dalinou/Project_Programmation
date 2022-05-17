import pygame
import os
import button
import text_render


# Ecran de warning si sauvegarde existante
class CreateWarning:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        self.text_font = pygame.font.Font("Game_font.TTF", 72)
        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Background.png")
        # Bouton pour continuer
        self.button_continue = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] * 3 / 4],
            2,
            0,
            ["Texture/Button up.png", "Texture/Button down.png"],
            self.button_font,
            ["Continue", "Continue"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Bouton pour retourner au menu
        self.button_back = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] / 2],
            2,
            0,
            ["Texture/Button up.png", "Texture/Button down.png"],
            self.button_font,
            ["Back", "Back"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
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


# Ecran de création de perso
class CreatePerso:
    def __init__(self, window, clock, setting):
        # Paramètre de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.button_font = pygame.font.Font("Game_font.TTF", 48)
        self.text_font = pygame.font.Font("Game_font.TTF", 72)
        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Background CreatePerso.png")
        # Chargement bouton Man
        self.button_man = button.Button(
            [self.setting.screensize[0] * 1.25 / 10, self.setting.screensize[1] * 4 / 10],
            2,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png"],
            self.button_font,
            ["Man", "Man"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Chargement bouton Woman
        self.button_woman = button.Button(
            [self.setting.screensize[0] * 1.25 / 10, self.setting.screensize[1] * 6 / 10],
            2,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png"],
            self.button_font,
            ["Woman", "Woman"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Chargement bouton back
        self.button_back = button.Button(
            [self.setting.screensize[0] * 1.25 / 15, self.setting.screensize[1] * 1 / 15],
            2,
            0,
            ["Texture/Button Back up.png", "Texture/Button Back down.png"],
            self.button_font,
            ["", ""],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Création de texte
        self.Text = text_render.Text(
            self.setting,
            [self.setting.screensize[0] / 2, self.setting.screensize[1] / 5],
            self.text_font,
            "Création de Personnage",
            pygame.Color("#000000"),
        )
        # bouton pour la classe guerrier
        self.button_guerrier = button.Button(
            [self.setting.screensize[0] * 8.75 / 10, self.setting.screensize[1] * 4 / 10],
            2,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png"],
            self.button_font,
            ["Guerrier", "Guerrier"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # bouton pour la classe mage
        self.button_mage = button.Button(
            [self.setting.screensize[0] * 8.75 / 10, self.setting.screensize[1] * 6 / 10],
            2,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png"],
            self.button_font,
            ["Mage", "Mage"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # bouton pour la classe voleur
        self.button_voleur = button.Button(
            [self.setting.screensize[0] * 8.75 / 10, self.setting.screensize[1] * 8 / 10],
            2,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png"],
            self.button_font,
            ["Voleur", "Voleur"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Curseur
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objects
        self.cursor_coord = (0, 0)

    def gameloop(self):
        # clock.tick pour respecter le fps
        while True:
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
                    if self.button_man.is_coord_on(self.cursor_coord):
                        self.button_man.set_state(1)
                    else:
                        self.button_man.set_state(0)
                    # regarde si la souris est sur le bouton femme
                    if self.button_woman.is_coord_on(self.cursor_coord):
                        self.button_woman.set_state(1)
                    else:
                        self.button_woman.set_state(0)
                    # bouton back pour revenir au menu
                    if self.button_back.is_coord_on(self.cursor_coord):
                        self.button_back.set_state(1)
                    else:
                        self.button_back.set_state(0)
                    #bouton classe guerrier
                    if self.button_guerrier.is_coord_on(self.cursor_coord):
                        self.button_guerrier.set_state(1)
                    else:
                        self.button_guerrier.set_state(0)
                    # bouton classe mage
                    if self.button_mage.is_coord_on(self.cursor_coord):
                        self.button_mage.set_state(1)
                    else:
                        self.button_mage.set_state(0)
                    # bouton classe voleur
                    if self.button_voleur.is_coord_on(self.cursor_coord):
                        self.button_voleur.set_state(1)
                    else:
                        self.button_voleur.set_state(0)

                # Si Click de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_man.state == 1:
                        return "man"
                    if self.button_woman.state == 1:
                        return "woman"
                    if self.button_back.state == 1:
                        return "menu"
                    if self.button_guerrier.state == 1:
                        return "guerrier"
                    if self.button_mage.state == 1:
                        return "mage"
                    if self.button_voleur.state == 1:
                        return "voleur"

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))
            # Affichage de texte
            self.Text.render(self.window)
            # Affichage des boutons
            self.button_man.render(self.window)
            self.button_woman.render(self.window)
            self.button_back.render(self.window)
            self.button_guerrier.render(self.window)
            self.button_mage.render(self.window)
            self.button_voleur.render(self.window)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()