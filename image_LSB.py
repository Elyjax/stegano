from scipy.misc import *
from numpy import binary_repr

def cacher_dans_image(nom_fichier, nom_resultat, message, bits_utilises):
    if bits_utilises > 8:
        print("bits_utilises doit être inférieur à 8 pour les fichiers bmp.")
        return

    t = imread(nom_fichier)
    largeur = len(t)
    hauteur = len(t[0])
    t = t.ravel()

    # On vérifie d'abord qu'il y a suffisament de places pour cacher le message.
    bits_disponibles = (len(t) - 40) * bits_utilises
    if len(message) > bits_disponibles:
        print("Message trop long pour être caché.")
        print("Bits nécessaires : " + len(message))
        print("Bits disponibles : " + bits_disponibles)
        return

    # On code d'abord bits_utilises dans le fichiers sur 8 bits répartis
    # sur les 8 premières valeurs RGB.
    b = binary_repr(bits_utilises, 8)
    for i in range(8):
        code_pixel = binary_repr(t[i], 8)
        t[i] = int(code_pixel[0:7] + b[i], 2)

    # On code ensuite le nombre d'octets du message sur 32 bits répartis
    # sur les 32 valeurs RGB suivantes.
    nb_octets = binary_repr(len(message) // 8, 32)
    for i in range(32):
        code_pixel = binary_repr(t[i + 8], 8)
        t[i + 8] = int(code_pixel[0:7] + nb_octets[i], 2)
    # On convertit nb_octets en entier
    nb_octets = int(nb_octets, 2)

    # On veut s'assurer que le dernier morceau du message à coder ne pose pas de
    # problème même si bits_utilises ne divise pas 8 (taille d'un octet).
    # Pour cela on ajoute suffisament de "0" à la fin de message.
    message += bits_utilises * "0"

    # On code maintenant message en utilisant bits_utilises LSB pour chaque
    # valeur RGB des pixels.
    i_message = 0 # Compte le nombre de bits de message codés
    i = 40
    i_octet = 0
    message += "0" * bits_utilises
    while i_message < nb_octets * 8:
        code_pixel = binary_repr(t[i], 8)
        nouveau_code = (code_pixel[0:8-bits_utilises] +
                        message[i_message:i_message+bits_utilises])
        t[i] = int(nouveau_code, 2)
        i_message += bits_utilises
        i += 1
    t = t.reshape((largeur, hauteur, 3))
    imsave(nom_resultat, t) # Ecriture de l'image modifiée

def extraire_depuis_image(nom_fichier):
    t = imread(nom_fichier).ravel()

    # Récupération de bits_utilises
    bits_utilises = ""
    for i in range(8):
        code_pixel = binary_repr(t[i], 8)
        bits_utilises += code_pixel[7] # On récupère le dernier bit
    bits_utilises = int(bits_utilises, 2)

    # Récupération de nb_octets
    nb_octets = ""
    for i in range(32):
        code_pixel = binary_repr(t[i + 8], 8)
        nb_octets += code_pixel[7] # On récupère le dernier bit
    nb_octets = int(nb_octets, 2)

    # Récupération de message
    message = ""
    i = 40
    while (len(message) < nb_octets * 8):
        code_pixel = binary_repr(t[i], 8)
        # On récupère les bits_utilises derniers bits
        message += code_pixel[8-bits_utilises:]
        i +=1
    return message[:nb_octets*8]

def detection_stegano(nom_fichier, nom_resultat):
    t = imread(nom_fichier)
    for i in range(len(t)):
        for j in range(len(t[0])):
            for k in [0, 1, 2]:
                if t[i][j][k] % 2 == 0:
                    t[i][j][k] = 0
                else:
                    t[i][j][k] = 255
    imsave(nom_resultat, t)
