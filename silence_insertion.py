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
#dtypemode = 'int16'
#ndtype=int(dtypemode[3:])

#variable globale
dtypemode = 'int16'

def est_silence(t,indice) :
    ndtype=int(dtypemode[3:])
    return abs(t[indice]/(2**ndtype)) < 1/100

def len_min_silences(nbitcodage) : 
    n=1
    while (2**nbitcodage-1)/n > 0.1 :
        n=n+1
    return n

#coder_ds_wav('discours1(1.1s).wav',txt,1,'int16')

def modification_silence(t,i,morceauchaine,nbitcodage):
    n = len(t)
    longueursilence=1
    k=i+1
    while est_silence(t,k) and k < n :
        k=k+1
        longueursilence = longueursilence + 1
    x = int(morceauchaine,2)
    beta = n % (2**nbitcodage)
    ajoutlongueur = x-beta
    if ajoutlongueur == 0 or len(morceauchaine) == 0 :
        return (False,i+n)
    elif ajoutlongueur < 0 :
        ajoutlongueur = ajoutlongueur + (2**nbitcodage)
        for j in range(0,ajoutlongueur) :
            t.insert(i+n+j,0)
        return(True,i+n+ajoutlongueur)
    else :
        for j in range(0,ajoutlongueur) :
            t.insert(i+n+j,0)
        return(True,i+n+ajoutlongueur)

def cacher_dans_silences(nomfichier,message,nbitcodage):
    f = wavfile.read(nomfichier)
    t = f[1] #array complet du son
    t = list(t)
    lenmessage = len(message)
    n = len(t)
    nombre_octets = np.binary_repr(n,30) #chaine binaire de la longueur du txt sur 30 bit comptant les octets
    chaine = nombre_octets + message
    i = 0
    imessage = 0
    while i < n :
        if est_silence(t,i) :
            (changement,i) = modification_silence(t,i,chaine[imessage:imessage+nbitcodage],nbitcodage)
            if changement :
                imessage=imessage+nbitcodage
        else :
            i=i+1
    t = np.asarray(t,dtype=np.int16)
    wavfile.write("resultat.wav",44100,t)
    
def extraire_depuis_silences(nomfichier,nbitcodage):
    f = wavfile.read(nomfichier)
    t = f[1]
    message = ''
    n = len(t)
    i = 0
    while len(message) < 30 :
        if est_silence(t,i) :
            longueursilence=1
            k=i+1
            while k < n and est_silence(t,k) :
                k=k+1
                longueursilence = longueursilence + 1
            valeur = longueursilence % (2**nbitcodage)
            message = message + np.binary_repr(valeur,2**nbitcodage)
            i = i + longueursilence
        else :
            i=i+1
    longueurmessage = int(message[0:30],2)*8
    j = 0
    while j < n and len(message) < (30 + longueurmessage) :
        if est_silence(t,j) :
            longueursilence=1
            k=j+1
            while k < n and est_silence(t,k):
                k=k+1
                longueursilence = longueursilence + 1
            valeur = longueursilence % (2**nbitcodage)
            message = message + np.binary_repr(valeur,2**nbitcodage)
            j = j + longueursilence
        else :
            j=j+1
    return message[30:30 + longueurmessage]
        
#a=np.array([4,8,10,58,28000,-4561]) a.dtype -> dtype('int32')
#a.astype('int16')
#array([    4,     8,    10,    58, 28000, -4561], dtype=int16)
