#include "image_LSB.h"

int main(void)
{
    cacher_dans_image("img.bmp", "res.bmp", "message", 8, 2);
    int sz;
    char *message = extraire_depuis_image("res.bmp", &sz);
    for (int i = 0; i < sz; i++)
        printf("%x\n", message[i]);
    free(message);
    return 0;
}
