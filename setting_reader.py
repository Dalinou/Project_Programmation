import os


# Classe de lecture des parametres
class SettingReader:
    def __init__(self):
        self.filename = "setting.txt"
        # Paramêtre par défaut
        self.screen_size = (1344, 704)
        self.fps = 120
        if os.path.exists(self.filename):
            self.read_file()
        else:
            print("Setting file does not exist, using default setting")
            self.write_file()

    # lis le fichier et extrait les différents paramêtre
    def read_file(self):
        file = open(self.filename, 'r')
        data = file.read().split('\n')
        for d in data:
            if d.split(':')[0] == "screen size":
                self.screen_size = [
                    int(d.split(':')[1].split(',')[0]),
                    int(d.split(':')[1].split(',')[1])
                ]
            elif d.split(':')[0] == "fps":
                self.fps = int(d.split(':')[1])
        file.close()

    # écrit le fichier avec les diifférent paramêtre
    def write_file(self):
        file = open(self.filename, 'w')
        file.write("screen size: %(1)s, %(2)s\nfps: %(3)s" %
                   {'1': self.screen_size[0], '2': self.screen_size[1], '3': self.fps})
        file.close()

    # renvoie lit le fichier et renvoie le paramêtre demandé
    def get_screen_size(self):
        self.read_file()
        return self.screen_size

    def get_fps(self):
        self.read_file()
        return self.fps

    # change la valeur du paramêtre et réecrit le fichier
    def set_screen_size(self, screen_size=(1344, 704)):
        self.screen_size = screen_size
        self.write_file()

    def set_fps(self, fps=120):
        self.fps = fps
        self.write_file()
