import pygame


# Classe pour faire le rendu de texte
class Text:
    def __init__(self, setting, coord, font, text, text_color,
                 is_center=True, screensize_adaptation=True, interligne=0):
        # Récupération des variables
        self.setting = setting
        self.coord = coord
        self.font = font
        self.text = text
        self.text_color = text_color
        self.is_center = is_center
        self.screensize_adaptation = screensize_adaptation
        self.interligne = interligne
        self.text_texture = None  # Liste car \n pris en compte
        # Création des textures
        self.create_texture()

    # Fabrique la texture du texte
    def create_texture(self):
        # Chargement des textures ligne par ligne
        self.text_texture = [self.font.render(t, True, self.text_color) for t in self.text.split('\n')]
        # Adaptation des textures par rapport à la taille de l'écran
        if self.screensize_adaptation:
            for i in range(0, self.text_texture.__len__()):
                self.text_texture[i] = pygame.transform.scale(
                    self.text_texture[i],
                    [
                        self.setting.screensize[0] / self.setting.default_screensize[0] *
                        self.text_texture[i].get_width(),
                        self.setting.screensize[1] / self.setting.default_screensize[1] *
                        self.text_texture[i].get_height()
                    ])

    # Change les coordonnées
    def change_coord(self, coord):
        self.coord = coord

    # Change le texte
    def change_text(self, text):
        self.text = text
        self.create_texture()

    # Change le police de charactère
    def change_font(self, font):
        self.font = font
        self.create_texture()

    # Change la couleur du texte
    def change_text_color(self, text_color):
        self.text_color = text_color
        self.create_texture()

    # Affiche le text sur la fenêtre
    def render(self, window):
        # Calcul de la différence de position entre 2 lignes
        dh = self.font.get_linesize() + self.interligne
        # Adapte la valeur de dh à la résolution de l'écran
        if self.screensize_adaptation:
            dh = dh * self.setting.screensize[1] / self.setting.default_screensize[1]
        # Boucle qui affiche ligne par ligne le texte
        for i in range(0, self.text_texture.__len__()):
            # change les coordonnées si centré + gestion du \n
            if self.is_center:
                _coord = [
                    self.coord[0] - self.text_texture[i].get_width() / 2,
                    self.coord[1] + dh * (i - 1/2)
                ]
            else:
                _coord = [
                    self.coord[0],
                    self.coord[1] + dh * i
                ]
            # Affichage du texte
            window.blit(self.text_texture[i], _coord)
