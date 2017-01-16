import numpy
from numpy import binary_repr
from scipy.io import wavfile

def cacher_dans_audio(nom_fichier, nom_resultat, message, bits_utilises):
    # message doit être une chaîne de caractères sous forme binaire
    # bits_utilises indique le nombre de bits LSB utilisés pour cacher le message
    rate, t = wavfile.read(nom_fichier) # t contient le tableau des données audio

    # Nombre de bits utilisés pour le codage du fichier wav
    bits_codage = t[0].itemsize * 8

    # On détermine si le fichier est mono ou stéréo ainsi que son codage.
    stereo = False
    if type(t[0]) is numpy.ndarray:
        stereo = True

    # On vérifie d'abord qu'il y a suffisament de places pour cacher le message.
    # On ne compte pas les 18 premières cases utilisées pour stocker bits_utilises
    # et nb_octets. On multiplie le total par 2 si le fichier est stéréo.
    if len(message) > (t.size * bits_utilises) - (18 * (1 + stereo)):
        print("Message trop long pour être caché. Tentez d'augmenter bits_utilises.")
        return

    # On code d'abord bits_utilises dans le fichiers sur 6 bits répartis
    # sur les 3 premières valeurs de t.
    b = binary_repr(bits_utilises, 6)
    # b est la représentation binaire de bits_utilises sur 6 bits
    for i in range(3):
        if stereo:
            code_sample = binary_repr(t[i][0], bits_codage)
            t[i][0] = int(code_sample[0:-2] + b[2*i:2*i+2], 2)
        else:
            code_sample = binary_repr(t[i], bits_codage)
            t[i] = int(code_sample[0:-2] + b[2*i:2*i+2], 2)

    # On code ensuite le nombre d'octets du message sur 30 bits répartis
    # sur les 15 valeurs suivantes de t.
    nb_octets = binary_repr(len(message) // 8, 30)
    for i in range(3, 18):
        indice = (i-3) * 2
        if stereo:
            code_sample = binary_repr(t[i][0], bits_codage)
            t[i][0] = int(code_sample[0:-2] + nb_octets[indice:indice+2], 2)
        else:
            code_sample = binary_repr(t[i], bits_codage)
            t[i] = int(code_sample[0:-2] + nb_octets[indice:indice+2], 2)

    nb_octets = int(nb_octets, 2) # On convertit nb_octets en entier

    # On veut s'assurer que le dernier morceau du message à coder ne pose pas de
    # problème même si bits_utilises ne divise pas bits_codage.
    # Pour cela on ajoute suffisament de "0" à la fin de message.
    message += 2 * bits_utilises * "0"

    # On code maintenant message en utilisant bits_utilises LSB pour chaque
    # valeur de t[i].
    i_message = 0 # Compte le nombre de bits de message cachés
    i = 18
    while (i_message < nb_octets * 8) and i < len(t):
        if stereo:
            for j in range(2):
                code_sample = binary_repr(t[i][j], bits_codage)
                t[i][j] = int(code_sample[0:bits_codage-bits_utilises] +
                              message[i_message:i_message + bits_utilises], 2)
                i_message += bits_utilises

        else:
            code_sample = binary_repr(t[i], bits_codage)
            t[i] = int(code_sample[0:bits_codage-bits_utilises] +
                       message[i_message:i_message + bits_utilises], 2)
            i_message += bits_utilises
        i += 1

    wavfile.write(nom_resultat, rate, t) # Ecriture du fichier audio modifié

def extraire_depuis_audio(nom_fichier):
    rate, t = wavfile.read(nom_fichier)

    # Nombre de bits utilisés pour le codage du fichier wav
    bits_codage = t[1].itemsize * 8

    # On détermine si le fichier est mono ou stéréo ainsi que son codage.
    stereo = False
    if type(t[0]) is numpy.ndarray:
        stereo = True

    # Récupération de bits_utilises
    bits_utilises = ""
    for i in range(3):
        if stereo:
            code_sample = binary_repr(t[i][0], bits_codage)
        else:
            code_sample = binary_repr(t[i], bits_codage)
        bits_utilises += code_sample[-2:] # On récupère les 2 derniers bits
    bits_utilises = int(bits_utilises, 2)

    # Récupération de nb_octets
    nb_octets = ""
    for i in range(3, 18):
        if stereo:
            code_sample = binary_repr(t[i][0], bits_codage)
        else:
            code_sample = binary_repr(t[i], bits_codage)
        nb_octets += code_sample[-2:] # On récupère les 2 derniers bits
    nb_octets = int(nb_octets, 2)

    # Récupération de message
    message = ""
    i = 18
    while (len(message) < nb_octets * 8) and i < len(t):
        if stereo:
            for j in range(2):
                code_sample = binary_repr(t[i][j], bits_codage)
                message += code_sample[bits_codage-bits_utilises:]
        else:
            code_sample = binary_repr(t[i], bits_codage)
            # On récupère les bits_utilises derniers bits
            message += code_sample[bits_codage-bits_utilises:]
        i +=1
    return message[:nb_octets*8] # On ignore les derniers bits récupérés en trop
