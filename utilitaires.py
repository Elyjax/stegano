from numpy import binary_repr

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
