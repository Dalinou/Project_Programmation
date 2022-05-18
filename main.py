import pygame
import menu
import settings
import create_perso

# initiation de pygame
pygame.font.init()
pygame.init()
# Mise en invisible du curseur de windows
pygame.mouse.set_visible(False)
# changement du nom de la fenêtre et de l'icone
pygame.display.set_caption("Nom du jeu")
pygame.display.set_icon(pygame.image.load("Texture/Game Icon.png"))

# Paramètre
setting = settings.SettingReader()

# Création de la fenetre
if setting.fullscreen:
    window = pygame.display.set_mode(setting.fullscreen_resolution, pygame.FULLSCREEN)
else:
    window = pygame.display.set_mode(setting.screensize)
clock = pygame.time.Clock()

# Ecran à affiché / Etat du jeu
state = "menu"

while state != "exit":
    setting.read_file()
    # regarde l'état du jeu
    if state == "menu":
        screen = menu.Menu(window, clock, setting)
        state = screen.gameloop()
    elif state == "create":
        screen = create_perso.CreatePerso(window, clock, setting)
        state = screen.gameloop()
    elif state == "warning":
        screen = create_perso.CreateWarning(window, clock, setting)
        state = screen.gameloop()
    elif state == "paramètre":
        screen = settings.SettingScreen(window, clock, setting)
        state = screen.gameloop()
    else:
        state = "menu"
