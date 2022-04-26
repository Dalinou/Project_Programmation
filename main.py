import pygame
import menu
import settings
import create_perso

# Paramêtre
setting = setting_reader.SettingReader()

# Création de la fenetre
window = pygame.display.set_mode(setting.screensize)
clock = pygame.time.Clock()

# Ecran à affiché / Etat du jeu
state = "menu"

while state != "exit":
    # regarde l'état du jeu²
    if state == "menu":
        screen = menu.Menu(window, clock, setting)
        state = screen.gameloop()
    elif state == "create":
        state = "menu"
        # state = create.gameloop()
    elif state == "warning":
        screen = create_perso.CreateWarning(window, clock, setting)
        state = screen.gameloop()
    elif state == "paramètre":
        screen = settings.SettingScreen(window, clock, setting)
        state = screen.gameloop()
    else:
        state = "menu"
