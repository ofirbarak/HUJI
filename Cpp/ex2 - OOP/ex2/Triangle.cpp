#include <iostream>
#include "Triangle.h"
#include "PrintOuts.h"
/**
 * @brief Constructor
 * @param p1 point 1
 * @param p2 point 2
 * @param p3 point 3
 */
Triangle::Triangle(Point p1, Point p2, Point p3) : Shape("Triangle")
{

    addLine(p1, p2);
    addLine(p2, p3);
    addLine(p3, p1);
}

/**
 * @brief Destructor
 */
Triangle::~Triangle()
{
}

/**
 * @brief Calculate the shape's area
 * @return the shape's area
 */
CordType Triangle::area() const
{
    CordType area = calcDeterminant(_lines[0].getSecondPoint(),
                           Line(_lines[1].getSecondPoint(), _lines[2].getSecondPoint()));
    if (area < 0)
    {
        area *= -1;
    }
    return area;
}

/**
 * @brief Print shape
 */
void Triangle::printShape()
{
    Point p1 = _lines[0].getFirstPoint();
    Point p2 = _lines[1].getFirstPoint();
    Point p3 = _lines[2].getFirstPoint();
    printTrig(p1.getX(), p1.getY(), p2.getX(), p2.getY(), p3.getX(), p3.getY());
}