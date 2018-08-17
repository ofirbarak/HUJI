#ifndef EX2_POINT_H
#define EX2_POINT_H

#include "Defs.h"

/**
 * Class represents a point
 */
class Point
{
private:
    /**
     * @brief X coordinate
     */
    CordType _x;

    /**
     * @brief Y coordinate
     */
    CordType _y;
public:
    /**
     * @brief Constructor
     * @param x x coordinate
     * @param y y coordinate
     */
    Point(const CordType x, const CordType y);

    /**
     * @brief Destructor
     */
    ~Point();

    /**
     * @brief Returns x coordinate
     * @return x coordinate
     */
    CordType getX() const ;

    /**
     * @brief Returns y coordinate
     * @return y coordinate
     */
    CordType getY() const ;

    /**
     * @brief Overloading == operator
     * @param p1 Point to copare to
     * @return True if equals, false otherwise
     */
    bool operator ==(Point const &p1) const;
};


#endif //EX2_POINT_H
