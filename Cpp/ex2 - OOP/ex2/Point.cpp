#include "Point.h"

/**
 * @brief Constructor
 * @param x x coordinate
 * @param y y coordinate
 */
Point::Point(CordType x, CordType y) : _x(x), _y(y)
{
}

/**
 * @brief Destructor
 */
Point::~Point()
{
}

/**
 * @brief Returns x coordinate
 * @return x coordinate
 */
CordType Point::getX() const
{
    return _x;
}

/**
 * @brief Returns y coordinate
 * @return y coordinate
 */
CordType Point::getY() const
{
    return _y;
}

/**
 * @brief Overloading == operator
 * @param p1 Point to copare to
 * @return True if equals, false otherwise
 */
bool Point::operator ==(Point const &p1) const
{
    CordType defX = p1._x - _x;
    CordType defY = p1._y - _y;
    return (defX < EPSILON && defX > -EPSILON) && (defY < EPSILON && defY > -EPSILON);
}