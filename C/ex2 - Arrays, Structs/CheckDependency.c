/**
 * @file CheckDependency.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 22 Aug 2016
 *
 * @brief System checks is there cyclic dependecy.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * The system checks is there exists a cyclic dependency between files.
 * Input  : <File>.
 * Process: Firstly, pass all input file twice - one for adding the first file in each line,
 *  than each file adds the pointer to dependencies files (file that not exists are not addded
 *  because they canno't close a cycle). Then runs the DFS algorithm, recursively:
 *  procedure DFS(G,v):
 *     label v as discovered
 *     for all edges from v to w in G.adjacentEdges(v) do
 *         if vertex w is not labeled as discovered then
 *             recursively call DFS(G,w)
 *  G - is the global array "dependencies". adjacenty list - each file contains an array of
 *  dependencies files.
 * Output : Ok or error.
 */
// ------------------------------ includes ------------------------------
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <malloc.h>

// -------------------------- const definitions -------------------------
/**
 * @def MAX_CHARACTERS_IN_ONE_LINE 1001
 * @brief A macro that save maximum characters in one line
 */
#define MAX_CHARACTERS_IN_ONE_LINE 1001

/**
 * @def MAX_FILES 1001
 * @brief A macro that save the maximum of files
 */
#define MAX_FILES 100000

/**
 * @def NAX_CHARACTERS_IN_NAME 250
 * @brief A macro that save the maximum characters in name
 */
#define MAX_CHARACTERS_IN_NAME 250

/**
 * @def MAX_DEPENDENCIES 100
 * @brief A macro that save the maximum dependencies file can have
 */
#define MAX_DEPENDENCIES 100

/**
 * @def FIRST_NAME_STRING ": "
 * @brief A macro that save the regex for getting the name of the first file
 */
#define FIRST_NAME_STRING ": "

/**
 * @def DEPENDENCY_NAME_STRING ", \n"
 * @brief A macro that save the regex for getting the name of dependency file
 */
#define DEPENDENCY_NAME_STRING ", \n"

/**
 * @def FILE_INPUT_PLACE 1
 * @brief A macro that save the place in argv for file input
 */
#define FILE_INPUT_PLACE 1

/**
 * @def CYCLIC_MESSAGE "Cyclic dependency\n"
 * @brief A macro that save the cyclic message
 */
#define CYCLIC_MESSAGE "Cyclic dependency\n"

/**
 * @def CYCLIC_MESSAGE "Cyclic dependency\n"
 * @brief A macro that save the cyclic message
 */
#define NO_CYCLIC_MESSAGE "No Cyclic dependency\n"
// ------------------------------ structs -----------------------------
typedef struct file
{
    char fileName[MAX_CHARACTERS_IN_NAME];
    int count; // count how may dependencies are exists
    struct file* fileDependencies[MAX_DEPENDENCIES];
} file;

// ------------------------------ globals -----------------------------
/**
 * @brief Array represents all files (like graph)
 */
file dependencies[MAX_FILES];

/**
 * @brief Number of real files in the big array
 */
int amount;

// ------------------------------ functions -----------------------------
/**
 * @brief Return NULL if not, otherwise return pointer to it's place in array.
 * @param txtFileName file name (txt)
 * @return NULL if not, otherwise return pointer to it's place in array.
 */
file *isFileExists(char *txtFileName)
{
    assert(txtFileName != NULL);
    for (int i = 0; i < amount; i++)
    {
        if (!strcmp(dependencies[i].fileName, txtFileName))
        {
            return &dependencies[i];
        }
    }
    return NULL;
}

/**
 * @brief Adds new file to dependencies array
 * @param txtFileName file name
 */
void allocateNewFile(char *txtFileName)
{
    assert(txtFileName != NULL);
    // File isn't exists, add it
    strcpy(dependencies[amount].fileName, txtFileName);
    dependencies[amount].count = 0;
    amount++;
}

/**
 * @brief First passing - Adds all files
 * @param input file
 */
void firstPass(FILE *input)
{
    assert(input != NULL);
    char line[MAX_CHARACTERS_IN_ONE_LINE];
    char *fileName2 = NULL;
    while (fgets(line, MAX_CHARACTERS_IN_ONE_LINE, input) != NULL)
    {
        fileName2 = strtok(line, FIRST_NAME_STRING);
        if (isFileExists(fileName2) == NULL)
        {
            allocateNewFile(fileName2);
        }
    }
}

/**
 * @brief Check if file appears in file dependencies
 * @param f file to check
 * @param search file to search
 * @return 0 if not, 1 if ture
 */
int isExistsInDependencies(file *f, file *search)
{
    assert(f != NULL);
    assert(search != NULL);
    for (int i = 0; i < f->count; ++i)
    {
        if (f->fileDependencies[i] == search)
        {
            return 1;
        }
    }
    return 0;
}

/**
 * @brief Pass all the file and adds files are exists in dependencies array
 * @param input file
 */
void addDependencies(FILE *input)
{
    assert(input != NULL);
    char line[MAX_CHARACTERS_IN_ONE_LINE];
    char *fileName = NULL;
    file *f = NULL, *dependency = NULL;
    while (fgets(line, MAX_CHARACTERS_IN_ONE_LINE, input) != NULL)
    {
        f = isFileExists(strtok(line, FIRST_NAME_STRING));
        while ((fileName = strtok(NULL, DEPENDENCY_NAME_STRING)) != NULL)
        {
            dependency = isFileExists(fileName);
            if (dependency == NULL)
            {
                allocateNewFile(fileName);
                dependency = isFileExists(fileName);
            }
            if(!isExistsInDependencies(f, dependency) &&
               f->fileName != dependency->fileName)
                // If file exists (if not it can not close a cycle)
            {
                f->fileDependencies[f->count] = dependency;
                (*f).count++;
            }
        }
    }
}

/**
 * @brief check if file exsits in  array
 * @param f poitner to file to search
 * @param array array pointers to files
 * @param arraySize array size
 * @return 1 if yes, 0 otherwise
 */
int isFileInArray(file *f, file *array[], int arraySize)
{
    for (int i = 0; i < arraySize; ++i)
    {
        if (f == array[i])
        {
            return 1;
        }
    }
    return 0;
}

/**
 * @brief Runs DFS algorithm
 * @param f pointer to file
 * @return 1 if a cycle was closed, 0 otherwise
 */
int dfs(file *f, file *gray[], int *graySize)
{
    if (isFileInArray(f, gray, *graySize))
    {
        return 1;
    }
    file *n = NULL;
    gray[(*graySize)++] = f;
    for (int i = 0; i < f->count; ++i)
    {
        n = f->fileDependencies[i];
        if (n != NULL && n->count != 0)
        {
            return dfs(n, gray, graySize);
        }
    }
    return 0;
}

/**
 * @brief Returns a file not in black list
 */
file *getFileNotInBlackList(file *black[], int blackSize)
{
    int in = 0;
    for (int i = 0; i < amount; ++i)
    {
        in = 0;
        for (int j = 0; j < blackSize; ++j)
        {
            if (&dependencies[i] == black[j])
            {
                in = 1;
            }
        }
        if (!in)
        {
            return &dependencies[i];
        }
    }
    return NULL;
}

/**
 * @brief Checking a cycle
 * @return 0 for no, non zero if yes
 */
int checkForACycle()
{
    assert(amount >= 0);
    file *black[MAX_DEPENDENCIES], *gray[MAX_DEPENDENCIES];
    int blackSize = 0;
    int *graySize = (int *)malloc(sizeof(int));
    *graySize = 0;
    file *f = NULL;
    int isExist;
    while ((f = getFileNotInBlackList(black, blackSize)))
    {
        if(dfs(f, gray, graySize))
        {
            return 1;
        }
        // Adds gray to black
        for (int i = 0; i < *graySize; ++i)
        {
            isExist = 0;
            for (int j = 0; j < blackSize; ++j)
            {
                if (black[j] == gray[i])
                {
                    isExist = 1;
                }
            }
            if (!isExist)
            {
                black[blackSize++] = gray[i];
            }
        }
        // clean gray list
        (*graySize) = 0;
    }
    free(graySize);
    return 0;
}


/**
 * @brief main funcion
 * @param argc number of parameters
 * @param argv array of inputs
 * @return 0 if all passed correctly, non zero if error occurred.
 */
int main(int argc, char **argv)
{
    if(argc != 2)
    {
        printf("Error");
        return -1;
    }
    FILE *input = fopen(argv[FILE_INPUT_PLACE], "r");
    if(input == NULL)
    {
        return -1;
    }

    // Create dependency tree - pass all lines and adds the files (the first one each line)
    firstPass(input);

    //Pass again all file and checks other files
    rewind(input);
    addDependencies(input);

    if (checkForACycle())
    {
        printf(CYCLIC_MESSAGE);
    }
    else
    {
        printf(NO_CYCLIC_MESSAGE);
    }
    fclose(input);
    return 0;
}
