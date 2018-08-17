#include "Line.h"
#include "Shape.h"

/**
 * @brief Constructor
 * @param p1 point 1
 * @param p2 point 2
 */
Line::Line(Point p1, Point p2) : _p1(p1), _p2(p2)
{
}

/**
 * @brief Destructor
 */
Line::~Line()
{
}

/**
 * @brief Check if two lines is intersect
 * @param l1 line 1
 * @param l2 line 2
 * @return true if yes, false otherwise
 */
bool Line::hasIntersection(const Line &l1, const Line &l2)
{
    return Shape::calcDeterminant(l1.getFirstPoint(), l2) *
        Shape::calcDeterminant(l1.getSecondPoint(), l2) < 0 &&
        Shape::calcDeterminant(l2.getFirstPoint(), l1) *
        Shape::calcDeterminant(l2.getSecondPoint(), l1) < 0;
}

/**
 * @brief Returns the second point
 * @return the second point
 */
Point Line::getSecondPoint() const
{
    return _p2;
}

/**
 * @brief Returns the first point
 * @return the first point
 */
Point Line::getFirstPoint() const
{
    return _p1;
}

/**
 * @brief Returns difference in x coordinates between the two points
 * @return difference in x coordinates between the two points
 */
CordType Line::getXDiff() const
{
    CordType x = _p2.getX() - _p1.getX();
    if (x < 0)
    {
        x *= -1;
    }
    return x;
}

