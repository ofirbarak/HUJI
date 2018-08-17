#include <iostream>
#include "Trapezoid.h"
#include "PrintOuts.h"

/**
 * @brief Constructor
 * @param p1 point 1
 * @param p2 point 2
 * @param p3 point 3
 * @param p4 point 4
 */
Trapezoid::Trapezoid(Point p1, Point p2, Point p3, Point p4) : Shape("Trapezoid")
{
    // Adds lines
    addLine(p1, p2);
    addLine(p2, p3);
    addLine(p3, p4);
    addLine(p4, p1);
}

/**
 * @brief Destructor
 */
Trapezoid::~Trapezoid()
{
}

/**
 * @brief Calculate the shape's area
 * @return the shape's area
 */
CordType Trapezoid::area() const
{
    CordType h = _lines[0].getFirstPoint().getY() - _lines[2].getFirstPoint().getY();
    if (h < 0)
    {
        h *= -1;
    }
    return 0.5 * h * (_lines[0].getXDiff() + _lines[2].getXDiff());
}

/**
 * @brief Print shape
 */
void Trapezoid::printShape()
{
    Point p1 = _lines[0].getFirstPoint();
    Point p2 = _lines[1].getFirstPoint();
    Point p3 = _lines[2].getFirstPoint();
    Point p4 = _lines[3].getFirstPoint();
    printTrapez(p1.getX(), p1.getY(), p2.getX(), p2.getY(), p3.getX(), p3.getY(),
                p4.getX(), p4.getY());
}