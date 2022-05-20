import pygame
import text_render


# Cette classe est une classe qui sert à avoir des boutons, on peut les afficher "render(window)",
# changer le texte, sa couleur, sa position, son état...
class Button:
    def __init__(self, coord, nb_state, init_state, background_filename, font, text, text_color, setting,
                 is_center=True, screensize_adaptation=True):
        # Recupération des variables
        self.nb_state = nb_state
        self.state = init_state
        self.setting = setting
        # Chargement des textures
        self.background_texture = [
            pygame.image.load(background_filename[i]) for i in range(0, self.nb_state)
        ]
        # Adapte la  taille du bouton à la taile de l'écran
        if screensize_adaptation:
            default_screensize = [1344, 704]
            # Pour chaque état
            for i in range(0, nb_state):
                # Changement de la taille de l'image
                self.background_texture[i] = pygame.transform.scale(
                    self.background_texture[i],
                    [
                        self.setting.screensize[0] / default_screensize[0] * self.background_texture[i].get_width(),
                        self.setting.screensize[1] / default_screensize[1] * self.background_texture[i].get_height()
                    ])
        # Centrage du boutton sur les coordonnées
        self.coord = [coord[0] - self.background_texture[0].get_width()/2,
                      coord[1] - self.background_texture[0].get_height()/2] if is_center else coord
        # Calcul des coordonnées du texte
        self.text_coord = [
            self.coord[0] + self.background_texture[self.state].get_width() / 2,
            self.coord[1] + self.background_texture[self.state].get_height() / 2
        ]
        # Création du texte
        self.text = [
            text_render.Text(
                self.setting,
                self.text_coord,
                font,
                text[i],
                text_color[i],
                is_center=True,
                screensize_adaptation=screensize_adaptation
            ) for i in range(0, self.nb_state)
        ]

    # Change l'état du bouton en vérifiant la validité de l'état
    def set_state(self, state):
        if state < self.nb_state:
            self.state = state

    # Change le text en recréant les textures textes
    def change_text(self, text):
        for i in range(0, self.nb_state):
            self.text[i].change_text(text[i])

    # Change la police en recréant les textures textes
    def change_font(self, font):
        for i in range(0, self.nb_state):
            self.text[i].change_font(font)

    # Change la couleur du texte en recréant les textures textes
    def change_text_color(self, text_color):
        for i in range(0, self.nb_state):
            self.text[i].change_text_color(text_color[i])

    # Vérifie si les coordonnées sont sur le bouton
    def is_coord_on(self, coord):
        return self.coord[0] <= coord[0] < self.coord[0] + self.background_texture[self.state].get_width() and \
            self.coord[1] <= coord[1] < self.coord[1] + self.background_texture[self.state].get_height()

    # Affichage sur du bouton
    def render(self, window):
        # Affichage du fond
        window.blit(self.background_texture[self.state], self.coord)
        # Affichage du texte
        self.text[self.state].render(window)
