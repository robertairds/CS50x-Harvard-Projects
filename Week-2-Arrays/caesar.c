#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main (int argc, string argv [])
{

    if (argc != 2)
        {
         printf("Usage: ./caesar key\n");
         return 1;
         }

       for (int i = 0, n = strlen (argv[1]); i < n; i++)
          {
       if (isdigit(argv[1][i]) == 0)
         {
            printf ("Usage ./caesar key\n");
             return 1;
                                                                                    }
                                                                                        }

    int key = atoi(argv[1]);

    while (key > 26)
    {
        key -=26;
    }


    string plain = get_string("plaintext: ");


    printf("ciphertext: ");

    int temp = 0;

    for (int i = 0, n = strlen(plain); i < n; i ++)
    {
        if (isalpha(plain[i]))
        {
            if (isupper(plain[i]))
            {
                temp = plain[i] + key;
                if (temp > 90)
                {
                    printf("%c", temp - 26);
                }
                else printf("%c", temp);
            }
            else
            {
                temp = plain[i] + key;
                if (temp > 122)
                {
                    printf("%c", temp - 26);
                }
                else printf("%c", temp);
            }
        }
        else
        {
            printf("%c", plain [i]);
        }
    }
    printf("\n");


}
