// PointSetBinaryOperations.cpp
#include <iostream>
#include "PointSet.h"

using namespace std;

/**
 * @brief Main function that does simple operations
 * @return result
 */
int main()
{
    PointSet *ps1 = new PointSet();
    PointSet *ps2 = new PointSet();
    Point p1(0, 0);
    Point p2(1, 0);
    Point p3(0, 1);
    Point p4(1, 1);
    Point p5(-1, -1);

    ps1->add(p1);
    ps2->add(p1);
    ps1->add(p2);
    ps2->add(p2);
    cout << "Check for equal\n" ;
    cout << "Set1: \n" << ps1->toString();
    cout << "Set2: \n" << ps2->toString();
    cout << "(result should be not 0):" << (*ps1 == *ps2) << "\n\n";

    ps1->add(p3);
    cout << "Check for not equal\n" ;
    cout << "Set1: \n" << ps1->toString();
    cout << "Set2: \n" << ps2->toString();
    cout << "(result should be not 0) " << (*ps1 != *ps2) << "\n\n";

    // Subtraction
    cout << "Check for subtraction:\n";
    cout << "Set1: \n" << ps1->toString();
    cout << "Set2: \n" << ps2->toString();
    PointSet subSet = (*ps1 - *ps2);
    cout << "After operation: \n" << subSet.toString() << "\n";
    delete(subSet.getSet());

    ps1->add(p4);
    // Intersection
    cout << "Check for Intersection:\n";
    cout << "Set1: \n" << ps1->toString();
    cout << "Set2: \n" << ps2->toString();
    PointSet interSet = (*ps1 & *ps2);
    cout << "After operation: \n" << interSet.toString() << "\n";
    delete(interSet.getSet());

    ps2->add(p5);
    // Assignment
    cout << "Check for assignment (set1 = set2):\n";
    cout << "Set1: \n" << ps1->toString();
    cout << "Set2: \n" << ps2->toString();
    *ps1 = *ps2;
    cout << "After operation:\n" << ps1->toString() << "\n";

    delete(ps1->getSet());
    delete(ps2->getSet());
    delete(ps1);
    delete(ps2);
    return 0;
}
