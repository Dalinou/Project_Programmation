import pygame
from pathlib import Path

# Principaux parametre
setting_screensize = (1344, 704)
setting_fps = 120

# Création de la fenetre
window = pygame.display.set_mode(setting_screensize)
clock = pygame.time.Clock()


# Classe pour l'écran de menu
# Reste dans la classe jusqu'à changement d'écran
# Revoie l'écran à charger ou "exit"
class Menu:
    def __init__(self, screensize, fps):
        # Paramêtre de l'écran
        self.screensize = screensize
        self.fps = fps
        # Chargement des textures
        self.texture_background = pygame.image.load("Texture/Menu/Background.png")
        # Bouton 1 pour continuer sur la partie
        self.texture_button_1_up = pygame.image.load("Texture/Menu/Button 1 up.png")
        self.texture_button_1_down = pygame.image.load("Texture/Menu/Button 1 down.png")
        self.texture_button_1_gray = pygame.image.load("Texture/Menu/Button 1 gray.png")
        self.texture_cursor = pygame.image.load("Texture/Cursor.png")
        # Coordonnée des différent object
        self.cursor_coord = (0, 0)
        self.button_1_coord = (
            screensize[0]/2-self.texture_button_1_up.get_width()/2,
            screensize[1]/4-self.texture_button_1_up.get_height()/2,
        )
        # Etat du boutton 1
        self.button_1_state = "up"

    def gameloop(self):
        while True:
            # clock.tick pour respecter le fps entré
            clock.tick(self.fps)
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
                window.blit(self.texture_background, (0, 0))
                # Affichage du boutton 1 en fonction de son état
                if self.button_1_state == "up":
                    window.blit(self.texture_button_1_up, self.button_1_coord)
                elif self.button_1_state == "down":
                    window.blit(self.texture_button_1_down, self.button_1_coord)
                elif self.button_1_state == "gray":
                    window.blit(self.texture_button_1_gray, self.button_1_coord)
                #  Affichage du curseur
                window.blit(self.texture_cursor, self.cursor_coord)
            # Actualisation de l'affichage
            pygame.display.update()


# création des différents  écran
menu = Menu(setting_screensize, setting_fps)

# Ecran à affiché / Etat du jeu
state = "menu"

while state != "exit":
    # regarde l'état du jeu
    if state == "menu":
        state = menu.gameloop()
        print(state)
    else:
        # retour sur le menu pour l'instant, parti non implémenté
        state = "menu"
