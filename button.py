import pygame


class Button:  # TODO add setting
    def __init__(self, coord, nb_state, init_state, background_filename, font, text, text_color,
                 is_center=True, screensize_adaption=False, screensize=[0, 0]):
        # Recupération des variables
        self.nb_state = nb_state
        self.state = init_state
        # Chargement des textures
        self.background_texture = [
            pygame.image.load(background_filename[i]) for i in range(0, self.nb_state)
        ]
        # Création des textures de texte
        self.text_texture = [
            font.render(text[i], True, text_color[i]) for i in range(0, self.nb_state)
        ]
        # Adapte la  taille du bouton à la taile de l'écran
        if screensize_adaption:
            default_screensize = [1344, 704]
            # Pour chaque état
            for i in range(0, nb_state):
                # Changement de la taille de l'image
                self.background_texture[i] = pygame.transform.scale(
                    self.background_texture[i],
                    [
                        screensize[0] / default_screensize[0] * self.background_texture[i].get_width(),
                        screensize[1] / default_screensize[1] * self.background_texture[i].get_height()
                    ])
                self.text_texture[i] = pygame.transform.scale(
                    self.text_texture[i],
                    [
                        screensize[0] / default_screensize[0] * self.text_texture[i].get_width(),
                        screensize[1] / default_screensize[1] * self.text_texture[i].get_height()
                    ])
        # Centrage du boutton sur les coordonnées
        self.coord = [coord[0] - self.background_texture[0].get_width()/2,
                      coord[1] - self.background_texture[0].get_height()/2] if is_center else coord

    # Change l'état du bouton en vérifiant la validité de l'état
    def set_state(self, state):
        if state < self.nb_state:
            self.state = state

    # Change le text en recréant les textures textes TODO à regarder
    def change_text(self, font, text, text_color):
        for i in range(0, self.nb_state):
            self.text_texture = [
                font.render(text[i], False, text_color[i]) for i in range(0, self.nb_state)
            ]

    # Vérifie si les coordonnées sont sur le bouton
    def is_coord_on(self, coord):
        return self.coord[0] <= coord[0] < self.coord[0] + self.background_texture[self.state].get_width() and \
            self.coord[1] <= coord[1] < self.coord[1] + self.background_texture[self.state].get_height()

    # Affichage sur du bouton
    def render(self, window):
        window.blit(self.background_texture[self.state], self.coord)
        text_coord = [
            self.coord[0] + self.background_texture[self.state].get_width()/2 -
            self.text_texture[self.state].get_width()/2,
            self.coord[1] + self.background_texture[self.state].get_height()/2 -
            self.text_texture[self.state].get_height()/2
        ]
        window.blit(self.text_texture[self.state], text_coord)
