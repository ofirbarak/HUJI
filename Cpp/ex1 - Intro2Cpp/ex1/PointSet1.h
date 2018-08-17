
#ifndef EX1_POINTSET_H
#define EX1_POINTSET_H


#include <string>
#include "Node.h"
#include "Point.h"

class PointSet
{
private:
    Node* _head;
    bool find(Point &p);
public:
    PointSet();
    ~PointSet();
    std::string toString();
    bool add(Point &p);
    bool remove(Point &p);
    int size();
};


#endif //EX1_POINTSET_H
