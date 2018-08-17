#include <algorithm>
#include "Shape.h"

/**
 * @brief Constructor
 * @param name name of shape
 */
Shape::Shape(const string name) : _shapeName(name)
{
}

/**
 * @brief Destructor
 */
Shape::~Shape()
{
}

/**
 * @brief Add lines - connect new point to the last one, check two points are not the same
 * @param newPoint point to add
 * @return true if added, false otherwise
 */
bool Shape::addLine(Point p1, Point p2)
{
    // Check for 0 length
    if (p1 == p2)
    {
        return false;
    }
    _lines.push_back(Line(p1, p2));
    return true;
}

/**
 * @brief Returns the coordinates
 * @return the coordinates
 */
vector<Line> Shape::getLines()
{
    return _lines;
}

/**
 * @brief Calculate the determinant
 * @param p1 point 1
 * @param l Line
 * @return the determinant
 */
CordType Shape::calcDeterminant(const Point &p, const Line &l)
{
    return 0.5 * (p.getX() * (l.getFirstPoint().getY() - l.getSecondPoint().getY()) -
           l.getFirstPoint().getX() * (p.getY() - l.getSecondPoint().getY()) +
           l.getSecondPoint().getX() * (p.getY() - l.getFirstPoint().getY()));
}

/**
 * @brief Check if s1 contained in s2
 * @param s1 shape 1
 * @param s2 shape e2
 * @return true if yes, false otherwise
 */
bool Shape::_checkContained(Shape &s1, Shape &s2)
{
    // Pass all s1 points and check they are in the same side
    CordType currentPointSide = 0;
    vector<Line> s1Lines = s1.getLines(), s2Lines = s2.getLines();
    std::vector<Line>::iterator it2;
    for (std::vector<Line>::iterator it1 = s1Lines.begin() ; it1 != s1Lines.end(); ++it1)
    {
        it2 = s2Lines.begin();
        currentPointSide = calcDeterminant(it1->getFirstPoint(), *it2);
        for (; it2 != s2Lines.end(); ++it2)
        {
            if (calcDeterminant(it1->getFirstPoint(), *it2) * currentPointSide < 0)
            {
                return false;
            }
        }
    }
    return true;
}

/**
 * @brief Check if s1 has intersection with s2
 * @param s1 Shape 1
 * @param s2 Shape 2
 * @return true if yes, false otherwise
 */
bool Shape::hasIntersection(Shape &s1, Shape &s2)
{
    // Check if s1 contained in s2 ro thr opposite
    if (_checkContained(s1, s2) || _checkContained(s2, s1))
    {
        return true;
    }
    // Check if lines of s1 has intersection with lines of s2
    std::vector<Line>::iterator it1, it2;
    vector<Line> s1Lines = s1.getLines(), s2Lines = s2.getLines();
    for (it1 = s1Lines.begin() ; it1 != s1Lines.end(); ++it1)
    {
        for (it2 = s2Lines.begin() ; it2 != s2Lines.end(); ++it2)
        {
            if (Line::hasIntersection(*it1, *it2))
            {
                return true;
            }
        }
    }
    return false;
}