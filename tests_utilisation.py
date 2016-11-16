# Fichier de test des différentes fonctions

from audio_LSB import *
from utilitaires import *

cacher_dans_audio("audio.wav", fichier_vers_binaire("fichier_a_cacher"), 3)
binaire_vers_fichier("fichier_extrait", extraire_depuis_audio("audio_code.wav"))
