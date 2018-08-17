#ifndef EX2_SHAPE_H
#define EX2_SHAPE_H

#include <vector>
#include <string>
#include "Point.h"
#include "Line.h"

using namespace std;

/**
 * Class that represents a simple shape
 */
class Shape
{
private:
    /**
     * @brief Check if s1 contained in s2
     * @param s1 shape 1
     * @param s2 shape e2
     * @return true if yes, false otherwise
     */
    static bool _checkContained(Shape &s1, Shape &s2);
protected:
    /**
     * @brief Vector represents the shape's lines
     */
    vector<Line> _lines;

    /**
     * @brief Save the shape name
     */
    const string _shapeName;

    /**
     * @brief Constructor
     * @param name name of shape
     */
    Shape(const string name);

    /**
     * @brief Add lines - connect new point to the last one, check two points are not the same
     * @param newPoint point to add
     * @return true if added, false otherwise
     */
    bool addLine(const Point p1, const Point p2);
public:
    /**
     * @brief Destructor
     */
    virtual ~Shape();

    /**
     * @brief Calculate the shape's area
     * @return the shape's area
     */
    virtual CordType area() const = 0;

    /**
     * @brief Print shape
     */
    virtual void printShape() = 0;

    /**
     * @brief Check if s1 has intersection with s2
     * @param s1 Shape 1
     * @param s2 Shape 2
     * @return true if yes, false otherwise
     */
    static bool hasIntersection(Shape &s1, Shape &s2);

    /**
     * @brief Returns the coordinates
     * @return the coordinates
     */
    vector<Line> getLines();

    /**
     * @brief Calculate the determinant
     * @param p1 point 1
     * @param l Line
     * @return the determinant
     */
    static CordType calcDeterminant(const Point &p, const Line &l);
};


#endif //EX2_SHAPE_H
