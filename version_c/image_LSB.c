#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void cacher_dans_image(char *nom_fichier, char *nom_resultat, char *message, int bits_utilises)
{
    FILE *fichier = fopen(nom_fichier, "rb");

    if (fichier == NULL) {
        fclose(fichier);
        return;
    }

    int bits_par_pixel = 0;
    int colonnes = 0;
    int lignes = 0;
    int offset = 0;
    fseek(fichier, 0xa, SEEK_SET);
    fread(&offset, 4, 1, fichier);
    fseek(fichier, 0x12, SEEK_SET);
    fread(&colonnes, 4, 1, fichier);
    fread(&lignes, 4, 1, fichier);
    fseek(fichier, 0x1c, SEEK_SET);
    fread(&bits_par_pixel, 2, 1, fichier);

    int octets_par_pixel = bits_par_pixel / 8;
    int octets_par_ligne = colonnes * octets_par_pixel;
    if (octets_par_ligne  % 4 != 0)
        octets_par_ligne = ((octets_par_ligne / 4) + 1) * 4;
    int taille = octets_par_ligne * lignes;
    int nb_octets_message = strlen(message);

    if (nb_octets_message * 8 > (taille - 19) * bits_utilises) {
        printf("Message trop long pour être caché. Tentez d'augmenter bits_utilises.");
        return;
    }

    unsigned char *t = NULL;
    t = malloc(taille);
    fseek(fichier, offset, SEEK_SET);
    fread(t, 1, taille, fichier);

    for (int i = 0; i < 3; i++) {
        t[i] &= 0b11111100;
        t[i] |= (bits_utilises & (0b11 << (2 * i))) >> (2 * i);
    }

    for (int i = 0; i < 16; i++) {
        t[i + 3] &= 0b11111100;
        t[i + 3] |= (nb_octets_message & (0b11 << (2 * i))) >> (2 * i);
    }

    int i = 19, i_message = 0, i_octet = 0;
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

    FILE *resulat = fopen(nom_resultat, "wb");
    char header[offset];
    fseek(fichier, 0, SEEK_SET);
    fread(header, 1, offset, fichier);
    fwrite(header, 1, offset, resulat);
    fwrite(t, 1, taille, resulat);

    fclose(resulat);
    fclose(fichier);
    free(t);
}

void extraire_depuis_image(char *nom_fichier)
{
    FILE *fichier = fopen(nom_fichier, "rb");

    if (fichier == NULL) {
        fclose(fichier);
        return;
    }

    int bits_par_pixel = 0;
    int colonnes = 0;
    int lignes = 0;
    int offset = 0;
    fseek(fichier, 0xa, SEEK_SET);
    fread(&offset, 4, 1, fichier);
    fseek(fichier, 0x12, SEEK_SET);
    fread(&colonnes, 4, 1, fichier);
    fread(&lignes, 4, 1, fichier);
    fseek(fichier, 0x1c, SEEK_SET);
    fread(&bits_par_pixel, 2, 1, fichier);

    int octets_par_pixel = bits_par_pixel / 8;
    int octets_par_ligne = colonnes * octets_par_pixel;
    if (octets_par_ligne  % 4 != 0)
        octets_par_ligne = ((octets_par_ligne / 4) + 1) * 4;
    int taille = octets_par_ligne * lignes;

    unsigned char *t = NULL;
    t = malloc(taille);
    fseek(fichier, offset, SEEK_SET);
    fread(t, 1, taille, fichier);
    int nb_octets_message = 0, bits_utilises = 0;

    for (int i = 0; i < 3; i++)
        bits_utilises |= (t[i] & 0b11) << (2 * i);

    for (int i = 0; i < 16; i++)
        nb_octets_message |= (t[i + 3] & 0b11) << (2 * i);

    int i = 19, i_message = 0, i_octet = 0;
    char message[nb_octets_message + 1];
    char octet_message = 0;
    while (i_message < nb_octets_message) {
        for (int j = 0; j < bits_utilises && i_message < nb_octets_message; j++) {
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
    message[nb_octets_message] = '\0';
    printf("message : %s\n", message);

    fclose(fichier);
    free(t);
}

int main(void)
{
    cacher_dans_image("img.bmp", "img_modifiee.bmp", "message à cacher", 3);
    extraire_depuis_image("img_modifiee.bmp");
    return 0;
}
