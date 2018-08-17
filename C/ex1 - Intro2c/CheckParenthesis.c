/**
 * @file CheckParenthesis.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 9 Aug 2016
 *
 * @brief System checks parenthesis in a file.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * The system checks parenthesis in a file.
 * Input  : <File>.
 * Process: Counting the parenthesis and checks they are balanced.
 * Output : Ok or error.
 */
// ------------------------------ includes ------------------------------
#include <stdio.h>

// -------------------------- const definitions -------------------------
/**
 * @def OPEN_BRACKET_TYPE_1 '<'
 * @brief A macro that save open bracket type 1.
 */
#define OPEN_BRACKET_TYPE_1 '<'

/**
 * @def  OPEN_BRACKET_TYPE_2 '{'
 * @brief A macro that save open bracket type 2.
 */
#define OPEN_BRACKET_TYPE_2 '{'

/**
 * @def OPEN_BRACKET_TYPE_3 '['
 * @brief A macro that save open bracket type 3.
 */
#define OPEN_BRACKET_TYPE_3 '['

/**
 * @def OPEN_BRACKET_TYPE_4 '('
 * @brief A macro that save open bracket type 4.
 */
#define OPEN_BRACKET_TYPE_4 '('

/**
 * @def CLOSE_BRACKET_TYPE_1 '>'
 * @brief A macro that save close bracket type 1.
 */
#define CLOSE_BRACKET_TYPE_1 '>'

/**
 * @def CLOSE_BRACKET_TYPE_2 '}'
 * @brief A macro that save close bracket type 2.
 */
#define CLOSE_BRACKET_TYPE_2 '}'

/**
 * @def CLOSE_BRACKET_TYPE_3 ']'
 * @brief A macro that save close bracket type 3.
 */
#define CLOSE_BRACKET_TYPE_3 ']'

/**
 * @def CLOSE_BRACKET_TYPE_4 ')'
 * @brief A macro that save close bracket type 4.
 */
#define CLOSE_BRACKET_TYPE_4 ')'

/**
 * @def SUPPLY_FILE_ERROR "Please supply a file!\nusage: CheckParenthesis <file name>\n"
 * @brief A macro that save the supply file error.
 */
#define SUPPLY_FILE_ERROR "Please supply a file!\nusage: CheckParenthesis <file name>\n"

/**
 * @def OPEN_FILE_ERROR "Error! trying to open the file %p\n"
 * @brief A macro that save the open file error.
 */
#define OPEN_FILE_ERROR "Error! trying to open the file %p\n"

/**
 * @def OK_MSG "ok\n"
 * @brief A macro that save the ok message.
 */
#define OK_MSG "ok\n"

/**
 * @def BAD_STRUCTURE_MSG "bad structure\n"
 * @brief A macro that save the bad structure message.
 */
#define BAD_STRUCTURE_MSG "bad structure\n"

// ------------------------------ functions -----------------------------
/**
 * @brief Check the parenthesis.
 * @param fpointer pointer to file.
 * @return 1 for good, 0 threwise.
 */
int checkParenthesis(FILE* fpointer)
{
    // Counter for each type of bracket '<','{','[','('
    int bracketType1Counter = 0, bracketType2Counter = 0, bracketType3Counter = 0,
            bracketType4Counter = 0;
    char singleChar;
    while ((singleChar = (char) fgetc(fpointer)) != EOF)
    {
        switch (singleChar)
        {
            case OPEN_BRACKET_TYPE_1:
                bracketType1Counter++;
                break;
            case OPEN_BRACKET_TYPE_2:
                bracketType2Counter++;
                break;
            case OPEN_BRACKET_TYPE_3:
                bracketType3Counter++;
                break;
            case OPEN_BRACKET_TYPE_4:
                bracketType4Counter++;
                break;

            case CLOSE_BRACKET_TYPE_1:
                bracketType1Counter--;
                break;
            case CLOSE_BRACKET_TYPE_2:
                bracketType2Counter--;
                break;
            case CLOSE_BRACKET_TYPE_3:
                bracketType3Counter--;
                break;
            case CLOSE_BRACKET_TYPE_4:
                bracketType4Counter--;
                break;
            default:
                break;
        }
        // Checks there are no more closing brackets than opening
        if (bracketType1Counter < 0 || bracketType2Counter < 0 || bracketType3Counter < 0 ||
            bracketType4Counter < 0)
        {
            return 0;
        }
    }
    // Checks all brackets are balanced
    if (bracketType1Counter != 0 || bracketType2Counter != 0 || bracketType3Counter != 0 ||
        bracketType4Counter != 0)
    {
        return 0;
    }
    return 1;
}

/**
 * @brief The main function.
 * @param argc number of arguments
 * @param argv arrray of arguments
 * @return 0, to tell the system the execution ended without errors. 1 otherwise.
 */
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, SUPPLY_FILE_ERROR);
        return 1;
    }

    FILE* fpointer = fopen(argv[1], "r"); // Try to open the file
    if(!fpointer)
    {
        fprintf(stderr, OPEN_FILE_ERROR, &argv[1]);
        return 1;
    }

    if (checkParenthesis(fpointer))
    {
        printf(OK_MSG);
    }
    else
    {
        printf(BAD_STRUCTURE_MSG);
    }
    fclose(fpointer);
    return 0;
}

