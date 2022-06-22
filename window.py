import pygame


class Window:
    def __init__(self, setting):
        self.setting = setting
        self.window = None
        self.clock = None
        self.screen_list = {}
        self.window_init()

    def window_init(self):
        ...

    def add_screen(self, screen_init):
        ...

    def remove_screen(self, screen_id):
        ...

    def display_screen(self, screen_id):
        ...
