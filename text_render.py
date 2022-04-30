import pygame


def render_text(window, coord, font, text, text_color, is_center=True,
                 screensize_adaption=False, screensize=[0, 0]):
    text_texture = font.render(text, True, text_color)
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
