def hideText(fileName, text):
    fi = open(fileName, 'rb')
    fo = open('out', 'wb')

    fo.write(fi.read(54))
    for c in text + chr(4):
        letterCode = bin(ord(c))[2:].zfill(8)
        for i in range(0, 4):
            pixelCode = bin(int.from_bytes(fi.read(1), 'big'))[2:].zfill(8)
            newCode = pixelCode[0:6] + letterCode[i*2:(i*2)+2]
            fo.write(int(newCode, 2).to_bytes(1, 'big'))
    fo.write(fi.read())
    fo.close()
    fi.close()

def extractText(fileName):
    fi = open(fileName, 'rb')
    fi.seek(54)
    text = ""
    EOF = False
    while not EOF:
        letterCode = ""
        for i in range(0, 4):
            pixelCode = bin(int.from_bytes(fi.read(1), 'big'))[2:].zfill(8)
            letterCode += pixelCode[6:]
        if letterCode == '00000100':
            EOF = True
        else:
            text += chr(int(letterCode, 2))
    fi.close()
    return text

hideText("img.bmp", "hello!")
print(extractText("out"))
