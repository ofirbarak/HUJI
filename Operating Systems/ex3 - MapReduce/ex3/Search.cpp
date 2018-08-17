#include <iostream>
#include <dirent.h>
#include <algorithm>
#include "MapReduceClient.h"
#include "MapReduceFramework.h"

using namespace std;

// First we are pass all over the given directories and map each file in these
// directories to <FileName, substring_to_search>.
// Then, shuffle part - check if the string actually is substring of FileName
// Third, create a list and add all elements are true, sort them.
class PathName : public k1Base{
    const string _path;
public:
    PathName(const string path):_path(path){}
    ~PathName(){}
    string getPathName() const { return _path;}
    bool operator<(const k1Base &other) const {
        return _path < (static_cast<const PathName&>(other)).getPathName();
    }
};


class FileNameKey : public k2Base, public k3Base {
    const string _file;
public:
    FileNameKey(const string fileName) : _file(fileName) {}
    ~FileNameKey() {}
    bool isSubString(string s) const {
        return _file.find(s) != std::string::npos;
    }

    string getFileName() const { return _file; }

    bool operator<(const k2Base &other) const {
        bool a = _file < (static_cast<const FileNameKey&>(other))._file;
        return a;
    }

    bool operator<(const k3Base &other) const {
        return _file < (static_cast<const FileNameKey&>(other))._file;
    }
};

class Substring : public v1Base, public v2Base {
    string _substring;
public:
    Substring(const string substring) : _substring(substring) {}

    string getString() const {
        return _substring;
    };
};


class NumOfAppearances : public v3Base {
    int _num;
public:
    NumOfAppearances() : _num(0) {}
    NumOfAppearances(int n) : _num(n) {}
    ~NumOfAppearances() {}
    int getNum() const { return _num; }
};


class SearchMapReduceBase : public MapReduceBase {
public:
    SearchMapReduceBase() {}
    ~SearchMapReduceBase() {}

    void Map(const k1Base *const key, const v1Base *const val) const {
        try {
            const string path =
                    dynamic_cast<const PathName*const>(key)->getPathName();
            const string substring =
                    dynamic_cast<const Substring*const>(val)->getString();
            DIR *dp;
            struct dirent *dirp;
            if ((dp = opendir(string(path).c_str())) != NULL) {
                while ((dirp = readdir(dp)) != NULL) {
                    FileNameKey *f = new FileNameKey(string(dirp->d_name));
                    Substring *s = new Substring(substring);
                    Emit2(f, s);
                }
                closedir(dp);
            }
        }
        catch (exception & e){
            cout << "Exception " << e.what() << endl;
        }

    }

    void Reduce(const k2Base *const key, const V2_VEC &vals) const {
        int sum = 0;
        auto file = dynamic_cast<const FileNameKey*const>(key);
        for (auto iterator = vals.begin(); iterator != vals.end(); ++iterator) {
            if(file->isSubString(((Substring*)(*iterator))->getString()))
                sum++;
        }
        if (sum > 0)
            Emit3(new FileNameKey(file->getFileName()),
                  new NumOfAppearances(sum));
    }
};



void releaseResources(IN_ITEMS_VEC pairs, OUT_ITEMS_VEC outs){
    for (auto &pair:pairs){
        delete pair.first;
        delete pair.second;
    }
    for (auto &pair:outs){
        delete pair.first;
        delete pair.second;
    }
}

IN_ITEMS_VEC addPaths(char *paths[], int num, char* substr){
    IN_ITEMS_VEC in = IN_ITEMS_VEC();
    for (int i=0; i < num; i++){
        in.push_back(make_pair(new PathName(paths[i]), new Substring(substr)));
    }
    return in;
}

int main(int argc, char *argv[]) {
    if (argc == 1) {
        cerr << "Usage: <substring to search> <folders, separated by space>"
             << endl;
        exit(1);
    }
    if (argc == 2) {
        return 0;
    }
    IN_ITEMS_VEC pairs = addPaths(&argv[2], argc-2, argv[1]);
    SearchMapReduceBase s = SearchMapReduceBase();
    OUT_ITEMS_VEC res = (OUT_ITEMS_VEC) RunMapReduceFramework(s,
                                                              pairs, 5,
                                                              true);
    for (auto it = res.begin(); it != res.end(); ++it) {
        for (int i = 0;
             i < (*((NumOfAppearances *) ((*it).second))).getNum(); ++i) {
            if(it!=res.begin()) cout << " ";
            cout << (*((FileNameKey *) ((*it).first))).getFileName();
        }
    }
    releaseResources(pairs, res);
    return 0;
}