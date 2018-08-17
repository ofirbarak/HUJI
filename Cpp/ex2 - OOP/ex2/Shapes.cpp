
#include <iostream>
#include <fstream>
#include <iomanip>
#include "Triangle.h"
#include "PrintOuts.h"
#include "Trapezoid.h"

#define ERROR_OPEN_READ_FILE "Error while opening the file to read from\n"
#define ERROR_OPEN_WRITE_FILE "Error while opening the writing file\n"
#define ERROR_IN_USAGE "Usage: Shapes <input_file_name> [<output_file_name>]\n"
#define INPUT_FILE_PLACE 1
#define OUTPUT_FILE_PLACE 2
#define PRECISION 2
#define ERROR_TRIANGLE "ERROR: Illegal Trig - represent a plain line.\n"
#define ERROR_TRAPEZOID "ERROR: Illegal Trapezoid."



using namespace std;

static bool validateTriangle(Point p1, Point p2, Point p3)
{
    return Shape::calcDeterminant(p1, Line(p2, p3)) != 0;
}


static bool validateTrapezoid(Point p1, Point p2, Point p3, Point p4)
{
    if (p1.getY() == p2.getY() && p3.getY() == p4.getY() && p1.getY() != p3.getY())
    {
        // Check for hourglass
        if (Shape::calcDeterminant(p1, Line(p2, p3)) *
            Shape::calcDeterminant(p4, Line(p2, p3)) >= 0)
        {
            return true;
        }
    }
    return false;
}

static int tryOpenReadFileAndRedirectionStd(string inFileName, ifstream &fileToRead)
{
    fileToRead.open(inFileName);
    if (fileToRead.fail())
    {
        return -1;
    }
    std::cin.rdbuf(fileToRead.rdbuf());
    return 0;
}

static int tryOpenWriteFileAndRedirectionStd(string outFileName, ofstream &fileToWrite)
{
    fileToWrite.open(outFileName);
    if (!fileToWrite.is_open())
    {
        return -1;
    }
    std::cout.rdbuf(fileToWrite.rdbuf());
    return 0;
}

static inline void endMain(vector<Shape *> shapes, ifstream &fileToRead, ofstream &fileToWrite,
                           streambuf *cinbuf, streambuf *coutbuf)
{
    for (vector<Shape *>::iterator it = shapes.begin(); it != shapes.end(); it++)
    {
        delete(*it);
    }
    fileToRead.close();
    fileToWrite.close();
    //Restore back.
    std::cin.rdbuf(cinbuf);
    std::cout.rdbuf(coutbuf);
}


static CordType checkForIntersectionAndSumAreas(vector<Shape *>shapes)
{
    CordType areaSum = 0;
    for (vector<Shape *>::iterator it1 = shapes.begin(); it1 != shapes.end(); ++it1)
    {
        areaSum += (**it1).area();
        for (vector<Shape *>::iterator it2 = it1 + 1; it2 != shapes.end(); ++it2)
        {
            if (Shape::hasIntersection(**it1, **it2))
            {
                (*it1)->printShape();
                (*it2)->printShape();
                reportDrawIntersect();
                return -1;
            }
        }
    }
    return areaSum;
}

/**
 * Main function
 */
int main(int argc, char *argv[])
{
    // Save original std::cin, std::cout
    streambuf *coutbuf = cout.rdbuf();
    streambuf *cinbuf = cin.rdbuf();
    if (argc != 2 && argc != 3)
    {
        cerr << ERROR_IN_USAGE << endl;
        return -1;
    }
    ifstream fileToRead;
    ofstream fileToWrite;
    if (tryOpenReadFileAndRedirectionStd(argv[INPUT_FILE_PLACE], fileToRead) != 0)
    {
        cerr << ERROR_OPEN_READ_FILE;
        return -1;
    }
    if (argc == 3 && tryOpenWriteFileAndRedirectionStd(argv[OUTPUT_FILE_PLACE], fileToWrite) != 0)
    {
        cerr << ERROR_OPEN_WRITE_FILE;
        fileToRead.close();
        return -1;
    }
    cout << fixed;
    cout << setprecision(PRECISION);
    char type;
    vector<Shape *> shapes;
    CordType x1, y1, x2, y2, x3, y3, x4, y4;
    while(cin >> type)
    {
        switch (type)
        {
            case 'T':
                cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3;
                if (!validateTriangle(Point(x1, y1), Point(x2, y2), Point(x3, y3)))
                {
                    cerr << ERROR_TRIANGLE << endl;
                    endMain(shapes, fileToRead, fileToWrite, cinbuf, coutbuf);
                    return -1;
                }
                shapes.push_back(new Triangle(Point(x1, y1), Point(x2, y2), Point(x3, y3)));
                break;
            case 't':
                cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3 >> x4 >> y4;
                if (!validateTrapezoid(Point(x1, y1), Point(x2, y2), Point(x3, y3),
                    Point(x4, y4)))
                {
                    cerr << ERROR_TRAPEZOID << endl;
                    endMain(shapes, fileToRead, fileToWrite, cinbuf, coutbuf);
                    return -1;
                }
                shapes.push_back(new Trapezoid(Point(x1, y1), Point(x2, y2), Point(x3, y3),
                    Point(x4, y4)));
                break;
            default:
                break;
        }
    }
    CordType areaSum;
    if ((areaSum = checkForIntersectionAndSumAreas(shapes)) != -1)
    {
        printArea(areaSum);
    }
    endMain(shapes, fileToRead, fileToWrite, cinbuf, coutbuf);
    return 0;
}
