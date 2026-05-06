#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(void)
{
    string player1 = get_string("Player 1: ");
    string player2 = get_string("Player 2: ");

    int score1 = 0, score2 = 0;

    int points[26] = {
        1, 3, 3, 2, 1, 4, 2, 4, 1, 8,
        5, 1, 3, 1, 1, 3, 10, 1, 1, 1,
        1, 4, 4, 8, 4, 10
    };

    for (int i = 0, n = strlen(player1); i < n; i++)
    {
        if (isalpha(player1[i]))
        {
            char c = toupper(player1[i]);
            score1 += points[c - 'A'];
        }
    }

    for (int i = 0, n = strlen(player2); i < n; i++)
    {
        if (isalpha(player2[i]))
        {
            char c = toupper(player2[i]);
            score2 += points[c - 'A'];
        }
    }

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
