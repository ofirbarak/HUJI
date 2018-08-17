
#include "Node.h"

Node::Node(Point p) : _point(p), _next(nullptr)
{
}

Node::~Node()
{
}

std::string Node::toString()
{
    return _point.toString();
}