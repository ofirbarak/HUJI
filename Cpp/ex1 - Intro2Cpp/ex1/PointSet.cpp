// PointSet.cpp
#include "PointSet.h"
#define INIT_ARRAY_SIZE 1
#define INIT_LAST_POINT_POSITION 0

// --------------------------------------------------------------------------------------
// This file contains the implementation of the class PointSet.
// --------------------------------------------------------------------------------------
/**
 * @brief Constuctor
 */
PointSet::PointSet() : _arraySize(INIT_ARRAY_SIZE),
                        _lastPointPosition(INIT_LAST_POINT_POSITION),
                       _pointSet(new Point[INIT_ARRAY_SIZE])
{
//    _initSet(_pointSet, _arraySize);
}

/**
 * @brief Copy constructor
 * @param p  pointSet
 */
PointSet::PointSet(const PointSet &p)
{
    _arraySize = p._arraySize;
    _lastPointPosition = p._lastPointPosition;
    _pointSet = new Point[_arraySize];
    for (int i = 0; i < _lastPointPosition; ++i)
    {
        _pointSet[i] = p._pointSet[i];
    }
}

/**
 * @brief Destructor
 */
PointSet::~PointSet()
{
}

/**
 * @brief Add point to sets
 * @param p point to add
 * @return return true if point was added, false otherwise
 */
bool PointSet::add(Point p)
{
    if (_find(p) != -1)
    {
        return false;
    }
    if (_lastPointPosition == _arraySize)
    {   // Increase array size
        int newArraySize = _arraySize * 2;
        Point *newPointSet = new Point[newArraySize];
        std::copy(_pointSet, _pointSet + _arraySize, newPointSet);
        delete(_pointSet);
//        _initSet(newPointSet, newArraySize);
//        for (int i = 0; i < _arraySize; ++i)
//        {
//            newPointSet[i] = _pointSet[i];
//        }
        _arraySize = newArraySize;
        _pointSet = newPointSet;
    }
    _pointSet[_lastPointPosition++] = p;
    return true;
}

/**
 * @brief Check if point already exists in set
 * @param p point
 * @return index if yes, -1 otherwise
 */
int PointSet::_find(Point &p) const
{
    for (int i = 0; i < _lastPointPosition; ++i)
    {
        if (_pointSet[i] == p)
        {
            return i;
        }
    }
    return -1;
}

/**
 * @brief returns the set's size
 * @return the set's size
 */
int PointSet::size() const
{
    return _lastPointPosition;
}

/**
 * @brief remove a point from the set
 * @param p point to remove
 * @return true if removed, falase otherwise
 */
bool PointSet::remove(Point &p)
{
    int index = _find(p);
    if (index == -1)
    {
        return false;
    }
//    delete(_pointSet[index]); // Delete the object pointed to
    _pointSet[index] = _pointSet[_lastPointPosition--];
    return true;
}

/**
 * @brief to string function
 * @return a string represntation
 */
std::string PointSet::toString()
{
    std::string out = "";
    for (int i = 0; i < _lastPointPosition; ++i)
    {
        out += _pointSet[i].toString() + "\n";
    }
    return out;
}

/**
 * @brief free set
 */
void PointSet::freeSet()
{
//    for (int i = 0; i < _lastPointPosition; ++i)
//    {
//        delete(_pointSet[i]);
//    }
    delete(_pointSet);
}

/**
 * @brief equals operator overloading
 * @param p point set
 * @return true if equals, false otherwise
 */
bool PointSet::operator==(PointSet const &p) const
{
    if (_lastPointPosition != p._lastPointPosition)
    {
        return false;
    }
    for (int i = 0; i < _lastPointPosition; ++i)
    {
        if (p._find(_pointSet[i]) == -1)
        {
            return false;
        }
    }
    return true;
}

/**
 * @brief not equals operator overloading
 * @param p point set
 * @return true if not equals, false otherwise
 */
bool PointSet::operator!=(PointSet const &p) const
{
    return !(*this == p);
}

/**
 * @brief subtraction operator overloading
 * @param p point set
 * @return new point set without the points in the second set
 */
PointSet PointSet::operator-(const PointSet &p)
{
    PointSet newP;
    for (int i = 0; i < _lastPointPosition; ++i)
    {
        if (p._find(_pointSet[i]) == -1)
        {
            newP.add(_pointSet[i]);
        }
    }
    return newP;
}

/**
 * @brief intersaction operator oveloading
 * @param p point set
 * @return the intersaction between two sets
 */
PointSet PointSet::operator&(const PointSet &p)
{
    PointSet newPointSet;
    for (int i = 0; i < _lastPointPosition; ++i)
    {
        if (p._find(_pointSet[i]) != -1)
        {
            newPointSet.add(_pointSet[i]);
        }
    }
    return newPointSet;
}

/**
 * @brief assignment operator oveloading
 * @param p point set
 * @return reference to current set
 */
PointSet & PointSet::operator =(const PointSet &p)
{
    delete(_pointSet);
    _arraySize = p._arraySize;
    _lastPointPosition = p._lastPointPosition;
    _pointSet = new Point[_arraySize];
    for (int i = 0; i < p._lastPointPosition; ++i)
    {
        _pointSet[i] = p._pointSet[i];
    }
    return *this;
}



