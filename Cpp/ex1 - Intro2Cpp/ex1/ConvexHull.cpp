/**
 * @file ConvexHull.cpp
 * @author  Ofir Birka <ofir.birka@mail.huji.ac.il>
 * @version 1.0
 * @date 6 sep 2016
 *
 * @brief Graham's algorithm implementation
 *
 * @section LICENSE
 * This program is not a free software;
 *
 * @section DESCRIPTION
 * Graham's algorithm implementation
 */
// ------------------------------ includes ------------------------------
#include <iostream>
#include <algorithm>
#include "PointSet.h"

#define FIRST_CELL 0
using namespace std;
// ------------------------------ globals -----------------------------
/**
 * @brief Save lowest rightmost point
 */
Point minPoint;

// ------------------------------ functions -----------------------------
/**
 * @brief Compare function, compare by coordinates
 * @param curr current point
 * @param other other point
 * @return >0 if cuurent bigger, <0 if ither bigger, 0 if equals
 */
int compareToFindMinimum(const Point &curr, const Point& other)
{
    int r = curr.getY() - other.getY();
    if (r)
    {
        return r;
    }
    else
    {
        return other.getX() - curr.getX();
    }
}

/**
 * @brief get point with minimum y-coordinate (and minimum x-coordinate if there are ties).
 * @param set the set
 * @return the point
 */
int getPointWithMinimumYCoordinate(const PointSet &set)
{
    Point *array = set.getSet();
    int minIndex = -1;
//     Check for 0 size
    if (set.size() > 0)
    {
        minIndex = 0;
    }
    for (int i = 0; i < set.size(); ++i)
    {
        if (compareToFindMinimum(array[i], array[minIndex]) < 0)
        {
            minIndex = i;
        }
    }
    return minIndex;
}

/**
 * @brief Calculate the distance between 2 points
 * @param a one point
 * @param b second point
 * @return the distance between two points
 */
int sqrDist(Point &a, Point &b)
{
    int dx = a.getX() - b.getX(), dy = a.getY() - b.getY();
    return dx * dx + dy * dy;
}

// returns -1 if a -> b -> c forms a counter-clockwise turn,
// +1 for a clockwise turn, 0 if they are collinear
/**
 * @brief returns -1 if a -> b -> c forms a counter-clockwise turn, +1 for a clockwise turn, 0
 * if they are collinear
 * @param a first point
 * @param b second point
 * @param c third point
 * @return -1 if a -> b -> c forms a counter-clockwise turn, +1 for a clockwise turn, 0
 * if they are collinear
 */
int ccw(Point &a, Point &b, Point &c)
{
    int area = (b.getX() - a.getX()) * (c.getY() - a.getY()) - (b.getY() - a.getY()) * (c.getX()
                                                                                        - a.getX());
    if (area > 0)
    {
        return -1;
    }
    else if (area < 0)
    {
        return 1;
    }
    return 0;
}

/**
 * @brief Comparation func - compare by polar angel
 * @param p1 first point
 * @param p2 second point
 * @return >0 if cuurent bigger, <0 if ither bigger, 0 if equals
 */
int compareAngelToPoint(const void* p1, const void* p2)
{
    int order = ccw(minPoint, *(Point *)p1, *(Point *)p2);
    if (order == 0)
    {
        return sqrDist(minPoint, *(Point *) p1) > sqrDist(minPoint, *(Point *) p2);
    }
    return (order == -1);
}

void printArray(Point *array, int size)
{
    std::cout << "result\n";
    for (int j = 0; j < size; ++j)
    {
        std::cout << array[j].toString() << "\n";
    }
}

/**
 * @brief (counter-clockwise) - find the lowest rightmost point, then sort
 * all the array by polar angel. Then begin at the minimal point - take the next two point in
 * the sorted array, if we turn left we don't count this point - so swap it with the next point.
 * In that way we run until the last point (and that why i increased the array by 1 -  to place
 * the minimal point again, because every time we check if we go right or left we need 3 points.
 * @param set the pointer set
 */
void grahamsAlgorithm(PointSet &set)
{
    if (set.size() == 0)
    {
        printArray(set.getSet(), set.size());
        return;
    }
    // Create pointers array
    Point **setArr = new Point*[set.size()];
    for (int j = 0; j < set.size(); ++j)
    {
        setArr[j] = &set.getSet()[j];
    }
    Point *sortedArr = new Point[set.size() + 1];
    int minIndex = getPointWithMinimumYCoordinate(set);
    minPoint = *setArr[minIndex];
//    swap
    {
        Point *temp = setArr[FIRST_CELL];
        setArr[0] = setArr[minIndex];
        setArr[minIndex] = temp;
    }
    std::sort(setArr + 1, setArr + set.size(), compareAngelToPoint);
    for (int i = 0; i < set.size(); ++i)
    {
        sortedArr[i] = *setArr[i];
    }
    delete(setArr);
    sortedArr[set.size()] = minPoint;
    Point temp;
    int m = 1;
    for (int i = 2; i < set.size() + 1; ++i)
    {
        while (ccw(sortedArr[m - 1], sortedArr[m], sortedArr[i]) >= 0)
        {
            if (m > 1)
            {
                m--;
            }
            else if (i == set.size())
            {
                break;
            }
            else
            {
                i++;
            }
        }
        m++;
        temp = sortedArr[m];
        sortedArr[m] = sortedArr[i];
        sortedArr[i] = temp;
    }
    printArray(sortedArr, m);
    delete(sortedArr);
}

/**
 * @brief Main function
 * @return result
 */
int main()
{
    int x, y;
    PointSet set;
    unsigned long pos;
    std::string input;
    while (std::getline(std::cin, input) && input != "22")
    {
        pos = input.find(",");
        if (pos != std::string::npos)
        {
            x = stoi(input.substr(0, pos));
            y = stoi(input.substr(pos + 1));
            set.add(Point(x, y));
        }
    }
    grahamsAlgorithm(set);
    set.freeSet();
    return 0;
}
