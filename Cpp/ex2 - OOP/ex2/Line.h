#ifndef EX2_LINE_H
#define EX2_LINE_H

#include "Point.h"

/**
 * Class represents a line
 */
class Line
{
private:
    /**
     * @brief First point
     */
    Point _p1;

    /**
     * @brief Second point
     */
    Point _p2;
public:
    /**
    * @brief Constructor
    * @param p1 point 1
    * @param p2 point 2
    */
    Line(Point p1, Point p2);

    /**
     * @brief Destructor
     */
    ~Line();

    /**
     * @brief Check if two lines is intersect
     * @param l1 line 1
     * @param l2 line 2
     * @return true if yes, false otherwise
     */
    static bool hasIntersection(const Line &l1, const Line &l2);

    /**
     * @brief Returns the second point
     * @return the second point
     */
    Point getSecondPoint() const;

    /**
     * @brief Returns the first point
     * @return the first point
     */
    Point getFirstPoint() const;

    /**
     * @brief Returns difference in x coordinates between the two points
     * @return difference in x coordinates between the two points
     */
    CordType getXDiff() const;
};


#endif //EX2_LINE_H
