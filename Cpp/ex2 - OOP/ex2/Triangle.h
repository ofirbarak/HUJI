#ifndef EX2_TRIANGLE_H
#define EX2_TRIANGLE_H

#include "Shape.h"

/**
 * Class represents a triangle shape
 */
class Triangle : public Shape
{
public:
    /**
     * @brief Constructor
     * @param p1 point 1
     * @param p2 point 2
     * @param p3 point 3
     */
    Triangle(Point p1, Point p2, Point p3);

    /**
     * @brief Destructor
     */
    ~Triangle();

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


#endif //EX2_TRIANGLE_H
