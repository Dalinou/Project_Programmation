import pygame



# fait le rendu de text monoligne
def render_text(window, coord, font, text, text_color, is_center=True,
                 screensize_adaption=False, screensize=[0, 0]):
    # fait le rendu du text
    text_texture = font.render(text, True, text_color)
    # adapte la taille du texte à la taille de l'écran
    if screensize_adaption:
        default_screensize = [1344, 704]
        text_texture = pygame.transform.scale(
            text_texture,
            [
                screensize[0] / default_screensize[0] * text_texture.get_width(),
                screensize[1] / default_screensize[1] * text_texture.get_height()
            ])
    if is_center:
        coord = [
            coord[0] - text_texture.get_width()/2,
            coord[1] - text_texture.get_height()/2
        ]
    window.blit(text_texture, coord)


# Fait le rendu de text sur plusieur ligne
def render_text_multilign(window, coord, font, text, text_color, is_center=True,
                 screensize_adaption=False, screensize=[0, 0], interligne=0):
    text_texture = [font.render(t, True, text_color) for t in text.split('\n')]
    # adapte la taille du texte à la taille de l'écran
    default_screensize = [1344, 704]
    dh = font.render("oo", True, text_color).get_width() + interligne
    if screensize_adaption:
        dh = dh * screensize[1] / default_screensize[1]
    for i in range(0, text_texture.__len__()):
        if screensize_adaption:
            text_texture[i] = pygame.transform.scale(
                text_texture[i],
                [
                    screensize[0] / default_screensize[0] * text_texture[i].get_width(),
                    screensize[1] / default_screensize[1] * text_texture[i].get_height()
                ])

        if is_center:
            _coord = [
                coord[0] - text_texture[i].get_width()/2,
                coord[1] - text_texture[i].get_height()/2 + dh * i
            ]
        window.blit(text_texture[i], _coord)
