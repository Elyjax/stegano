from numpy import binary_repr

def texte_vers_binaire(texte):
    s = ""
    for c in texte:
        s += binary_repr(ord(c), 8)
    return s

def binaire_vers_texte(binaire):
    s = ""
    for i in range(len(binaire) // 8):
        s += chr(int(binaire[8*i:8*(i+1)], 2))
    return s

def fichier_vers_binaire(nom_fichier):
    f = open(nom_fichier, 'rb')
    s = ""
    binaire = f.read()
    for i in range(len(binaire)):
        s += binary_repr(binaire[i], 8)
    f.close()
    return s

def binaire_vers_fichier(nom_fichier, binaire):
    f = open(nom_fichier, 'wb')
    for i in range(len(binaire) // 8):
        octet = int(binaire[8*i:8*(i+1)], 2)
        f.write(octet.to_bytes(1, 'little'))
    f.close()
