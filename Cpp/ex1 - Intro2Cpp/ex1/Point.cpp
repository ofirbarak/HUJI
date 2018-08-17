// Point.cpp
#include <string>
#include "Point.h"

// --------------------------------------------------------------------------------------
// This file contains the implementation of the class Point.
// --------------------------------------------------------------------------------------
/**
 * @brief Constuctor
 */
Point::Point()
{
}

/**
 * @brief Copy constructor
 * @param p point
 */
Point::Point(const int x, const int y) : _x(x), _y(y)
{
}

/**
 * @brief Destructor
 */
Point::~Point()
{
}

/**
 * @brief ToString function
 * @return string represntation
 */
std::string Point::toString()
{
    return std::to_string(_x) + "," + std::to_string(_y);
}

/**
 * @brief Set point values
 * @param x x coordinate
 * @param y y coordinate
 */
void Point::set(const int x, const int y)
{
    _x = x;
    _y = y;
}

/**
 * @brief Operator funtion overloading
 * @param other point
 * @return true if equals, false otherwise
 */
bool Point::operator ==(Point const & other)
{
    return _x == other._x && _y == other._y;
}