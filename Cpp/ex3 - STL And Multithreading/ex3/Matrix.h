#ifndef EX3_MATRIX_H
#define EX3_MATRIX_H

#include <stdexcept>
#include <vector>
#include <ostream>
#include <iostream>
#include <thread>

#include "MatrixExceptions.h"
#include "Complex.h"

#define TAB "\t"
#define NEW_LINE "\n"

static bool _parallel;

/**
 * Matrix class
 */
template <class T>
class Matrix
{

private:
    unsigned int _rows;
    unsigned int _cols;
    std::vector<T> _matrix;
public:
    using const_iterator = typename std::vector<T>::const_iterator;
    /**
     * @brief Default constructor
     */
    Matrix();

    /**
     * @brief Prameters constructor
     * @param rows number of init rows
     * @param cols number of init colums
     */
    Matrix(unsigned int rows, unsigned int cols);

    /**
     * @brief Copy constructor
     * @param matrix the matrix to copy
     */
    Matrix(const Matrix<T> &matrix);

    /**
     * @brief Move constructor
     * @param other matrix to move from
     */
    Matrix(Matrix<T> && other);

    /**
     * @brief Parameters constructors
     * @param rows number of rows
     * @param cols number of colums
     * @param cells cells
     */
    Matrix(unsigned int rows, unsigned int cols, const std::vector<T>& cells);

    /**
     * @brief Destructor
     */
    ~Matrix();

    /**
     * @brief Assignment operator
     * @param other other matrix
     * @return the new matrix
     */
    Matrix<T> &operator=(const Matrix<T> & other);

    /**
     * @brief Plus operator
     * @param other other matrix
     * @return the new matrix
     */
    Matrix<T> operator+(const Matrix<T> & other) const;

    /**
     * @brief Subtraction operator
     * @param other other matrix
     * @return the new matrix
     */
    Matrix<T> operator-(const Matrix<T> & other) const;

    /**
     * @brief Multiplition operator
     * @param other other matrix
     * @return the new matrix
     */
    Matrix<T> operator*(const Matrix<T> & other) const;

    /**
     * @brief Compare operator
     * @param other other matrix
     * @return the new matrix
     */
    bool operator==(const Matrix<T> & other) const;

    /**
     * @brief Transpose matrix
     * @return the new matrix
     */
    Matrix<T> trans();

    /**
     * @brief Returns true iff matrix is square
     * @return true iff matrix is square
     */
    bool isSquareMatrix() const;

    /**
     * @brief Print operator
     * @param os object stream
     * @return object stream
     */
    friend std::ostream& operator<<(std::ostream &os, const Matrix<T> &matrix)
    {
        for (unsigned int i = 0; i < matrix._rows; ++i)
        {
            for (unsigned int j = 0; j < matrix._cols; ++j)
            {
                os << matrix(i, j) << TAB;
            }
            os << NEW_LINE;
        }
        return os;
    }

    /**
     * @brief Operator overloading function call
     * @param row row number
     * @param col column number
     * @return copy of value in position [row, col]
     */
    T operator()(unsigned int row, unsigned int col) const;

    /**
     * @brief Operator overloading function call
     * @param row row number
     * @param col column number
     * @return reference to the value in position [row, col]
     */
    T &operator()(unsigned int row, unsigned int col);

    /**
     * @brief Returns the begin of iterator
     * @return the begin of iterator
     */
    const_iterator begin() const;

    /**
     * @brief Returns the begin of iterator
     * @return the begin of iterator
     */
    const_iterator end() const;

    /**
     * @brief Returns number of rows
     * @return number of rows
     */
    unsigned int rows() const;

    /**
     * @brief Returns number of columns
     * @return number of columns
     */
    unsigned int cols() const;

    /**
     * @brief Set parallel
     */
    static void setParallel(bool toParallel)
    {
        _parallel = toParallel;
    }

    /**
     * @brief Add helper function for thread
     */
    void callFromThread(Matrix &changeMatrix, const Matrix &other, int row) const;

    /**
     * @brief Thread add function
     * @return the matrix
     */
    Matrix<T> otherAdd(const Matrix &other) const;

    /**
     * @brief Mul helper function
     */
    void callFromThreadMul(Matrix &mulMatrix, const Matrix &other, int i) const;

    /**
     * @brief Mul thread function
     * @return the matrix
     */
    Matrix<T> otherMul(const Matrix &other) const;
};


#endif //EX3_MATRIX_H
