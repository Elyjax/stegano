from scipy.io import wavfile
from scipy.fftpack import *
import matplotlib.pyplot as plt
import os
import numpy as np

#os.chdir("C:/Users/Clément/Desktop/TIPE Masquage/Code TIPE")
#f=wavfile.read("test.wav")
#t=f[1]
#frequence d'échantillonnage = 44100 Hz
#période d'échantillonnage = 2.26*10^-5 s
#écrire un wav (scipy.io.)wavfile.write(filename, rate, data)

dtypemode = 'int16' # Type utilisé par le fichier wav
bits_nb_octets = 32 # Nombre de bits utilisés pour stocker la taille du message

def est_silence(t, indice):
    ndtype = int(dtypemode[3:])
    return abs(t[indice] / (2**ndtype)) < 1/100

def len_min_silences(nbitcodage):
    n = 1
    while (2**nbitcodage-1) / n > 0.1 :
        n += 1
    return n

def duree_silence(t, i):
    k = i + 1
    while est_silence(t, k) and k < len(t):
        k += 1
    return k - i

def modification_silence(t, i, valeur_a_cacher, nbitcodage):
    longueur_silence = duree_silence(t, i)
    valeur_a_cacher = int(valeur_a_cacher, 2)
    ajout_silences = valeur_a_cacher - (longueur_silence % (2**nbitcodage))
    while ajout_silences < 0:
        ajout_silences += (2**nbitcodage)
    for j in range(ajout_silences):
        t.insert(i, 0)
    return (True, i + longueur_silence + ajout_silences)

def cacher_dans_silences(nom_fichier, message, nbitcodage):
    f = wavfile.read(nom_fichier)
    t = f[1] # Array complet du son
    t = list(t)
    n = len(t)
    # Nombre d'octets du message à cacher représenté sur bits_nb_octets
    nb_octets = np.binary_repr(len(message) // 8, bits_nb_octets)
    message = nb_octets + message
    i = 0
    i_message = 0 # Compte le nombre de bits de message cachés
    while i < n and i_message < len(message):
        if est_silence(t, i):
            valeur_a_cacher = message[i_message:i_message+nbitcodage]
            (changement, i) = modification_silence(t, i, valeur_a_cacher, nbitcodage)
            if changement:
                i_message += nbitcodage
        else:
            i += 1
    t = np.asarray(t, dtype=np.int16)
    wavfile.write("resultat.wav", 44100, t)

def extraire_depuis_silences(nom_fichier, nbitcodage):
    f = wavfile.read(nom_fichier)
    t = f[1]
    n = len(t)

    # Récupération de nb_octets
    nb_octets = ""
    i = 0
    while len(nb_octets) < bits_nb_octets:
        if est_silence(t, i):
            longueur_silence = duree_silence(t, i)
            valeur = longueur_silence % (2**nbitcodage)
            nb_octets += np.binary_repr(valeur, nbitcodage)
            i += longueur_silence
        else :
            i += 1
    nb_octets = int(nb_octets, 2)

    # Récupération du message
    message = ""
    while (len(message) < nb_octets * 8) and i < len(t):
        if est_silence(t, i):
            longueur_silence = duree_silence(t, i)
            valeur = longueur_silence % (2**nbitcodage)
            message += np.binary_repr(valeur, nbitcodage)
            i += longueur_silence
        else:
            i += 1
    return message

#a=np.array([4,8,10,58,28000,-4561]) a.dtype -> dtype('int32')
#a.astype('int16')
#array([    4,     8,    10,    58, 28000, -4561], dtype=int16)
