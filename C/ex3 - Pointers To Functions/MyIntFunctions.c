/**
 * @file MyIntFunctions.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 27 Aug 2016
 *
 * @brief Int hash table implementation.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * Int hash table implementation
 */
// ------------------------------ includes ------------------------------
#include <malloc.h>
#include <stdio.h>
#include "MyIntFunctions.h"
#include "TableErrorHandle.h"

// ------------------------------ functions -----------------------------
/**
 * @brief clone an int
 */
void* cloneInt(const void* i)
{
    if (i == NULL)
    {
        reportError(GENERAL_ERROR);
        return NULL;
    }
    int *clone = malloc(sizeof(*(int *)i));
    if (clone == NULL)
    {
        reportError(MEM_OUT);
        return NULL;
    }
    *clone = *(int *)i;
    return (void *)clone;
}

/**
 * @brief free an int
 */
void freeInt(void* i)
{
    if (i == NULL)
    {
        reportError(GENERAL_ERROR);
        return;
    }
    free(i);
}

/**
 * @brief hash value of key for HashTable with size tableSize
 *  assuming key pointer to an int
 * @return number between 0-(tableSize-1)
 */
int intFcn(const void* key, size_t tableSize)
{
    if (key != NULL)
    {
        int i = *(int *) key % tableSize;
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
 *  assuming key pointer to an int
 */
void intPrint (const void* key)
{
    if (key != NULL)
    {
        printf("%d", *(int *)key);
    }
}

/**
 *  intCompare - pointer to int comparison function:
 * @brief compare 2 ints
 *   returns zero int if both ints are equal, otherwise
 *   returns non-zero.
 */
int intCompare(const void *key1, const void *key2)
{
    if (*(int *)key1 == *(int *)key2)
    {
        return 0;
    }
    return 1;
}
