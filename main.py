import pygame
import menu

# Principaux parametre
setting_screensize = (1344, 704)
setting_fps = 120

# Création de la fenetre
window = pygame.display.set_mode(setting_screensize)
clock = pygame.time.Clock()


# création des différents  écran
menu_screen = menu.Menu(setting_screensize, setting_fps)

# Ecran à affiché / Etat du jeu
state = "menu"

while state != "exit":
    # regarde l'état du jeu
    if state == "menu":
        state = menu_screen.gameloop()
        print(state)
    else:
        # retour sur le menu pour l'instant, parti non implémenté
        state = "menu"
