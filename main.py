import pygame
import menu
import setting_reader

# Paramêtre
setting = setting_reader.SettingReader()

# Création de la fenetre
window = pygame.display.set_mode(setting.screen_size)
clock = pygame.time.Clock()


# création des différents  écran
menu_screen = menu.Menu(window, clock, setting)

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
