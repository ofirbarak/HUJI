//Point.h

#ifndef EX1_POINT_H
#define EX1_POINT_H

/**
 * @brief A poinnt class
 */
class Point
{
private:
    /**
     * @brief X and Y coordinates
     */
    int _x, _y;
public:
    /**
     * @brief Constuctor
     */
    Point();

    /**
     * @brief Copy constructor
     * @param x x coordinate
     * @param y y coordinate
     */
    Point(const int x, const int y);

    /**
     * @brief Destructor
     */
    ~Point();

    /**
     * @brief ToString function
     * @return string represntation
     */
    std::string toString();

    /**
     * @brief Set point values
     * @param x c coordinate
     * @param y y coordinate
     */
    void set(const int x, const int y);

    /**
     * @brief Operator funtion overloading
     * @param other point
     * @return true if equals, false otherwise
     */
    bool operator==(Point const & other);

    /**
     * @brief Get y coordinate
     * @return return y
     */
    int getY() const
    {
        return _y;
    }

    /**
     * @brief get x coordinate
     * @return return x
     */
    int getX() const
    {
        return _x;
    }
};


#endif //EX1_POINT_H
