// PointSet.h
#ifndef EX1_POINTSET_H
#define EX1_POINTSET_H

#include <string>
#include "Point.h"

/**
 * @brief A set of points class
 */
class PointSet
{
public:
    /**
     * @brief Constuctor
     */
    PointSet();

    /**
     * @brief Copy constructor
     * @param p  pointSet
     */
    PointSet(const PointSet &p);

    /**
     * @brief Destructor
     */
    ~PointSet();

    /**
     * @brief to string function
     * @return a string represntation
     */
    std::string toString();

    /**
     * @brief Add point to sets
     * @param p point to add
     * @return return true if point was added, false otherwise
     */
    bool add(Point p);

    /**
     * @brief remove a point from the set
     * @param p point to remove
     * @return true if removed, falase otherwise
     */
    bool remove(Point &p);

    /**
     * @brief returns the set's size
     * @return the set's size
     */
    int size() const;

    /**
     * @brief free set
     */
    void freeSet();

    /**
     * @brief return the set
     * @return the set
     */
    Point *getSet() const
    {
        return _pointSet;
    }

    /**
     * @brief not equals operator overloading
     * @param p point set
     * @return true if not equals, false otherwise
     */
    bool operator !=(PointSet const &p) const;

    /**
     * @brief equals operator overloading
     * @param p point set
     * @return true if equals, false otherwise
     */
    bool operator ==(PointSet const &p) const;

    /**
     * @brief subtraction operator overloading
     * @param p point set
     * @return new point set without the points in the second set
     */
    PointSet operator -(const PointSet &p);

    /**
     * @brief intersaction operator oveloading
     * @param p point set
     * @return the intersaction between two sets
     */
    PointSet operator &(const PointSet &p);

    /**
     * @brief assignment operator oveloading
     * @param p point set
     * @return reference to current set
     */
    PointSet &operator =(const PointSet &p);
private:
    /*
     * The array size, and the size fo the set
     */
    int _arraySize, _lastPointPosition;

    /*
     * pointer to array of points
     */
    Point *_pointSet;

    /*
     * @brief Check if point already exists in set
     * @param p point
     * @return index if yes, -1 otherwise
     */
    int _find(Point &p) const;

    /*
     * @brief Initulize list with null pointers
     * @param pointSet the point set
     * @param size size of set
     */
//    void _initSet(Point *pointSet, int size);
};


#endif //EX1_POINTSET_H
