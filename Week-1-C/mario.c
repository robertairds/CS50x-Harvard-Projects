#include <stdio.h>
#include <cs50.h>
int main (void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while ( h < 1 || h > 8);

    for (int row = 1; row <= h; row++)
    {
        for (int space = 0; space < h - row; space++)
        {
            printf(" ");
        }

        for (int hash = 0; hash <row; hash++)
        {
            printf("#");
        }
        printf ("\n");
    }
}
