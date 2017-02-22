#include "image_LSB.h"

int main(void)
{
    cacher_dans_image("img.bmp", "res.bmp", "message", 2, 2);
    int *sz = malloc(sizeof(int));
    char *t = extraire_depuis_image("res.bmp", sz);
    free(sz);
    free(t);
    return 0;
}
