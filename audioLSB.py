from numpy import binary_repr
from scipy.io import wavfile

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
