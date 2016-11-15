from numpy import binary_repr
from scipy.io import wavfile

def cacher_dans_audio(nom_fichier, message, bits_utilises):
    rate, t = wavfile.read(nom_fichier)
    b = binary_repr(bits_utilises, 6)
    for i in range(3):
        code_sample = binary_repr(t[i], 16)
        t[i] = int(code_sample[0:14] + b[2*i:2*i+2], 2)
    nb_octets = binary_repr(len(message) // 8, 30)
    for i in range(3, 18):
            code_sample = binary_repr(t[i], 16)
            indice = (i-3)*2
            t[i] = int(code_sample[0:14] + nb_octets[indice:indice+2], 2)
    nb_octets = int(nb_octets, 2)
    message += bits_utilises * "0"
    fin_message = False
    i_message = 0
    i = 18
    while not fin_message and i < len(t):
        code_sample = binary_repr(t[i], 16)
        t[i] = int(code_sample[0:16-bits_utilises] + message[i_message:i_message + bits_utilises], 2)
        i_message += bits_utilises
        fin_message = (i_message >= nb_octets * 8)
        i += 1
    wavfile.write("audioCode.wav", rate, t)

def extraireDepuisAudio(nom_fichier):
    rate, t = wavfile.read(nom_fichier)
    bits_utilises = ""
    for i in range(3):
        code_sample = binary_repr(t[i], 16)
        bits_utilises += code_sample[14:16]
    bits_utilises = int(bits_utilises, 2)
    nb_octets = ""
    for i in range(3, 18):
            code_sample = binary_repr(t[i], 16)
            nb_octets += code_sample[14:16]
    nb_octets = int(nb_octets, 2)
    message = ""
    i_message = 0
    fin_message = False
    i = 18
    while not fin_message and i < len(t):
        code_sample = binary_repr(t[i], 16)
        message += code_sample[16-bits_utilises:]
        i_message += bits_utilises
        fin_message = (i_message >= nb_octets * 8)
        i +=1
    return message[:nb_octets*8]
