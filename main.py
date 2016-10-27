def cacherTexte(nomFichier, texte):
    fi = open(nomFichier, 'rb')
    fo = open('out', 'wb')

    fo.write(fi.read(54))
    for c in texte + chr(4):
        codeLettre = bin(ord(c))[2:].zfill(8)
        for i in range(0, 4):
            codePixel = bin(int.from_bytes(fi.read(1), 'big'))[2:].zfill(8)
            nouveauCode = codePixel[0:6] + codeLettre[i*2:(i*2)+2]
            fo.write(int(nouveauCode, 2).to_bytes(1, 'big'))
    fo.write(fi.read())
    fo.close()
    fi.close()

def extraireTexte(nomFichier):
    fi = open(nomFichier, 'rb')
    fi.seek(54)
    texte = ""
    EOF = False
    while not EOF:
        codeLettre = ""
        for i in range(0, 4):
            codePixel = bin(int.from_bytes(fi.read(1), 'big'))[2:].zfill(8)
            codeLettre += codePixel[6:]
        if codeLettre == '00000100':
            EOF = True
        else:
            texte += chr(int(codeLettre, 2))
    fi.close()
    return texte

def inverserImage(nomFichier):
    fi = open(nomFichier, 'rb')
    fo = open(nomFichier + ".swp", 'wb')

    fo.write(fi.read(54))
    for c in fi.read():
        codePixel = bin(c)[2:].zfill(8)
        nouveauCode = codePixel[4:8] + codePixel[0:4]
        fo.write(int(nouveauCode, 2).to_bytes(1, 'big'))
    fo.write(fi.read())
    fo.close()
    fi.close()
