from scipy.misc import *
from numpy import binary_repr

def cacherDansImage(nom_fichier, message, bits_utilises):
    t = imread(nom_fichier)
    i_message = 0
    b = binary_repr(bits_utilises, 6)
    for i in range(3):
        code_pixel = binary_repr(t[0][0][i], 8)
        t[0][0][i] = int(code_pixel[0:6] + b[2*i:2*i+2], 2)
    nb_octets = binary_repr(len(message) // 8, 30)
    for i in range(1, 6):
        for j in range(3):
            code_pixel = binary_repr(t[0][i][j], 8)
            indice = 6*(i-1) + (2*j)
            t[0][i][j] = int(code_pixel[0:6] + nb_octets[indice:indice+2], 2)
    nb_octets = int(nb_octets, 2)
    message += bits_utilises * "0"
    fin_message = False
    i = 1
    while not fin_message and i < len(t):
        j = 0
        while not fin_message and j < len(t[0]):
            k = 0
            while not fin_message and k < 3:
                code_pixel = binary_repr(t[i][j][k], 8)
                nouveau_code = code_pixel[0:8-bits_utilises] +
                               message[i_message:i_message+bits_utilises]
                t[i][j][k] = int(nouveau_code, 2)
                i_message += bits_utilises
                fin_message = (i_message >= nb_octets * 8)
                k += 1
            j += 1
        i += 1
    imsave("imgCode.png", t)

def extraireDepuisImage(nom_fichier):
    t = imread(nom_fichier)
    bits_utilises = ""
    for i in range(3):
        code_pixel = binary_repr(t[0][0][i], 8)
        bits_utilises += code_pixel[6:8]
    bits_utilises = int(bits_utilises, 2)
    nb_octets = ""
    for i in range(1, 6):
        for j in range(3):
            code_pixel = binary_repr(t[0][i][j], 8)
            nb_octets += code_pixel[6:8]
    nb_octets = int(nb_octets, 2)
    message = ""
    i_message = 0
    fin_message = False
    i = 1
    while not fin_message and i < len(t):
        j = 0
        while not fin_message and j < len(t[0]):
            k = 0
            while not fin_message and k < 3:
                code_pixel = binary_repr(t[i][j][k], 8)
                message += code_pixel[8-bits_utilises:]
                i_message += bits_utilises
                fin_message = (i_message >= nb_octets * 8)
                k += 1
            j += 1
        i +=1
    return message[:nb_octets*8]


def detectionStegano(nom_fichier):
    t = imread(nom_fichier)
    for i in range(len(t)):
        for j in range(len(t[0])):
            for k in [0, 1, 2]:
                if t[i][j][k] % 2 == 0:
                    t[i][j][k] = 0
                else:
                    t[i][j][k] = 255
    imsave("detection.bmp", t)
