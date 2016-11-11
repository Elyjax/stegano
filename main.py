from scipy.misc import *
from scipy.io import wavfile
from numpy import binary_repr

def cacherDansImage(nomFichier, message, bitsUtilises):
    t = imread(nomFichier)
    iMessage = 0
    b = binary_repr(bitsUtilises, 6)
    for i in range(3):
        codePixel = binary_repr(t[0][0][i], 8)
        t[0][0][i] = int(codePixel[0:6] + b[2*i:2*i+2], 2)
    nbOctets = binary_repr(len(message) // 8, 30)
    for i in range(1, 6):
        for j in range(3):
            codePixel = binary_repr(t[0][i][j], 8)
            indice = 6*(i-1) + (2*j)
            t[0][i][j] = int(codePixel[0:6] + nbOctets[indice:indice+2], 2)
    nbOctets = int(nbOctets, 2)
    message += bitsUtilises * "0"
    finMessage = False
    i = 1
    while not finMessage and i < len(t):
        j = 0
        while not finMessage and j < len(t[0]):
            k = 0
            while not finMessage and k < 3:
                codePixel = binary_repr(t[i][j][k], 8)
                nouveauCode = codePixel[0:8-bitsUtilises] + message[iMessage:iMessage+bitsUtilises]
                t[i][j][k] = int(nouveauCode, 2)
                iMessage += bitsUtilises
                finMessage = (iMessage >= nbOctets * 8)
                k += 1
            j += 1
        i += 1
    imsave("imgCode.png", t)

def extraireDepuisImage(nomFichier):
    t = imread(nomFichier)
    bitsUtilises = ""
    for i in range(3):
        codePixel = binary_repr(t[0][0][i], 8)
        bitsUtilises += codePixel[6:8]
    bitsUtilises = int(bitsUtilises, 2)
    nbOctets = ""
    for i in range(1, 6):
        for j in range(3):
            codePixel = binary_repr(t[0][i][j], 8)
            nbOctets += codePixel[6:8]
    nbOctets = int(nbOctets, 2)
    message = ""
    iMessage = 0
    finMessage = False
    i = 1
    while not finMessage and i < len(t):
        j = 0
        while not finMessage and j < len(t[0]):
            k = 0
            while not finMessage and k < 3:
                codePixel = binary_repr(t[i][j][k], 8)
                message += codePixel[8-bitsUtilises:]
                iMessage += bitsUtilises
                finMessage = (iMessage >= nbOctets * 8)
                k += 1
            j += 1
        i +=1
    return message[:nbOctets*8]

def cacherDansAudio(nomFichier, message, bitsUtilises):
    rate, t = wavfile.read(nomFichier)
    b = binary_repr(bitsUtilises, 6)
    for i in range(3):
        codeSample = binary_repr(t[i], 16)
        t[i] = int(codeSample[0:14] + b[2*i:2*i+2], 2)
    nbOctets = binary_repr(len(message) // 8, 30)
    for i in range(3, 18):
            codeSample = binary_repr(t[i], 16)
            indice = (i-3)*2
            t[i] = int(codeSample[0:14] + nbOctets[indice:indice+2], 2)
    nbOctets = int(nbOctets, 2)
    message += bitsUtilises * "0"
    finMessage = False
    iMessage = 0
    i = 18
    while not finMessage and i < len(t):
        codeSample = binary_repr(t[i], 16)
        t[i] = int(codeSample[0:16-bitsUtilises] + message[iMessage:iMessage + bitsUtilises], 2)
        iMessage += bitsUtilises
        finMessage = (iMessage >= nbOctets * 8)
        i += 1
    wavfile.write("audioCode.wav", rate, t)

def extraireDepuisAudio(nomFichier):
    rate, t = wavfile.read(nomFichier)
    bitsUtilises = ""
    for i in range(3):
        codeSample = binary_repr(t[i], 16)
        bitsUtilises += codeSample[14:16]
    bitsUtilises = int(bitsUtilises, 2)
    nbOctets = ""
    for i in range(3, 18):
            codeSample = binary_repr(t[i], 16)
            nbOctets += codeSample[14:16]
    nbOctets = int(nbOctets, 2)
    message = ""
    iMessage = 0
    finMessage = False
    i = 18
    while not finMessage and i < len(t):
        codeSample = binary_repr(t[i], 16)
        message += codeSample[16-bitsUtilises:]
        iMessage += bitsUtilises
        finMessage = (iMessage >= nbOctets * 8)
        i +=1
    return message[:nbOctets*8]


def detectionStegano(nomFichier):
    t = imread(nomFichier)
    for i in range(len(t)):
        for j in range(len(t[0])):
            for k in [0, 1, 2]:
                if t[i][j][k] % 2 == 0:
                    t[i][j][k] = 0
                else:
                    t[i][j][k] = 255
    imsave("detection.bmp", t)

def texteVersBinaire(texte):
    s = ""
    for c in texte:
        s += binary_repr(ord(c), 8)
    return s

def binaireVersTexte(binaire):
    s = ""
    for i in range(len(binaire) // 8):
        s += chr(int(binaire[8*i:8*(i+1)], 2))
    return s

def fichierVersBinaire(nomFichier):
    f = open(nomFichier, 'rb')
    s = ""
    binaire = f.read()
    for i in range(len(binaire)):
        s += binary_repr(binaire[i], 8)
    f.close()
    return s

def binaireVersFichier(nomFichier, binaire):
    f = open(nomFichier, 'wb')
    for i in range(len(binaire) // 8):
        octet = int(binaire[8*i:8*(i+1)], 2)
        f.write(octet.to_bytes(1, 'little'))
    f.close()
