/**
 * Simple test for the PointSet implementation
 */
#include <iostream>
#include <string>
#include "PointSet.h"
#include "Point.h"

#define NUM_ARRAYS 3
#define EQ_RETURN_VAL 0

int main()
{
	PointSet listsArr[NUM_ARRAYS];
	int res;
	res = listsArr[0].add(Point(6, 5));
	res+=listsArr[0].add(Point(7, 6));
	res+=listsArr[1].add(Point(7, 6));
	res+=listsArr[1].add(Point(6, 5));
	res+=listsArr[1].add(Point(8, 2));
	res+=listsArr[2].add(Point(9, -2));
	res+=listsArr[2].add(Point(10, -2));
	
	if (res != 7)
	{
		std::cout << "ERROR: Fail test add" << std::endl;
		return 1;
	}
	
	if (listsArr[0] == listsArr[1])
	{
		std::cout << "ERROR: Fail test comparing " << std::endl;
		return 1;
	}
	
	PointSet min = listsArr[0] - listsArr[1];
	if (min.size() != 0)
	{
		std::cout << "ERROR: Fail test Minus" << std::endl;
		std::cout <<	listsArr[0].toString();
		std::cout << "-" << std::endl;		
		std::cout << 	listsArr[1].toString();
		std::cout << "=" << std::endl;		
		std::cout << min.toString();
		std::cout << "-" << std::endl;		
		return 1;
	}
	
	PointSet intersect = listsArr[0] & listsArr[2];
	if (intersect.size() != 0)
	{
		
		std::cout << "ERROR: Fail test Intersection" << std::endl;
		std::cout << listsArr[0].toString();
		std::cout << "&" << std::endl;		
		std::cout << listsArr[2].toString();
		std::cout << "=" << std::endl;		
		std::cout << intersect.toString();
		std::cout << "&" << std::endl;		
		return 1;
	}

	std::cout << "Pass basic binary tests." << std::endl;
	return 0;
}
