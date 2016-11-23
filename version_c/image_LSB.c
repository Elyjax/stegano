#include <stdlib.h>
#include <stdio.h>

int main(void)
{
    cacher_dans_image("test", "", 0);
    return 0;
}

void cacher_dans_image(char *nom_fichier, char *message, int bits_utilises)
{
    FILE *fichier = fopen(nom_fichier, "wb");

    if (fichier != NULL) {
        fputc('A', fichier);
        fclose(fichier);
    }
}
