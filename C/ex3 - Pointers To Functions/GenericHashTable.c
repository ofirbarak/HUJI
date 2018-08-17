/**
 * @file GenericHashTable.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 27 Aug 2016
 *
 * @brief Generic hash table implementation.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * Generic hash table implementation
 */
// ------------------------------ includes ------------------------------
#include <malloc.h>
#include <assert.h>
#include "GenericHashTable.h"
#include "TableErrorHandle.h"

// -------------------------- const definitions -------------------------
/**
 * @brief A macro that save the index of first cell
 */
#define FIRST_CELL 0


/**
 * @brief A macro that save the print format fot cell number
 */
#define CELL_NUMBER_PRINT "[%d]"

/**
 * @brief A macro that save tab
 */
#define TAB "\t"

/**
 * @brief A macro that save the print format for end raw in table cell
 */
#define END_LINE_PRINT "\t-->"

/**
 * @brief A macro that save the print format for separate cell data
 */
#define SEPARATE_PRINT ","
// -------------------------- Structs -----------------------------------
/**
 * Cell that save pointer to a duplicate key and pointer to data
 */
typedef struct Cell
{
    void *key; // clone of key
    DataP *data; // pointer to data
} Cell;

/**
 * Table structs that save all table cells and functions
 */
typedef struct Table
{
    int originalTableSize;
    Cell ***tableCells;
//    int *tableCellsSize;
    size_t tableSize;
    CloneKeyFcn cloneKeyFunc;
    FreeKeyFcn freeKeyFunc;
    HashFcn tableHashFunc;
    PrintKeyFcn printKeyFunc;
    PrintDataFcn printDataFunc;
    ComparisonFcn comparisonFunc;
} Table;

// ------------------------------ globals -----------------------------
/**
 * Empty cell
 */
Cell *emptyCell;

// ------------------------------ functions -----------------------------
/**
 * brief Make all table cells point to the empty cell
 */
void makeAllTableCellsNull(TableP tableP)
{
    for (int i = 0; i < (int)tableP->tableSize; ++i)
    {
        for (int j = 0; j < MAX_ROW_ELEMENTS; ++j)
        {
            tableP->tableCells[i][j] = emptyCell;
        }
    }
}

/**
 * @brief Create 2D array of cells pointers
 */
Cell ***createNew2DArrayOfPointers(int tableSize)
{
    Cell ***array = (Cell ***)malloc(tableSize * sizeof(Cell **));
    if (array == NULL)
    {
        reportError(MEM_OUT);
        return NULL;
    }
    for (int j = 0; j < tableSize; ++j)
    {
        array[j] = (Cell **)malloc(tableSize * MAX_ROW_ELEMENTS * sizeof(Cell *));
    }
    // Sets cells addresses
    for (int i = 0; i < tableSize; ++i)
    {
        array[i] = (array[FIRST_CELL] + MAX_ROW_ELEMENTS * i);
    }
    if (array[FIRST_CELL] == NULL)
    {
        free(array);
        reportError(MEM_OUT);
        return NULL;
    }
    return array;
}

/**
 * @brief Allocate memory for a hash table with which uses the given functions.
 * tableSize is the number of cells in the hash table.
 * If run out of memory, free all the memory that was already allocated by the function,
 * report error MEM_OUT to the standard error and return NULL.
 */
TableP createTable(size_t tableSize, CloneKeyFcn cloneKey, FreeKeyFcn freeKey
                   , HashFcn hfun, PrintKeyFcn printKeyFun, PrintDataFcn printDataFun
                   , ComparisonFcn fcomp)
{
    TableP newTable = (TableP)malloc(sizeof(Table));
    if (newTable == NULL)
    {
        reportError(MEM_OUT);
        return NULL;
    }
    Cell ***arr = createNew2DArrayOfPointers((int)tableSize);
    if (arr == NULL)
    {
        free(newTable);
        return NULL;
    }
    newTable->originalTableSize = (int)tableSize;
    newTable->tableCells = arr;
    newTable->tableSize = tableSize;
    makeAllTableCellsNull(newTable);
    newTable->cloneKeyFunc = cloneKey;
    newTable->freeKeyFunc = freeKey;
    newTable->tableHashFunc = hfun;
    newTable->printKeyFunc = printKeyFun;
    newTable->printDataFunc = printDataFun;
    newTable->comparisonFunc = fcomp;
    return newTable;
}

/**
 * Resize the table - mul the table and move cells to new table and free the old one
 */
static bool resizeTable(TableP table)
{
    // Resize the table
    Cell ***newCells = createNew2DArrayOfPointers((int)table->tableSize * MAX_ROW_ELEMENTS);
    if (newCells == NULL)
    {
        reportError(MEM_OUT);
        return false;
    }
    // Move cells
    for (int i = 0; i < (int)table->tableSize; ++i)
    {
        for (int j = 0; j < MAX_ROW_ELEMENTS; ++j)
        {
            Cell *c = table->tableCells[i][j];
            if (c != NULL)
            {
                newCells[i * MAX_ROW_ELEMENTS][j] = table->tableCells[i][j];
            }
        }
    }
    free(table->tableCells[FIRST_CELL]);
    free(table->tableCells);
    table->tableSize *= MAX_ROW_ELEMENTS;
    table->tableCells = newCells;
    return true;
}

/**
 * @brief try to save new object in a given raw.
 */
static bool saveNewObject(TableP table, const void* key, DataP object, int raw, int mul)
{
    assert(raw < (int)table->tableSize && raw >= 0);
    for (int j = 0; j < mul && raw + j < (int)table->tableSize; ++j)
    {
        for (int i = 0; i < MAX_ROW_ELEMENTS; ++i)
        {
            if (table->tableCells[raw + j][i] == NULL)
            {
                Cell *newCell = (Cell *) malloc(sizeof(Cell));
                if (newCell == NULL)
                {
                    reportError(MEM_OUT);
                    return false;
                }
                newCell->key = table->cloneKeyFunc(key);
                if (newCell->key == NULL)
                {
                    return false;
                }
                newCell->data = object;
                table->tableCells[raw + j][i] = newCell;
                return true;
            }
        }
    }
    return false;
}


/**
 * @brief Insert an object to the table with key.
 * If all the cells appropriate for this object are full, duplicate the table.
 * If run out of memory, report
 * MEM_OUT and do nothing (the table should stay at the same situation
 * as it was before the duplication).
 * If everything is OK, return true. Otherwise (an error occured) return false;
 */
int insert(TableP table, const void* key, DataP object)
{
    if (key == NULL || table == NULL || object == NULL)
    {
        reportError(GENERAL_ERROR);
        return false;
    }
    // Check if cell key exists
    int *arrC = (int *)malloc(sizeof(int));
    int *l = (int *)malloc(sizeof(int));
    if (arrC == NULL)
    {
        return false;
    }
    if (l == NULL)
    {
        free(arrC);
        return false;
    }
    DataP *pointerToData = findData(table, key, arrC, l);
    free(arrC);
    free(l);
    if (pointerToData != NULL)
    {
        *pointerToData = object;
        return true;
    }
    // Try to find a place and if there isn't resize the table until a place is found
    int raw;
    raw = (int)table->tableSize / table->originalTableSize * table->tableHashFunc(key,
                                                                                  (size_t) table->originalTableSize);
    assert(raw >= 0 && raw <= (int)table->tableSize);
    while (!saveNewObject(table, key, object, raw, (int)table->tableSize / table->originalTableSize))
    {
        if (!resizeTable(table))
        {
            return false;
        }
        raw = (int)table->tableSize / table->originalTableSize * table->tableHashFunc(key,
                                                                                      (size_t) table->originalTableSize);
    }
    return true;
}


/**
 * @brief remove an data from the table.
 * If everything is OK, return the pointer to the ejected data. Otherwise return NULL;
 */
DataP removeData(TableP table, const void* key)
{
    if (key == NULL)
    {
        return NULL;
    }
    DataP *dataP = NULL;
    Cell *cell;
    for (int i = 0; i < (int)table->tableSize; ++i)
    {
        for (int j = 0; j < MAX_ROW_ELEMENTS; ++j)
        {
            cell = table->tableCells[i][j];
            if (cell != NULL && !table->comparisonFunc(cell->key, key))
            {
                dataP = cell->data;
                table->freeKeyFunc(cell->key);
                free(cell);
                table->tableCells[i][j] = emptyCell;
                return dataP;
            }
        }
    }
    return NULL;
}


/**
 * @brief Search the table and look for an object with the given key.
 * If such object is found fill its cell number into arrCell (where 0 is the
 * first cell), and its placement in the list into listNode (when 0 is the
 * first node in the list, i.e. the node that is pointed from the table
 * itself).
 * If the key was not found, fill both pointers with value of -1.
 * return pointer to the data or null
 */
DataP findData(const TableP table, const void* key, int* arrCell, int* listNode)
{
    if (key == NULL || arrCell == NULL || listNode == NULL)
    {
        return NULL;
    }
    *arrCell = -1;
    *listNode = -1;
    Cell *cell;
    for (int i = 0; i < (int)table->tableSize; i++)
    {
        for (int j = 0; j < MAX_ROW_ELEMENTS; ++j)
        {
            cell = table->tableCells[i][j];
            if (cell != NULL && !table->comparisonFunc(cell->key, key))
            {
                *arrCell = i;
                *listNode = j;
                return cell->data;
            }
        }
    }
    return NULL;
}

/**
 * @brief return a pointer to the data that exist in the table in cell number arrCell (where 0 is
 * the first cell), and placment at listNode in the list (when 0 is the
 * first node in the list, i.e. the node that is pointed from the table
 * itself).
 * If such data not exist return NULL
 */
DataP getDataAt(const TableP table, int arrCell, int listNode)
{
    if (arrCell >= 0 && arrCell < (int)table->tableSize && listNode >= 0
        && listNode < MAX_ROW_ELEMENTS)
    {
        return table->tableCells[arrCell][listNode]->data;
    }
    return NULL;
}


/**
 * @brief return the pointer to the key that exist in the table in cell number arrCell (where 0 is
 * the first cell), and placment at listNode in the list (when 0 is the
 * first node in the list, i.e. the node that is pointed from the table
 * itself).
 * If such key not exist return NULL
 */
ConstKeyP getKeyAt(const TableP table, int arrCell, int listNode)
{
    if (arrCell >= 0 && arrCell < (int)table->tableSize && listNode >= 0
        && listNode < MAX_ROW_ELEMENTS)
    {
        return table->tableCells[arrCell][listNode]->key;
    }
    return NULL;
}


/**
 * @brief Print the table (use the format presented in PrintTableExample).
 */
void printTable(const TableP table)
{
    bool printed = false;
    Cell *cell;
    int j;
    for (int i = 0; i < (int)table->tableSize; ++i)
    {
        printf(CELL_NUMBER_PRINT, i);
        j = 0;
        while (j < MAX_ROW_ELEMENTS)
        {
            cell = table->tableCells[i][j];
            if (cell != emptyCell)
            {
                printf(TAB);
                table->printKeyFunc(cell->key);
                printf(SEPARATE_PRINT);
                table->printDataFunc(cell->data);
                printf(END_LINE_PRINT);
                printed = true;
            }
            j++;
        }
        if (!printed)
        {
            printf(END_LINE_PRINT);
        }
        printf("\t\n");
    }
}


/**
 * @brief Free all the memory allocated for the table.
 * It's the user responsibility to call this function before exiting the program.
 */
void freeTable(TableP table)
{
    Cell *c;
    for (int i = 0; i < (int)table->tableSize; ++i)
    {
        for (int j = 0; j < MAX_ROW_ELEMENTS; ++j)
        {
            c = table->tableCells[i][j];
            if (c != NULL)
            {
                table->freeKeyFunc(c->key);
                free(c);
            }
        }
    }
    free(table);
}


