#include <iostream>
using namespace std;
    static int x;
class A
{
public:
    // This declares it.
    static int getX(){return x;}
};

// Now you need an create the object so
// This must be done in once source file (at file scope level)
//int A::x = 100;


int main()
{
    A::getX();
    // Note no int here. You can modify it

    cout<<A::getX(); // Should work
    return 0;
}
