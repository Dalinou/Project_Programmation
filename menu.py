import pygame
from pathlib import Path


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
        self.texture_background = pygame.image.load("Texture/Menu/Background.png")
        # Bouton 1 pour continuer sur la partie
        self.texture_button_1_up = pygame.image.load("Texture/Menu/Button 1 up.png")
        self.texture_button_1_down = pygame.image.load("Texture/Menu/Button 1 down.png")
        self.texture_button_1_gray = pygame.image.load("Texture/Menu/Button 1 gray.png")
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différents objects
        self.cursor_coord = (0, 0)
        self.button_1_coord = (
            self.setting.screen_size[0]/2-self.texture_button_1_up.get_width()/2,
            self.setting.screen_size[1]/4-self.texture_button_1_up.get_height()/2,
        )
        # Etat du boutton 1
        self.button_1_state = "up"

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
                    if not Path("save.txt").exists():
                        self.button_1_state = "gray"
                    # regarde si la souris est sur le boutton 1
                    elif self.button_1_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_1_coord[0] + self.texture_button_1_up.get_width() and \
                            self.button_1_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_1_coord[1] + self.texture_button_1_up.get_height():
                        self.button_1_state = "down"
                    else:
                        self.button_1_state = "up"
                # Si Click de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Recupération des coordonnées de la souris
                    self.cursor_coord = event.pos
                    # regarde si une sauvegarde existe
                    if not Path("save.txt").exists():
                        self.button_1_state = "gray"
                    # regarde si la souris est sur le boutton 1
                    elif self.button_1_coord[0] \
                            <= self.cursor_coord[0] \
                            < self.button_1_coord[0] + self.texture_button_1_up.get_width() and \
                            self.button_1_coord[1] \
                            <= self.cursor_coord[1] \
                            < self.button_1_coord[1] + self.texture_button_1_up.get_height():
                        # passe à l'écran suivant --------------------------
                        return "game"
                # Affichage du fond d'écran
                self.window.blit(self.texture_background, (0, 0))
                # Affichage du boutton 1 en fonction de son état
                if self.button_1_state == "up":
                    self.window.blit(self.texture_button_1_up, self.button_1_coord)
                elif self.button_1_state == "down":
                    self.window.blit(self.texture_button_1_down, self.button_1_coord)
                elif self.button_1_state == "gray":
                    self.window.blit(self.texture_button_1_gray, self.button_1_coord)
                #  Affichage du curseur
                self.window.blit(self.texture_cursor, self.cursor_coord)
                self.window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()
