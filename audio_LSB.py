from numpy import binary_repr
from scipy.io import wavfile

def cacher_dans_audio(nom_fichier, message, bits_utilises):
    # message doit être une chaîne de caractères sous forme binaire
    # bits_utilises indique le nombre de bits LSB utilisés pour cacher le message
    rate, t = wavfile.read(nom_fichier) # t contient le tableau des données audio

    # On code d'abord bits_utilises dans le fichiers sur 6 bits répartis
    # sur les 3 premières valeurs de t.
    b = binary_repr(bits_utilises, 6)
    # b est la représentation binaire de bits_utilises sur 6 bits
    for i in range(3):
        code_sample = binary_repr(t[i], 16)
        t[i] = int(code_sample[0:14] + b[2*i:2*i+2], 2)

    # On code ensuite le nombre d'octets du message sur 30 bits répartis
    # sur les 15 valeurs suivantes de t.
    nb_octets = binary_repr(len(message) // 8, 30)
    for i in range(3, 18):
            code_sample = binary_repr(t[i], 16)
            indice = (i-3) * 2
            t[i] = int(code_sample[0:14] + nb_octets[indice:indice+2], 2)
    nb_octets = int(nb_octets, 2) # On convertit nb_octets en entier

    # On veut s'assurer que le dernier morceau du message à coder ne pose pas de
    # problème même si bits_utilises ne divise pas 16 (taille d'une case de t).
    # Pour cela on ajoute suffisament de "0" à la fin de message.
    message += bits_utilises * "0"

    # On code maintenant message en utilisant bits_utilises LSB pour chaque
    # valeur de t[i].
    i_message = 0 # Compte le nombre de bits de message codés
    i = 18
    while (i_message < nb_octets * 8) and i < len(t):
        code_sample = binary_repr(t[i], 16)
        t[i] = int(code_sample[0:16-bits_utilises] +
                   message[i_message:i_message + bits_utilises], 2)
        i_message += bits_utilises
        i += 1
    wavfile.write("audio_code.wav", rate, t) # Ecriture du fichier audio modifié

def extraire_depuis_audio(nom_fichier):
    rate, t = wavfile.read(nom_fichier)

    # Récupération de bits_utilises
    bits_utilises = ""
    for i in range(3):
        code_sample = binary_repr(t[i], 16)
        bits_utilises += code_sample[14:16] # On récupère les 2 derniers bits
    bits_utilises = int(bits_utilises, 2)

    # Récupération de nb_octets
    nb_octets = ""
    for i in range(3, 18):
            code_sample = binary_repr(t[i], 16)
            nb_octets += code_sample[14:16] # On récupère les 2 derniers bits
    nb_octets = int(nb_octets, 2)

    # Récupération de message
    message = ""
    i_message = 0
    i = 18
    while (i_message < nb_octets * 8) and i < len(t):
        code_sample = binary_repr(t[i], 16)
        message += code_sample[16-bits_utilises:]
        i_message += bits_utilises
        i +=1
    return message[:nb_octets*8] # On ignore les derniers bits récupérés en trop
