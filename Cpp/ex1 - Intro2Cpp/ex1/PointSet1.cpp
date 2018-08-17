
#include "PointSet1.h"

PointSet::PointSet() : _head(nullptr)
{
}

PointSet::~PointSet()
{
}

bool PointSet::add(Point &p)
{
    if (find(p))
    {
        return false;
    }
    if(_head == nullptr)
    {
        _head = new Node(p);
        return true;
    }
    Node* n = _head;
    while (n->getNext() != nullptr)
    {
        n = n->getNext();
    }
    n->setNext(new Node(p));
    return true;
}

/**
 * @brief Check if point already exists in set
 * @param p point
 * @return true if yes, false otherwise
 */
bool PointSet::find(Point &p)
{
    Node* n = _head;
    if (n != nullptr)
    {
        while (n->getNext() != nullptr)
        {
            if (n->getPoint() == p)
            {
                return true;
            }
            n = n->getNext();
        }
    }
    return false;
}

bool PointSet::remove(Point &p)
{
    if(_head == nullptr)
    {
        return false;
    }
    Node* n = _head;
    while (n->getNext() != nullptr)
    {
        if(n->getPoint() == p)
        {
            n->setNext(n->getNext()->getNext());
            n->getNext()->destroy();
            delete(n->getNext());
            return true;
        }
        n = n->getNext();
    }
    return false;
}

std::string PointSet::toString()
{
    std::string out = "";
    Node* n = _head;
    if (n != nullptr)
    {
        while (n->getNext() != nullptr)
        {
            out += n->toString() + "\n";
            n = n->getNext();
        }
    }
    return out;
}

int PointSet::size()
{
    int size = 0;
    Node* n = _head;
    if (n != nullptr)
    {
        while (n->getNext() != nullptr)
        {
            n = n->getNext();
        }
    }
    return size;
}

