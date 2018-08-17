#ifndef EX3_MATRIX_HPP
#define EX3_MATRIX_HPP

#include <stdexcept>
#include <vector>
#include <ostream>
#include <iostream>
#include <thread>
#include <vector>

#include "Matrix.h"

#define BAD_ARGUMENTS "bad arguments"
#define DEFAULT_SIZE 1, 1
#define TAB "\t"
#define NEW_LINE "\n"
#define MSG "Generic Matrix mode changed to (Parallel|non-Parallel) mode."


/**
 * @brief Default constructor
 */
template <class T>
Matrix<T>::Matrix() : Matrix(DEFAULT_SIZE)
{
}

/**
 * @brief Prameters constructor
 * @param rows number of init rows
 * @param cols number of init colums
 */
template <class T>
Matrix<T>::Matrix(unsigned int rows, unsigned int cols) : _rows(rows), _cols(cols),
                                                          _matrix(rows * cols, T())
{
}

/**
 * @brief Copy constructor
 * @param matrix the matrix to copy
 */
template <class T>
Matrix<T>::Matrix(const Matrix<T> &other) : Matrix(other._rows, other._cols, other._matrix)
{
}

/**
 * @brief Move constructor
 * @param other matrix to move from
 */
template <class T>
Matrix<T>::Matrix(Matrix<T> && other)
{
    _rows = std::move(other._rows);
    _cols = std::move(other._cols);
    _matrix = std::move(other._matrix);
}

/**
 * @brief Parameters constructors
 * @param rows number of rows
 * @param cols number of colums
 * @param cells cells
 */
template <class T>
Matrix<T>::Matrix(unsigned int rows, unsigned int cols, const std::vector<T> &cells) : Matrix
                                                                                               (rows, cols)
{
    if (rows != cols && (rows == 0 || cols == 0))
    {
        throw MatrixException();
    }
    unsigned int index = 0;
    for (const_iterator iter = cells.begin(); iter != cells.end(); iter++, index++)
    {
        _matrix[index] = *iter;
    }
}

/**
 * @brief Destructor
 */
template <class T>
Matrix<T>::~Matrix()
{
}

/**
 * @brief Assignment operator
 * @param other other matrix
 * @return the new matrix
 */
template <class T>
Matrix<T>& Matrix<T>::operator=(const Matrix<T> &other)
{
    if (&other != this)
    {
        _rows = other._rows;
        _cols = other._cols;
        _matrix = other._matrix;
    }
    return *this;
}


/**
 * @brief Plus operator
 * @param other other matrix
 * @return the new matrix
 */
template <class T>
Matrix<T> Matrix<T>::operator+(const Matrix &other) const
{
    if (!(_rows == other._rows && _cols == other._cols))
    {
        throw MatrixAdditionException();
    }
    if (_parallel)
    {
        return otherAdd(other);
    }
    Matrix plusMatrix(other._rows, other._cols);
    for (unsigned int i = 0; i < _rows; ++i)
    {
        for (unsigned int j = 0; j < _cols; ++j)
        {
            plusMatrix(i, j) = (*this)(i, j) + other(i, j);
        }
    }
    return plusMatrix;
}


/**
 * @brief Subtraction operator
 * @param other other matrix
 * @return the new matrix
 */
template <class T>
Matrix<T> Matrix<T>::operator-(const Matrix<T> &other) const
{
    if (!(_rows == other._rows && _cols == other._cols))
    {
        throw std::exception();
    }
    Matrix<T> subMatrix(other._rows, other._cols);
    for (unsigned int i = 0; i < _rows; ++i)
    {
        for (unsigned int j = 0; j < _cols; ++j)
        {
            subMatrix(i, j) = (*this)(i, j) - other(i, j);
        }
    }
    return subMatrix;
}

/**
 * @brief Multiplition operator
 * @param other other matrix
 * @return the new matrix
 */
template <class T>
Matrix<T> Matrix<T>::operator*(const Matrix<T> &other) const
{
    if (!(_cols == other._rows && isSquareMatrix() && other.isSquareMatrix()))
    {
        throw std::exception();
    }
    if (_parallel)
    {
        return otherMul(other);
    }
    T sum;
    Matrix mulMatrix(other._rows, other._cols);
    for (unsigned int i = 0; i < _rows; ++i)
    {
        sum = 0;
        for (unsigned int j = 0; j < other._cols; ++j)
        {
            for (unsigned int k = 0; k < _cols; ++k)
            {
                sum += (*this)(i, k) * other(k, j);
            }
            mulMatrix(i, j) = sum;
        }
    }
    return mulMatrix;
}

//template <class T>
//std::ostream& Matrix<T>::operator<<(std::ostream &os, const Matrix<T> &matrix)
//{
//    for (unsigned int i = 0; i < matrix._rows; ++i)
//    {
//        for (unsigned int j = 0; j < matrix._cols; ++j)
//        {
//            os << matrix(i, j) << TAB;
//        }
//        os << NEW_LINE;
//    }
//    return os;
//}


/**
 * @brief Compare operator
 * @param other other matrix
 * @return the new matrix
 */
template <class T>
bool Matrix<T>::operator==(const Matrix<T> &other) const
{
    if (_rows == other._rows && _cols == other._cols)
    {
        const_iterator thisIter = _matrix.begin(), otherIter = other._matrix.begin();
        for (; thisIter != _matrix.end(); thisIter++, otherIter++)
        {
            if (*thisIter != *otherIter)
            {
                return false;
            }
        }
        return true;
    }
    return false;
}

// operator != created automatically

/**
 * @brief Transpose matrix
 * @return the new matrix
 */
template <>
Matrix<Complex> Matrix<Complex>::trans()
{
    Matrix<Complex> transMatrix = *this;
    Complex temp;
    for (unsigned int i = 0; i < _rows; ++i)
    {
        for (unsigned int j = i; j < _cols; ++j)
        {
            temp = transMatrix(i, j).conj();
            transMatrix(i, j) = transMatrix(j, i).conj();
            transMatrix(j, i) = temp;
        }
    }
    return transMatrix;
}

/**
 * @brief Transpose matrix
 * @return the new matrix
 */
template <class T>
Matrix<T> Matrix<T>::trans()
{
    Matrix<T> transMatrix = *this;
    T temp;
    for (unsigned int i = 0; i < _rows; ++i)
    {
        for (unsigned int j = i; j < _cols; ++j)
        {
            temp = transMatrix(i, j);
            transMatrix(i, j) = transMatrix(j, i);
            transMatrix(j, i) = temp;
        }
    }
    return transMatrix;
}

/**
 * @brief Returns true iff matrix is square
 * @return true iff matrix is square
 */
template <class T>
bool Matrix<T>::isSquareMatrix() const
{
    return _rows == _cols;
}

/**
 * @brief Operator overloading function call
 * @param row row number
 * @param col column number
 * @return copy of value in position [row, col]
 */
template <class T>
T Matrix<T>::operator()(unsigned int row, unsigned int col) const
{
    if (row < 0 || col < 0  || row > _rows || col > _cols)
    {
        throw std::invalid_argument(BAD_ARGUMENTS);
    }
    return _matrix[row * _cols + col];
}

/**
 * @brief Operator overloading function call
 * @param row row number
 * @param col column number
 * @return reference to the value in position [row, col]
 */
template <class T>
T &Matrix<T>::operator()(unsigned int row, unsigned int col)
{
    if (row < 0 || col < 0  || row > _rows || col > _cols)
    {
        throw std::invalid_argument(BAD_ARGUMENTS);
    }
    return _matrix[row * _cols + col];
}

/**
 * @brief Returns the begin of iterator
 * @return the begin of iterator
 */
template <class T>
typename std::vector<T>::const_iterator Matrix<T>::begin() const
{
    return _matrix.begin();
}

/**
 * @brief Returns the begin of iterator
 * @return the begin of iterator
 */
template <class T>
typename std::vector<T>::const_iterator Matrix<T>::end() const
{
    return _matrix.end();
}

/**
 * @brief Returns number of rows
 * @return number of rows
 */
template <class T>
unsigned int Matrix<T>::rows() const
{
    return _rows;
}

/**
 * @brief Returns number of columns
 * @return number of columns
 */
template <class T>
unsigned int Matrix<T>::cols() const
{
    return _cols;
}

/**
 * @brief Add helper function for thread
 */
template <class T>
void Matrix<T>::callFromThread(Matrix &changeMatrix, const Matrix &other, int row) const
{
    for (unsigned int j = 0; j < _cols; ++j)
    {
        changeMatrix(row, j) = (*this)(row, j) + other(row, j);
    }
}

/**
 * @brief Thread add function
 * @return the matrix
 */
template <class T>
Matrix<T> Matrix<T>::otherAdd(const Matrix &other) const
{
    std::cout << MSG;
    if (!(_rows == other._rows && _cols == other._cols))
    {
        throw MatrixAdditionException();
    }
    Matrix plusMatrix(other._rows, other._cols);
    std::vector<std::thread> threads;
    for (unsigned int k = 0; k < _rows; ++k)
    {
        threads.push_back(std::thread(&Matrix<T>::callFromThread,
                                      this, std::ref(plusMatrix), std::ref(other), k));
    }
    for (auto& th : threads)
    {
        th.join();
    }
    return plusMatrix;
}

/**
 * @brief Mul helper function
 */
template <class T>
void Matrix<T>::callFromThreadMul(Matrix &mulMatrix, const Matrix &other, int i) const
{
    T sum = 0;
    for (unsigned int j = 0; j < other._cols; ++j)
    {
        for (unsigned int k = 0; k < _cols; ++k)
        {
            sum += (*this)(i, k) * other(k, j);
        }
        mulMatrix(i, j) = sum;
    }
}

/**
 * @brief Mul thread function
 * @return the matrix
 */
template <class T>
Matrix<T> Matrix<T>::otherMul(const Matrix &other) const
{
    std::cout << MSG;
    if (!(_rows == other._rows && _cols == other._cols))
    {
        throw MatrixAdditionException();
    }
    Matrix mulMatrix(other._rows, other._cols);
    std::vector<std::thread> threads;
    for (unsigned int i = 0; i < _rows; ++i)
    {
        threads.push_back(std::thread(&Matrix<T>::callFromThreadMul,
                                      this, std::ref(mulMatrix), std::ref(other), i));
    }
    for (auto th = threads.begin(); th != threads.end(); th++)
    {
        th->join();
    }
    return mulMatrix;
}

#endif //EX3_MATRIX_HPP
