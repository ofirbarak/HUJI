/**
 * @file MyLinkedList.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 22 Aug 2016
 *
 * @brief System linked list implemantation.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * Linked list implementation
 */
// ------------------------------ includes ------------------------------
#include <malloc.h>
#include <string.h>
#include <stdio.h>
#include "MyLinkedList.h"

// -------------------------- const definitions -------------------------
/*
 * MINIMUM NEXT NODES
 */
#define MIN_NEXT_NODES 1

/*
 * EMPTY MESSAGE
 */
#define EMPTY_MSG "Empty!\n"

/*
 * Node style print
 */
#define NODE_PRINT "'%s'->"

/*
 * End list print
 */
#define END_LIST_PRINT "|| size:%d \n"

// ------------------------------ structs -----------------------------
/**
 * @brief: Structure represents a node
 */
typedef struct Node
{
    char *data;
    struct Node *next;
} Node;

/**
 * @brief: Structure represents a list
 */
typedef struct _MyLinkedList
{
    int listSize;
    struct Node *firstNode;
} _MyLinkedList;


// ------------------------------ functions -----------------------------
/**
 * @brief Allocates a new empty LinkedList
 * 			It is the caller's responsibility to free the returned LinkedList.
 *
 * RETURN VALUE:
 * @return a pointer to the new LinkedList, or NULL if the allocation failed.
 */
MyLinkedListP createList()
{
    MyLinkedListP m = (struct _MyLinkedList *)malloc(sizeof(struct _MyLinkedList));
    if (m != NULL)
    {
        m->listSize = 0;
    }
    return m;
}

/**
 * @brief Free list mamory by recursion
 * @param n the head
 * @param numNodes number of nodes in list
 */
void freeListRecursion(Node *n, int numNodes)
{
    if (numNodes > MIN_NEXT_NODES)
    {
        freeListRecursion(n->next, numNodes-1);
    }
    if (n != NULL)
    {
        free(n->data);
        free(n);
    }
    return;
}

Node *createNewNode(const char *val)
{
    Node *newN = (Node *)malloc(sizeof(Node));
    if (newN == NULL)
    {
        return NULL;
    }
    newN->data = (char *)malloc(sizeof(val));
    if (newN->data == NULL)
    {
        free(newN);
        return NULL;
    }
    strcpy(newN->data, val);
    newN->next = NULL;
    return newN;
}

/**
 * @brief Allocates a new MyLinkedList with the same values as l. It is the caller's
 * 			responsibility to free the returned LinkedList.
 * @param l the MyLinkedListP to clone.
 * RETURN VALUE:
 *   @return a pointer to the new LinkedList, or NULL if the allocation failed.
 */
MyLinkedListP cloneList(MyLinkedListP l)
{
    MyLinkedListP dup = createList();
    if (dup == NULL)
    {
        return NULL;
    }
    dup->listSize = l->listSize;
    Node *dupListPointer = l->firstNode;
    Node *newNode = NULL, *preNode;
    int count = l->listSize;
    if (count >= 1)
    {
        //Set the head
        dup->firstNode = createNewNode(dupListPointer->data);
        if (dup->firstNode == NULL)
        {
            return NULL;
        }
        preNode = dup->firstNode;
        while (--count)
        {
            dupListPointer = dupListPointer->next;

            newNode = (Node *)malloc(sizeof(Node));
            if (newNode == NULL)
            {
                freeListRecursion(dup->firstNode, dup->listSize - count);
                return NULL;
            }
            newNode->data = (char *)malloc(sizeof(dupListPointer->data));
            if (newNode->data == NULL)
            {
                free(newNode);
                freeListRecursion(dup->firstNode, dup->listSize - count);
                return NULL;
            }
            strcpy(newNode->data, dupListPointer->data);
            preNode->next = newNode;
            preNode = newNode;
        }
    }
    return dup;
}


/**
 * @brief Frees the memory and resources allocated to LinkedList l.
 * @param l the LinkedList to free.
 * If l is NULL, no operation is performed.
 */
void freeList(MyLinkedListP l)
{
    if (l != NULL)
    {
        freeListRecursion(l->firstNode, l->listSize);
        free(l);
    }
}


/**
 * @brief print LinkedList l and it's contents- see school solution for the exact format.
 * @param l the LinkedList to print.
 */
void printList(const MyLinkedListP l)
{
    if (l != NULL)
    {
        if (l->listSize == 0)
        {
            printf(EMPTY_MSG);
        }
        else
        {
            Node *n = l->firstNode;
            for (int i = 0; i < l->listSize; ++i)
            {
                printf(NODE_PRINT, n->data);
                n = n->next;
            }
            printf(END_LIST_PRINT, l->listSize);
        }
    }
}


/**
 * @brief remove all the ocuurences of val in l
 * @param l the LinkedList
 * @param val the value - char *
 * RETURN VALUE:
 *   @return number of elements that were removed. or MYLIST_ERROR_CODE if error occured
 */
int removeData(MyLinkedListP l, char *val)
{
    if (l == NULL || val == NULL)
    {
        return MYLIST_ERROR_CODE;
    }
    int removedItems = 0;
    if (l->listSize >= 2)
    {
        Node *res = l->firstNode, *curr = res->next, *helper;
        for (int i = 0; i < l->listSize-1 && curr != NULL; ++i)
        {
            helper = curr->next;
            if (!strcmp(curr->data, val))
            {
                res->next = curr->next;
                removedItems++;
                free(curr->data);
                free(curr);
            }
            else
            {
                res = curr;
            }
            curr = helper;
        }
    }
    if (!strcmp((*l->firstNode).data, val))
    {
        Node *r = l->firstNode;
        l->firstNode = (*l->firstNode).next;
        free(r->data);
        free(r);
        removedItems++;
    }
    l->listSize = l->listSize - removedItems;
    return removedItems;
}

/**
 * @brief add val to the beginning of the list(the List may contain duplicates)
 * UPDATE -- val may be changed /deleted and your list should bot be effected by that.
 * @param l the LinkedList
 * @param val the value - char *
 * RETURN VALUE:
 *   @return true iff succeed
 */
bool insertFirst(MyLinkedListP l, char *val)
{
    Node *oldList;
    if (l->listSize > 0)
    {
        oldList = l->firstNode;
    }
    else
    {
        oldList = NULL;
    }
    Node *newNode = createNewNode(val);
    if (newNode == NULL)
    {
        return false;
    }
    newNode->next = oldList;
    l->listSize++;
    l->firstNode = newNode;
    return true;
}


/**
 * @brief search val in the list with recursion
 * @param n The head of list
 * @param val value to add
 * @return the number of val ocuurences in the list.  or MYLIST_ERROR_CODE if error occured
 */
int isInListRecursion(Node *n, const char *val)
{
    if (n == NULL)
    {
        return 0;
    }
    if (!strcmp(n->data, val))
    {
        return 1 + isInListRecursion(n->next, val);
    }
    return isInListRecursion(n->next, val);
}

/**
 * @brief search val in the list
 * @param l the LinkedList
 * @param val the value to add
 * RETURN VALUE:
 *   @return the number of val ocuurences in the list.  or MYLIST_ERROR_CODE if error occured
 */
int isInList(MyLinkedListP l, char *val)
{
    if (l == NULL)
    {
        return MYLIST_ERROR_CODE;
    }
    return isInListRecursion(l->firstNode, val);
}


/**
 * @brief get list size
 * @param l the LinkedList
 * RETURN VALUE:
 *   @return number of elements in the list.  or MYLIST_ERROR_CODE if error occured
 */
int getSize(const MyLinkedListP l)
{
    return l->listSize;
}

/**
 * @brief Returns size in bytes of l and all it's contents
 *			eqvuilant to sum of sizeof for all the list contents with recursion
 * @param n The head of list
 * @param listSize list length
 * @return the allocated size for l
 */
int sumListRecursion(Node *n, int listSize)
{
    if (listSize <= 0)
    {
        return 0;
    }
    return sizeof(n->data) + sumListRecursion(n->next, listSize);
}


/**
 * @brief Returns size in bytes of l and all it's contents
 *			eqvuilant to sum of sizeof for all the list contents
 * @param l the LinkedList
 * RETURN VALUE:
 *   @return the allocated size for l
 */
int getSizeOf(const MyLinkedListP l)
{
    return sumListRecursion(l->firstNode, l->listSize);
}