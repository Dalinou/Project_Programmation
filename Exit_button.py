import pygame
import os
import sys
import button


class Exit:
    def __init__(self, window, clock, setting):
        #paramétrage de l'écran
        self.window = window
        self.clock = clock
        self.setting = setting
        self.font = pygame.font.Font("Game_font.TTF", 48)

        #Chargements des textures
        self.texture_background = self.setting.get_texture("Texture/Background.png")

        #button exit
        self.button_exit = button.Button(
            [self.setting.screensize[0] / 2, self.setting.screensize[1] * 3 / 4],
            2,
            0,
            ["Texture/Button up.png", "Texture/Button down.png"],
            self.font,
            ["Exit", "Exit"],
            [pygame.Color("#CB4F00"), pygame.Color("#FE6400")],
            screensize_adaption=True, screensize=self.setting.screensize
        )

    def gameloop(self):
        x = True
        while x:
            # Vérification d'une sauvegarde existante
            if not os.path.exists('save.txt'):
                print("Attention il n'y a pas de sauvegarde !!!")
                # Demande de confirmation si aucune sauvegarde
                print("Êtes-vous sûr de vouloir quitter ? 'y' pour oui / 'n' pour non")
                answer = input()
                if answer == 'y':
                    state = "exit"
                    sys.exit("Vous avez bien quittez le jeu")
                elif answer == 'n':
                    x = False
                else:
                    print("Veuillez répondre 'y' ou 'n'")
            else:
                # Demande de confirmation même si une sauvegarde existe
                print("Voulez-vous vraiment quitter ?")
                answer = input()
                if answer == 'y':
                    state = "exit"
                    sys.exit("Vous avez bien quittez le jeu")
                elif answer == 'n':
                    x = False
                else:
                    print("Veuillez répondre 'y' ou 'n'")

#### Mettre ce qu'il y a au dessus dans menu.py -> gameloop : sur le pygame.QUIT:

#### + rajouter : # regarde si la souris est sur le bouton exit
                    if self.button_exit.is_coord_on(self.cursor_coord):
                        self.button_exit.set_state(1)

                    if self.button_back.state == 1:
                        # renvoies la valeur permettant de quitter
                        return "exit"
