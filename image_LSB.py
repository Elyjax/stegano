from scipy.misc import *
from numpy import binary_repr

def cacher_dans_image(nom_fichier, nom_resultat, message, bits_utilises):
    # message doit être une chaîne de caractères sous forme binaire
    # bits_utilises indique le nombre de bits LSB utilisés pour cacher le message
    t = imread(nom_fichier)
    # t est la matrice des pixels, chaque pixel étant un tableau [R, G, B]

    # On vérifie d'abord qu'il y a suffisament de places pour cacher le message.
    # On ne compte pas la première ligne de pixels utilisée pour stocker bits_utilises
    # et nb_octets.
    if len(message) > (len(t)-1) * len(t[0]) * 3 * bits_utilises:
        print("Message trop long pour être caché. Tentez d'augmenter bits_utilises.")
        return

    # On code d'abord bits_utilises dans le fichiers sur 6 bits répartis
    # sur les 3 valeurs RGB du premier pixel.
    b = binary_repr(bits_utilises, 6)
    for i in range(3):
        code_pixel = binary_repr(t[0][0][i], 8)
        t[0][0][i] = int(code_pixel[0:6] + b[2*i:2*i+2], 2)

    # On code ensuite le nombre d'octets du message sur 30 bits répartis
    # sur les 5 pixels suivants de la première ligne.
    nb_octets = binary_repr(len(message) // 8, 30)
    for i in range(1, 6):
        for j in range(3):
            code_pixel = binary_repr(t[0][i][j], 8)
            # Chaque pixel code 6 bits de nb_octets, 2 bits par valeur RGB.
            # A la jeme composante RGB du ieme pixels on a donc déjà codé
            # (i-1)*6 + (2*j) bits de nb_octets (i commence à 1).
            indice = 6*(i-1) + (2*j)
            t[0][i][j] = int(code_pixel[0:6] + nb_octets[indice:indice+2], 2)
    nb_octets = int(nb_octets, 2) # On convertit nb_octets en entier

    # On veut s'assurer que le dernier morceau du message à coder ne pose pas de
    # problème même si bits_utilises ne divise pas 8 (taille d'un octet).
    # Pour cela on ajoute suffisament de "0" à la fin de message.
    message += bits_utilises * "0"

    # On code maintenant message en utilisant bits_utilises LSB pour chaque
    # valeur RGB des pixels.
    i_message = 0 # Compte le nombre de bits de message codés
    i = 1 # On commence à partir de la deuxième ligne de pixels
    while (i_message < nb_octets * 8) and i < len(t):
        j = 0
        while (i_message < nb_octets * 8) and j < len(t[0]):
            k = 0
            while (i_message < nb_octets * 8) and k < 3:
                code_pixel = binary_repr(t[i][j][k], 8)
                nouveau_code = (code_pixel[0:8-bits_utilises] +
                                message[i_message:i_message+bits_utilises])
                t[i][j][k] = int(nouveau_code, 2)
                i_message += bits_utilises
                k += 1
            j += 1
        i += 1
    imsave(nom_resultat, t) # Ecriture de l'image modifiée

def extraire_depuis_image(nom_fichier):
    t = imread(nom_fichier)

    # Récupération de bits_utilises
    bits_utilises = ""
    for i in range(3):
        code_pixel = binary_repr(t[0][0][i], 8)
        bits_utilises += code_pixel[6:8] # On récupère les 2 derniers bits
    bits_utilises = int(bits_utilises, 2)

    # Récupération de nb_octets
    nb_octets = ""
    for i in range(1, 6):
        for j in range(3):
            code_pixel = binary_repr(t[0][i][j], 8)
            nb_octets += code_pixel[6:8] # On récupère les 2 derniers bits
    nb_octets = int(nb_octets, 2)

    # Récupération de message
    message = ""
    i = 1 # Le message commence à partir de la deuxième ligne de pixels
    while (len(message) < nb_octets * 8) and i < len(t):
        j = 0
        while (len(message) < nb_octets * 8) and j < len(t[0]):
            k = 0
            while (len(message) < nb_octets * 8) and k < 3:
                code_pixel = binary_repr(t[i][j][k], 8)
                # On récupère les bits_utilises derniers bits
                message += code_pixel[8-bits_utilises:]
                k += 1
            j += 1
        i +=1
    return message[:nb_octets*8] # On ignore les derniers bits récupérés en trop

def detection_stegano(nom_fichier):
    t = imread(nom_fichier)
    for i in range(len(t)):
        for j in range(len(t[0])):
            for k in [0, 1, 2]:
                if t[i][j][k] % 2 == 0:
                    t[i][j][k] = 0
                else:
                    t[i][j][k] = 255
    imsave("detection.bmp", t)
