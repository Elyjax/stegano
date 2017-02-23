#include "image_LSB.h"

int main(void)
{
    cacher_fichier("img.bmp", "res.bmp", "d.pdf", 3);
    extraire_fichier("res.bmp", "res.pdf");
    return 0;
}
