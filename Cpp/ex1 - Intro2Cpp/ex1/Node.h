

#ifndef EX1_NODE_H
#define EX1_NODE_H


#include <string>
#include "Point.h"

class Node
{
private:
    Point& _point ;
    Node* _next;
public:
    Node(Point d);
    ~Node();
    Node* getNext()
    {
        return _next;
    }

    Point getPoint()
    {
        return _point;
    }

    void setNext(Node* const newPoint)
    {
        _next = newPoint;
    }

    void destroy()
    {
        delete(_point);
    }
    std::string toString();
};


#endif //EX1_NODE_H
