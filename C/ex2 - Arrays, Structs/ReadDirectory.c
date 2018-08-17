/**
 * @file ReadDirectory.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 22 Aug 2016
 *
 * @brief create input file for last question.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * create input file for last question
 */
// ------------------------------ includes ------------------------------
#include <assert.h>
#include <stdio.h>
#include <dirent.h>
#include <string.h>

// -------------------------- const definitions -------------------------
/*
 * NUmber if arguments
 */
#define NUMBER_OF_ARGUMENETS 3

/*
 * File to write arguments position
 */
#define FILE_OUTPUT_POSITION 2

/*
 * Max chars in line
 */
#define MAX_CHARS_IN_LINE 1001

/*
 * UP DIRECTORY
 */
#define UP_DIRECTORY "."

/*
 * UP DIRECTORY 2
 */
#define UP_DIRECTORY2 ".."

/*
 * INCLUDE FORMAT
 */
#define INCLUDE_FORMAT "%s %s\n"

/*
 * NAME FORMAT
 */
#define NAME_FORMAT "%s: "

/*
 * INCLUDE
 */
#define INCLUDE "#include"

/*
 * "
 */
#define QUAT '\"'

/*
 * OPEN BRACKET
 */
#define OPEN_BRACKET '<'

/*
 * CLOSE BRACKET
 */
#define CLOSE_BRACKET '>'

/*
 * END STRING
 */
#define END_STRING '\0'

/*
 * FIRST DEPENDENCY FORMAT
 */
#define FIRST_DEPENDENCY_FORMAT "%s"


/*
 * DEPENDENCY FORMAT
 */
#define DEPENDENCY_FORMAT ",%s"

/*
 * new line
 */
#define NEW_LINE "\n"

/*
 * DIRECTORY PATH
 */
#define DIRECTORY_PATH "%s/%s"

// ------------------------------ functions -----------------------------
/**
 * Main function
 */
int main(int argc, char **argv)
{
    if(argc != NUMBER_OF_ARGUMENETS)
    {
        return -1;
    }
    FILE *writeFile = fopen(argv[FILE_OUTPUT_POSITION], "w");
    assert(writeFile != NULL);

    DIR *fd = opendir(argv[1]);
    assert(fd != NULL);

    struct dirent* in_file;
    FILE *entry_file;
    char line[MAX_CHARS_IN_LINE];
    char name[MAX_CHARS_IN_LINE], begin[MAX_CHARS_IN_LINE];
    size_t len;
    int isFirst = 1;
    while((in_file = readdir(fd)))
    {
        if (!strcmp(in_file->d_name, UP_DIRECTORY))
        {
            continue;
        }
        if (!strcmp(in_file->d_name, UP_DIRECTORY2))
        {
            continue;
        }
        sprintf(name, DIRECTORY_PATH, argv[1], in_file->d_name);
        entry_file = fopen(name, "r");
        assert(entry_file != NULL);

        fprintf(writeFile, NAME_FORMAT, in_file->d_name);
        isFirst = 1;
        while (fgets(line, MAX_CHARS_IN_LINE, entry_file) != NULL)
        {
            sscanf(line, INCLUDE_FORMAT, begin, name);
            len = strlen(name);
            if (!strcmp(begin, INCLUDE) && ((name[0] == QUAT && name[len - 1] == QUAT) ||
                (name[0] == OPEN_BRACKET && name[len - 1] == CLOSE_BRACKET)))
            {
                name[len - 1] = END_STRING; // remove the last char
                memmove(name, name + 1, strlen(name)); // remove the first char
                if (isFirst)
                {
                    fprintf(writeFile, FIRST_DEPENDENCY_FORMAT, name);
                    isFirst = 0;
                }
                else
                {
                    fprintf(writeFile, DEPENDENCY_FORMAT, name);
                }
            }
        }
        fprintf(writeFile, NEW_LINE);
        fclose(entry_file);
    }
    fclose(writeFile);
}

