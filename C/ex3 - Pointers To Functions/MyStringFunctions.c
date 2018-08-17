/**
 * @file MyStringFunctions.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 27 Aug 2016
 *
 * @brief String hash table implementation.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * String hash table implementation
 */
// ------------------------------ includes ------------------------------
#include <malloc.h>
#include <string.h>
#include "MyStringFunctions.h"
#include "TableErrorHandle.h"

// ------------------------------ functions -----------------------------
/**
 * @brief clone a string
 */
void* cloneStr(const void* s)
{
    if (s == NULL)
    {
        reportError(GENERAL_ERROR);
        return NULL;
    }
    char *s_string = (char *)s;
    char *clone = malloc(strlen(s_string) + 1);
    if (clone == NULL)
    {
        reportError(MEM_OUT);
        return NULL;
    }
    strcpy(clone, s_string);
    return (void *)clone;
}

/**
 * @brief free an string
 */
void freeStr(void* s)
{
    if (s == NULL)
    {
        reportError(GENERAL_ERROR);
        return;
    }
    free(s);
}

/**
 * Sum ascii of string
 */
int sumAscii(const char *s_string)
{
    int asciiSum = 0;
    for (int i = 0; i < (int)strlen(s_string); ++i)
    {
        asciiSum += s_string[i];
    }
    return asciiSum;
}

/**
 * @brief hash value of key for HashTable with size tableSize
 *  assuming key pointer to string
 * @return number between 0-(tableSize-1)
 */
int strFcn(const void* s, size_t tableSize)
{
    if (s != NULL)
    {
        char *c = (char *)s;
        int i = sumAscii(c) % (int)tableSize;
        if (i < 0)
        {
            i += tableSize;
        }
        return i;
    }
    return -1;
}

/**
 * @brief print a string
 *  assuming key pointer to string
 *
 */
void strPrint (const void* s)
{
    if (s != NULL)
    {
        printf("%s", (char *)s);
    }
}

/**
 *  strCompare - pointer to int comparison function:
 * @brief compare 2 strings
 *   returns zero int if both strings are equal, otherwise
 *   returns non-zero.
 */
int strCompare(const void* k1, const void *k2)
{
    if (sumAscii(k1) == sumAscii(k2))
    {
        return 0;
    }
    return 1;
}