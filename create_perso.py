import pygame
import os
import button
import text_render
import classe
import json


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
        self.texture_background = self.setting.get_texture("Texture/Background 2.png")
        # Bouton pour continuer
        self.button_continue = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] * 3 / 4],
            2,
            0,
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
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
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
            self.button_font,
            ["Back", "Back"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Message avertissement
        self.Text = text_render.Text(
            self.setting,
            [self.setting.screensize[0] / 2, self.setting.screensize[1] / 5],
            self.text_font,
            "Attention si vous continuez, vous allez\nperdre votre sauvegarde !!",
            pygame.Color("#FF0000"),
        )
        # chargement du curseur
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
            # Affichage de texte
            self.Text.render(self.window)
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
        self.input_box_font = pygame.font.Font("Game_font.TTF", 30)
        self.text_font = pygame.font.Font("Game_font.TTF", 72)
        # Chargement des textures
        self.texture_background = self.setting.get_texture("Texture/Background CreatePerso.png")
        # Chargement des données des classes
        # Ouverture du fichier
        with open("classe.json") as data:
            # Ouverture du fichier à l'aide du décodeur json et décoder classe.decode
            z = json.load(data, object_hook=classe.decode)
        # Adaptation de la texture à la tailles de l'écran
        for element in z:
            element.texture["face M"] = self.setting.adapt_texture(element.texture["face M"])
            element.texture["face F"] = self.setting.adapt_texture(element.texture["face F"])
        # sert à désigner chaque classe par son nom, non un numéro (pas forcément fixe)
        self.classe_list = {z[i].classe_name: z[i] for i in range(z.__len__())}
        # Initialisation des variables de sélection
        self.gender = "M"
        self.classe_name = "Guerrier"

        # Chargement bouton Man
        self.button_man = button.Button(
            [self.setting.screensize[0] * 8.75 / 10, self.setting.screensize[1] * 4 / 10],
            3,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png", "Texture/Button selectionned.png"],
            self.button_font,
            ["Man", "Man", "Man"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Chargement bouton Woman
        self.button_woman = button.Button(
            [self.setting.screensize[0] * 8.75 / 10, self.setting.screensize[1] * 6 / 10],
            3,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png", "Texture/Button selectionned.png"],
            self.button_font,
            ["Woman", "Woman", "Woman"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
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
            [self.setting.screensize[0] * 1.25 / 10, self.setting.screensize[1] * 4 / 10],
            3,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png", "Texture/Button selectionned.png"],
            self.button_font,
            ["Guerrier", "Guerrier", "Guerrier"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # bouton pour la classe mage
        self.button_mage = button.Button(
            [self.setting.screensize[0] * 1.25 / 10, self.setting.screensize[1] * 6 / 10],
            3,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png", "Texture/Button selectionned.png"],
            self.button_font,
            ["Mage", "Mage", "Mage"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # bouton pour la classe voleur
        self.button_voleur = button.Button(
            [self.setting.screensize[0] * 1.25 / 10, self.setting.screensize[1] * 8 / 10],
            3,
            0,
            ["Texture/Button up choice.png", "Texture/Button down choice.png", "Texture/Button selectionned.png"],
            self.button_font,
            ["Voleur", "Voleur", "Voleur"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # création de l'espace pour entrer son pseudo
        self.input_box = button.Button(
            [self.setting.screensize[0] * 8.75 / 10, self.setting.screensize[1] * 8 / 10],
            2,
            0,
            ["Texture/Button up 2.png", "Texture/Button down 2.png"],
            self.input_box_font,
            ["Enter name", "Enter name"],
            [pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Création du bouton de confirmation
        self.button_confirm = button.Button(
            [self.setting.screensize[0]/2, self.setting.screensize[1] * 8 / 10],
            3,
            2,
            ["Texture/Button up 2.png", "Texture/Button down 2.png", "Texture/Button gray 2.png"],
            self.button_font,
            ["Confirm", "Confirm", "Need a name"],
            [pygame.Color("#000000"), pygame.Color("#000000"), pygame.Color("#000000")],
            self.setting
        )
        # Curseur
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objects
        self.cursor_coord = (0, 0)
        # nombre de caractère max pour l'input box
        self.input_box_max_length = 16
        # Boolean pour l'inputbox
        self.input_box_input = False
        self.input_box_text = ""

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
                    #bouton homme
                    if self.button_man.is_coord_on(self.cursor_coord):
                        # change l'état du bouton si la souris est dessus
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
                    # bouton classe guerrier
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
                    # bouton confirm
                    if self.input_box_text.__len__() < 3:
                        self.button_confirm.set_state(2)
                    elif self.button_confirm.is_coord_on(self.cursor_coord):
                        self.button_confirm.set_state(1)
                    else:
                        self.button_confirm.set_state(0)

                # Si Click de la souris sur les différents bouton,
                # on verifie ou est la souris pour activer le bon bouton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_man.state == 1:
                        self.gender = "M"
                    if self.button_woman.state == 1:
                        self.gender = "F"
                    if self.button_back.state == 1:
                        return "menu"
                    if self.button_guerrier.state == 1:
                        self.classe_name = "Guerrier"
                    if self.button_mage.state == 1:
                        self.classe_name = "Mage"
                    if self.button_voleur.state == 1:
                        self.classe_name = "Voleur"
                    # check clic sur l'input box
                    coord = event.pos
                    if self.input_box.is_coord_on(coord):
                        # si il y a un clique sur l'input box, autorise l'entrée de caractère
                        self.input_box_input = True
                        self.input_box.set_state(1)
                    else:
                        # sinon l'entrée de caractère dans l'input box n'est pas activée
                        self.input_box_input = False
                        self.input_box.set_state(0)
                # si l'entrée dans l'input box est activée et qu'on apuie sur une touche, permet l'entrée de caract
                elif event.type == pygame.KEYDOWN and self.input_box_input:
                    # Touche enter, echap, tab
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                        self.input_box_input = False
                        self.input_box.set_state(0)
                    # Touche effacer
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_box_text = self.input_box_text[:-1]
                    # Touche suppr
                    elif event.key == pygame.K_DELETE:
                        self.input_box_text = ""
                    # Autre touche si text dans la limite de longueur (16)
                    elif self.input_box_text.__len__() < self.input_box_max_length:
                        # Ajout du charactère
                        self.input_box_text += event.unicode
                    # Actualisation du text sur le bouton
                    self.input_box.change_text(
                        [self.input_box_text, self.input_box_text]
                        if self.input_box_text.__len__() != 0
                        else ["Enter name", "Enter name"])
                    # Actualisation du bouton confirm
                    if self.input_box_text.__len__() < 3:
                        self.button_confirm.set_state(2)
                    else:
                        if self.button_confirm.is_coord_on(self.cursor_coord):
                            self.button_confirm.set_state(1)
                        else:
                            self.button_confirm.set_state(0)

                # Affichage des boutons selectionnés
                if self.gender == "M":
                    self.button_man.set_state(2)
                if self.gender == "F":
                    self.button_woman.set_state(2)
                if self.classe_name == "Guerrier":
                    self.button_guerrier.set_state(2)
                if self.classe_name == "Mage":
                    self.button_mage.set_state(2)
                if self.classe_name == "Voleur":
                    self.button_voleur.set_state(2)

            # Affichage du fond d'écran
            self.window.blit(self.texture_background, (0, 0))

            # affichage de l'aperçu du personnage sélectionné
            texture_name = "face M" if self.gender == "M" else "face F"
            texture = self.classe_list[self.classe_name].texture[texture_name]
            # Passage d'une texture de 32*32 en plus grand (facteur 7.5)
            texture = pygame.transform.scale(texture,
                                             [texture.get_width()*8, texture.get_height()*8])
            self.window.blit(texture,
                             [self.setting.screensize[0] / 2 - texture.get_width() / 2,
                              self.setting.screensize[1] / 2 - texture.get_height() / 2])

            # Affichage de texte
            self.Text.render(self.window)
            # Affichage des boutons
            self.button_man.render(self.window)
            self.button_woman.render(self.window)
            self.button_back.render(self.window)
            self.button_guerrier.render(self.window)
            self.button_mage.render(self.window)
            self.button_voleur.render(self.window)
            self.input_box.render(self.window)
            self.button_confirm.render(self.window)
            #  Affichage du curseur
            self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()