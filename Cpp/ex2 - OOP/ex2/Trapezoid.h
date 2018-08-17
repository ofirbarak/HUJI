#ifndef EX2_TRAPEZOID_H
#define EX2_TRAPEZOID_H

#include "Shape.h"

/**
 * Class represents a trapezoid shape
 */
class Trapezoid : public Shape
{
private:

public:
    /**
     * @brief Constructor
     * @param p1 point 1
     * @param p2 point 2
     * @param p3 point 3
     * @param p4 point 4
     */
    Trapezoid(Point p1, Point p2, Point p3, Point p4);

    /**
     * @brief Destructor
     */
    ~Trapezoid();

    /**
     * @brief Calculate the shape's area
     * @return the shape's area
     */
    CordType area() const override;

    /**
     * @brief Print shape
     */
    void printShape();
};


#endif //EX2_TRAPEZOID_H
