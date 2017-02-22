#ifndef IMAGE_LSB
#define IMAGE_LSB

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void cacher_dans_image(char *nom_fichier_hote, char *nom_fichier_resultat,
                       char *message, int nb_octets_message, int bits_utilises);

char* extraire_depuis_image(char *nom_fichier_hote, int *nb_octets_message);

#endif
