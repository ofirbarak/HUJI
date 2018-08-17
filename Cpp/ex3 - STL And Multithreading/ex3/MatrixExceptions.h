#ifndef EX3_MATRIXEXCEPTIONS_H
#define EX3_MATRIXEXCEPTIONS_H

#include <exception>
/**
 * Exception class - excluded from 'Matrix.hpp' for better understanding, easy
 * to add more classes
 */
class MatrixException : public std::exception
{
    /**
     * what implementation
     */
    const char * what () const throw ()
    {
        return "if 1 of the dimension is 0 than there other had to be 0 too";
    }
};

/**
 * Exception class - different sizes
 */
class MatrixAdditionException : public std::exception
{
    /**
     * what implementation
     */
    const char * what () const throw ()
    {
        return "cannot addition matrices if different sizes.";
    }
};

#endif //EX3_MATRIXEXCEPTIONS_H
