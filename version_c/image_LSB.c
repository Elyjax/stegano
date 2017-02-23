#include "image_LSB.h"

void cacher_fichier(char *nom_fichier_hote, char *nom_fichier_resultat,
                    char *nom_fichier_secret, int bits_utilises)
{
    FILE *secret = fopen(nom_fichier_secret, "rb");
    if (secret == NULL) {
        printf("Fichier secret inexistant");
        return;
    }

    fseek(secret, 0, SEEK_END);
    int nb_octets_message = ftell(secret);
    char *message = malloc(nb_octets_message);
    fseek(secret, 0, SEEK_SET);
    fread(message, 1, nb_octets_message, secret);

    cacher_dans_image(nom_fichier_hote, nom_fichier_resultat, message,
                      nb_octets_message, bits_utilises);
}

void extraire_fichier(char *nom_fichier_hote, char *nom_fichier_extrait)
{
    int nb_octets_message = 0;
    char *message = extraire_depuis_image(nom_fichier_hote, &nb_octets_message);

    if (message == NULL)
        return;

    FILE *fichier_extrait = fopen(nom_fichier_extrait, "wb");
    fwrite(message, 1, nb_octets_message, fichier_extrait);

    fclose(fichier_extrait);
    free(message);
}

void cacher_dans_image(char *nom_fichier_hote, char *nom_fichier_resultat,
                       char *message, int nb_octets_message, int bits_utilises)
{
    if (bits_utilises > 8) {
        printf("bits_utilises doit être inférieur à 8\n");
        return;
    }

    FILE *hote = fopen(nom_fichier_hote, "rb");
    if (hote == NULL) {
        printf("Fichier hote inexistant\n");
        return;
    }

    int offset = 0;
    int taille = 0;
    initialiser(hote, &offset, &taille);

    if (nb_octets_message * 8 > (taille - 19) * bits_utilises) {
        printf("Message trop long pour être caché. Tentez d'augmenter bits_utilises.");
        return;
    }

    char *t = malloc(taille);
    fseek(hote, offset, SEEK_SET);
    fread(t, 1, taille, hote);

    for (int i = 0; i < 3; i++) {
        t[i] &= 0b11111100;
        t[i] |= (bits_utilises & (0b11 << (2 * i))) >> (2 * i);
    }

    for (int i = 0; i < 16; i++) {
        t[i + 3] &= 0b11111100;
        t[i + 3] |= (nb_octets_message & (0b11 << (2 * i))) >> (2 * i);
    }

    int i = 19;
    int i_message = 0;
    int i_octet = 0;
    char octet_message = message[0];
    char masque = 0b11111111 << bits_utilises;
    while (i_message < nb_octets_message) {
        t[i] &= masque;
        for (int j = 0; j < bits_utilises && i_message < nb_octets_message; j++) {
            t[i] |= ((octet_message & (1 << i_octet)) >> i_octet) << j;

            if (i_octet == 7) {
                i_octet = 0;
                i_message++;
                octet_message = message[i_message];
            }
            else
                i_octet++;
        }
        i++;
    }

    FILE *resultat = fopen(nom_fichier_resultat, "wb");
    char header[offset];
    fseek(hote, 0, SEEK_SET);
    fread(header, 1, offset, hote);
    fwrite(header, 1, offset, resultat);
    fwrite(t, 1, taille, resultat);

    fclose(hote);
    fclose(resultat);
    free(t);
}

char* extraire_depuis_image(char *nom_fichier_hote, int *nb_octets_message)
{
    FILE *hote = fopen(nom_fichier_hote, "rb");
    if (hote == NULL) {
        printf("Fichier hote inexistant\n");
        return NULL;
    }

    int offset = 0;
    int taille = 0;
    initialiser(hote, &offset, &taille);

    char *t = malloc(taille);
    fseek(hote, offset, SEEK_SET);
    fread(t, 1, taille, hote);

    int bits_utilises = 0;
    *nb_octets_message = 0;

    for (int i = 0; i < 3; i++)
        bits_utilises |= (t[i] & 0b11) << (2 * i);

    for (int i = 0; i < 16; i++)
        *nb_octets_message |= (t[i + 3] & 0b11) << (2 * i);

    int i = 19;
    int i_message = 0;
    int i_octet = 0;
    char *message = malloc(*nb_octets_message);
    char octet_message = 0;
    while (i_message < *nb_octets_message) {
        for (int j = 0; j < bits_utilises && i_message < *nb_octets_message; j++) {
            octet_message |= ((t[i] & (1 << j)) >> j) << i_octet;

            if (i_octet == 7) {
                i_octet = 0;
                message[i_message] = octet_message;
                octet_message = 0;
                i_message++;
            }
            else
                i_octet++;
        }
        i++;
    }

    fclose(hote);
    free(t);

    return message;
}

void initialiser(FILE *hote, int *offset, int *taille)
{
    int colonnes = 0;
    int lignes = 0;
    int bits_par_pixel = 0;
    fseek(hote, 0xa, SEEK_SET);
    fread(offset, 4, 1, hote);
    fseek(hote, 0x12, SEEK_SET);
    fread(&colonnes, 4, 1, hote);
    fread(&lignes, 4, 1, hote);
    fseek(hote, 0x1c, SEEK_SET);
    fread(&bits_par_pixel, 2, 1, hote);

    int octets_par_pixel = bits_par_pixel / 8;
    int octets_par_ligne = colonnes * octets_par_pixel;
    if (octets_par_ligne  % 4 != 0)
        octets_par_ligne = ((octets_par_ligne / 4) + 1) * 4;
    *taille = octets_par_ligne * lignes;
}
