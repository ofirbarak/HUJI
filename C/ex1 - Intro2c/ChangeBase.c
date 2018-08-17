/**
 * @file ChangeBase.c
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 9 Aug 2016
 *
 * @brief System converts numbers from base 1 to base 2.
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * The system converts numbers from base 1 to base 2.
 * Input  : <Base 1> <Base 2> <A number>.
 * Process: Check the given number is in correct base - done bby passing the digits
 *      and check each digit. After that convert the number to decimal base and then to the
 *      wanted base.
 * Output : The number in asked base, or error if occured.
 */

// ------------------------------ includes ------------------------------
#include <stdio.h>

// -------------------------- const definitions -------------------------
/**
 * @def DECIMAL_BASE 10
 * @brief A macro that save the decimal base.
 */
#define DECIMAL_BASE 10

/**
 * @def NUMBER_OF_ARGUMENTS 3
 * @brief A macro that save the number of arguments.
 */
#define NUMBER_OF_ARGUMENTS 3

/**
 * @def ARRAY_SIZE 50
 * @brief A macro that save the maximal array size that save the converted number.
 */
#define ARRAY_SIZE 50

/**
 * @def ERROR_MSG "invalid!!\\n"
 * @brief A macro that save the error message.
 */
#define ERROR_MSG "invalid!!\\n"

/**
 * @def INPUT_FORMAT "%d^%d^%d^"
 * @brief A macro that save the input format.
 */
#define INPUT_FORMAT "%d^%d^%d^"

// ------------------------------ functions -----------------------------
/**
 * @brief Returns the power of a number
 * @param num A number
 * @param power power to raise
 * @return a^b
 */
int powerANumber(int num, int power)
{
    int retValue = 1;
    for (; power > 0; power--)
    {
        retValue *= num;
    }
    return retValue;
}

/**
 * @brief Checks a given number is in correct base
 * @param num A number
 * @param base the base
 * @return A number in correct base
 */
int isNumberInCorrectBase(int num, const int base)
{
    while (num % DECIMAL_BASE < base && num != 0)
    {
        num /= DECIMAL_BASE;
    }
    if (num == 0)
    {
        return 1;
    }
    return 0;
}

/**
 * @brief Converts a number to decimal base
 * @param num A numebr
 * @param base the base
 * @return the number convert to decimal
 */
int convertToDecimal(int num, const int base)
{
    int decimalNumber = 0, i = 0;
    while (num != 0)
    {
        decimalNumber += (num % DECIMAL_BASE) * (powerANumber(base, i));
        i++;
        num /= DECIMAL_BASE;
    }
    return decimalNumber;
}

/**
 * @brief Converts number from decimal to the given base and prints the result
 * @param num A number
 * @param base the base
 */
void convertAndPrintFromDecimal(int num, const int base)
{
    char res[ARRAY_SIZE];
    char* pointer;
    pointer = &res[ARRAY_SIZE-1];
    *pointer = '\0';
    if (num == 0)
    {
        (pointer)--;
        *pointer = '0';
    }
    while (num != 0)
    {
        pointer--;
        *pointer = (char)(num % base + '0');
        num = num / base;
    }
    printf("%s\n", pointer);
}

/**
 * @brief The main function.
 * @return 0, to tell the system the execution ended without errors. 1 otherwise.
 */
int main()
{
    int orgBase, newBase, numberInOrgBase;
    if (scanf(INPUT_FORMAT, &orgBase, &newBase, &numberInOrgBase) != NUMBER_OF_ARGUMENTS)
    {
        fprintf(stderr, ERROR_MSG);
        return 1;
    }
    // Check given number is in correct given base
    if (!isNumberInCorrectBase(numberInOrgBase, orgBase))
    {
        fprintf(stderr, ERROR_MSG);
        return 1;
    }
    convertAndPrintFromDecimal(convertToDecimal(numberInOrgBase, orgBase), newBase);
    return 0;
}

/*
 * The algorithm I used is: check the given number is in correct base - done bby passing the digits
 * and check each digit. After that convert the number to decimal base and then to the wanted base.
 * I took the algorithm for convert the number to decimal base and from decimal to given base from
 * http://www.cut-the-knot.org/recurrence/conversion.shtml
 * The algorithm runs in O(log n)
 */
