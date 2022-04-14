import numpy as np
import random as random
import pygame
import sys
import math

pygame.init()
#Donnée de dimension de l'affichage
pas = [32, 32]
dim = [32, 20]
res = [pas[0]*dim[0], pas[1]*dim[1]]

#création de la fenetre
windows = pygame.display.set_mode(res)
#création de la clock
Clock = pygame.time.Clock()
#Chargement des textures
Mire = pygame.image.load('Texture/Mire 1.png')
Herbe = pygame.image.load('Texture/Herbe 1.png')
Sable = pygame.image.load('Texture/Sable 1.png')
Eau = pygame.image.load('Texture/Eau 1.png')
#Création de la carte
carte = [[' ' for _ in range(0, dim[1])] for _ in range(0, dim[0])]
#Remplisage de la carte
for i in range(0, dim[0]):
    for j in range(0, dim[1]):
        if 4 <= i < 6:
            carte[i][j] = 'S'
        elif 28 < i + j < 32:
            carte[i][j] = 'E'
        else:
            carte[i][j] = 'H'

#Fonction d'actualisation de l'affichage
def affich():
    #affichage du fond  (carte)
    for i in range(0, dim[0]):
        for j in range(0, dim[1]):
            if carte[i][j] == 'S':
                windows.blit(Sable, (i * pas[0], j * pas[1]))
            elif carte[i][j] == 'H':
                windows.blit(Herbe, (i * pas[0], j * pas[1]))
            elif carte[i][j] == 'E':
                windows.blit(Eau, (i * pas[0], j * pas[1]))
    #Récupération des coordonnées
    posx = math.floor(event.pos[0] / pas[0]) * pas[0]
    posy = math.floor(event.pos[1] / pas[1]) * pas[1]
    # affichage de la mire souris
    windows.blit(Mire, (posx, posy))

#Boucle de fonctionnement
while True:
    #Tempo pour être à 120 Ips
    Clock.tick(120)
    #Lecture des entrées
    for event in pygame.event.get():
        #Alt-f4 ou croix rouge
        if event.type == pygame.QUIT:
            sys.exit()
        #Déplacement de la souris
        if event.type == pygame.MOUSEMOTION:
            affich()
        #Click de la souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Récupération des coordonnées
            posx = math.floor(event.pos[0] / pas[0])
            posy = math.floor(event.pos[1] / pas[1])
            #Changement de la carte
            if carte[posx][posy] == 'S':
                carte[posx][posy] = 'H'
            elif carte[posx][posy] == 'H':
                carte[posx][posy] = 'E'
            else:
                carte[posx][posy] = 'S'
            affich()

    pygame.display.update()

