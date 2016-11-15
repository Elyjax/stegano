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
#len(t)=184390
#T*len(t) = durée du signal =4.181 s
#écrire un wav (scipy.io.)wavfile.write(filename, rate, data)
dtypemode = 'int16'
ndtype=int(dtypemode[3:])
#len(lgaulle)=239476

def est_silence(t,num,dtypemode) :
    ndtype=int(dtypemode[3:])
    return abs(t[num]/(2**ndtype)) < 1/100

#renvoie la liste des silences : num de début et de fin
def liste_silences(t,dtypemode) :
    l=[]
    b=False
    for i in range(0,len(t)) :
        if not b and est_silence(t,i,dtypemode) :
            l.append([i,i])
            b = True
        else :
            if est_silence(t,i,dtypemode) :
                (l[len(l)-1])[1]=i
            else :
                b = False
    return l

#len(lgaulle)=239476

def silences_longs(l,lenminsilences) :
    i=0
    l2=[]
    while i < len(l) :
        if l[i][1]-l[i][0]+1 < lenminsilences :
            l2.append(l[i])
        i=i+1
    return l

def num_est_ds_liste(i,l2) : #indique si i est le début d'un silence dans l2 liste des intervalles et l'indice dans l2
    n=len(l2)
    j=0
    for j in range(0,n) :
        if i==l2[j][0] :
            return (True,j)
    return (False,0)


#len(l2gaulle)=80416

def len_min_silences(nbitcodage) :
    n=1
    while (2**nbitcodage-1)/n > 0.1 :
        n=n+1
    return n

def coder_ds_wav(nomfichier,txtcode,nbitcodage,dtypemode) :
    ndtype=int(dtypemode[3:])
    f=wavfile.read(nomfichier)
    t=f[1] #array complet du son
    lenmin = len_min_silences(nbitcodage)
    l=liste_silences(t,dtypemode)
    l2=silences_longs(l,lenmin) #liste silences suffisamments longs / nbitcodage
    if len(l2)>(len(txtcode)+30)/nbitcodage : #on code sur 30 bits la longueur de txtcode
        binlentxt=np.binary_repr(len(txtcode),30) #chaine binaire de la longueur du txt sur 30 bit
        chainecodee=binlentxt+txtcode #chaine totale à coder
        #reste=len(chainecodee)%(2**nbitcodage) 
        #nmax=(len(chainecodee)-reste)/(2**nbitcodage)
        data=np.array([],dtype='int16') #array du son modifié
        n=len(t)
        i=0
        while i<n :
            (bool,indicel2)=num_est_ds_liste(i,l2)
            if bool :
                chainecodeel2=chainecodee[indicel2:indicel2+(2**nbitcodage)]
                if chainecodeel2 != '' :
                    x=int(chainecodeel2,2)
                    lensilencel2=l2[indicel2][1]-l2[indicel2][0]+1
                    beta=(lensilencel2)%(2**nbitcodage)
                    #if x-beta>=0 :
                    #    alpha=x-beta #nb de silences à ajouter
                    #else :
                    #    alpha=x-beta+(2**nbitcodage)
                    alpha=x-beta
                    data=np.concatenate((data,np.array([0]*(lensilencel2+alpha),dtype=dtypemode)))
                    #ajout des alpha silences dans le silence
                    i=l2[indicel2][1]+1
                else :
                    data=np.concatenate((data,np.array([t[i]],dtype=dtypemode)))
                    i=i+1
            else :
                data=np.concatenate((data,np.array([t[i]],dtype=dtypemode)))
                i=i+1
        wavfile.write("resultat.wav",44100,data) #data = array des silences modifiés + sons
        return True
    else :
        return False

#coder_ds_wav('discours1(5s).wav',txt,1,'int16')

def decoder_depuis_wav(fichiercode,nbitcodage,dtypemode) :
    ndtype=int(dtypemode[3:])
    lenmin = len_min_silences(nbitcodage) #les silences modifiés seront toujours ok les autres (non modifiés) sont toujours invalides pour le codage
    f=wavfile.read(fichiercode)
    t=f[1]
    l=liste_silences(t,dtypemode)
    l2=l2=silences_longs(l,lenmin)
    n=len(l2)
    chaine=''
    for i in range(0,n) :
        x=(l2[i][1]-l2[i][0]+1)%(2**nbitcodage)
        chainex=np.binary_repr(x,2**nbitcodage)
        chaine=chaine+chainex
    lentxt=int(chaine[0:30],2)
    #return chaine[30:30+lentxt]
    return chaine[0:300]



#In [41]: np.concatenate((np.array([5,8,10,12]),np.array([2,4,8,10])),axis=0)
#Out[41]: array([ 5,  8, 10, 12,  2,  4,  8, 10])
#In [23]: wavfile.write("data",44100,np.array([4,8,10]))
#In [24]: wavfile.write("data2",44100,np.array([4,8,10,58,4500]))
#In [25]: wavfile.write("data3",44100,np.array([4,8,10,58,28000]))
#wavfile.write("data3",44100,np.arange(15000))
    #wavfile.write("data4",44100,np.array([5,8,9,10,48],int16)
    #enregistre en wav 32bit pcm par défaut -> réglage ?
#a=np.array([4,8,10,58,28000,-4561]) a.dtype -> dtype('int32')
#a.astype('int16')
#array([    4,     8,    10,    58, 28000, -4561], dtype=int16)
