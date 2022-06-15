import pygame
import menu
import settings
import create_perso
import game

'''
Projet de Programmation 2022
Auteurs: Braun Gwendal, Rota-Graziosi Othilie, Pataille Arthur

Ce projet est la création d'un jeu en utilisant le langage python avec comme librairie graphique pygame
Le jeu est organisé en plusieurs écrans chacun géré par une classe
Les écrans sont appelés par le main en fonction de l'état du jeu
Les classes écrans sont: menu.Menu, create_perso.CreatePerso, create_perso.CreateWarning, settings.SettingScreen,
game.GameScreen, game.FightScreen, game.GameOver
Les fichier button.py et text_render.py proposent des objects pour faciliter le travail de création d'écran
comme des boutons ou une zone de texte
Il y a aussi une gestion de sauvegarde avec save.py qui comporte trois méthodes:
save.load_save(filename), save.dump_save(filename, in_data),
save.init_save(filename, classe, gender, init_location, name)
La classe settings.SettingReader fait la lecture des paramètres de l'écran
Les classes monster.Monster et personnage. Personnage définit les objects "joueur" du jeu
Enfin maps.py fait la gestion de la carte
Toutes les données sont sauvegardées dans des fichiers en .json
'''
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
    # regarde l'état du jeu et lance la gameloop voulu en fonction de cet etat
    # Fenêtre menu
    if state == "menu":
        screen = menu.Menu(window, clock, setting)
        state = screen.gameloop()
    # Fenêtre création du personnage
    elif state == "create":
        screen = create_perso.CreatePerso(window, clock, setting)
        state = screen.gameloop()
    # Fenêtre warning lorsqu'une sauvegarde existe
    elif state == "warning":
        screen = create_perso.CreateWarning(window, clock, setting)
        state = screen.gameloop()
    # Fenêtre paramètres
    elif state == "paramètre":
        screen = settings.SettingScreen(window, clock, setting)
        state = screen.gameloop()
    # Fenêtre du jeu
    elif state == "game":
        screen = game.GameScreen(window, clock, setting)
        state = screen.gameloop()
    # Fenêtre de fin du jeu si le perso meurt
    elif state == "game_over":
        screen = game.GameOver(window, clock, setting)
        state = screen.gameloop()
    # si l'état pour une raison quelconque a une valeur inconnu, on retourne au menu
    else:
        state = "menu"
