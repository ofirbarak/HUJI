
#include <sys/types.h>
#include <pthread.h>
#include <iostream>
#include <map>
#include <semaphore.h>
#include <algorithm>
#include <fstream>
#include <sys/time.h>
#include "MapReduceFramework.h"
#include <math.h>
#define CHUNK_SIZE 10


using namespace std;

typedef std::pair<k2Base*, v2Base*> mid_pair;
typedef std::pair<k2Base*, vector<v2Base*>> mid_pair_with_vector;
typedef std::pair<k3Base*, v3Base*> final_pair;

timeval timer;
double startTime;
pthread_mutex_t locationMutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t pthreadToContainer_mutex = PTHREAD_MUTEX_INITIALIZER;;
pthread_mutex_t shuffleMap_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t logFile_mutex = PTHREAD_MUTEX_INITIALIZER;
int currentLocation = 0;

struct mid_data{
    vector<mid_pair> _pairsVector;
    pthread_mutex_t _mutex;
};

struct final_data{
    vector<final_pair> _pairsVector;
    pthread_mutex_t _mutex;
};

struct compareMapElement{
    inline bool operator()(k2Base* const & lhs,
                           k2Base* const & rhs) const {
        return (*lhs < *rhs);
    }
};

map<pthread_t,mid_data> pthreadToContainer;
sem_t items_semaphore;
map<k2Base*,vector<v2Base*>,compareMapElement> shuffleMap;
vector<pair<k2Base*,vector<v2Base*>>> shuffleVector;

map<pthread_t,final_data> reduceContainers;

struct mapArgumentStruct{
    IN_ITEMS_VEC arg1;
    MapReduceBase *arg2;
};

struct reduceArgumentStruct{
    vector<pair<k2Base*,vector<v2Base*>>> arg1;
    MapReduceBase *arg2;
};

void checkError(int result, string func_err){
    if (result < 0){
        cerr << "MapReduceFramework Failure: "<< func_err << "failed.";
        exit(1);
    }
}

void *ExecMap(void* arguments){
    checkError(pthread_mutex_lock(&pthreadToContainer_mutex), "ExecMap");
    checkError(pthread_mutex_unlock(&pthreadToContainer_mutex), "ExecMap");
    struct mapArgumentStruct *args = (mapArgumentStruct *) arguments;
    auto itemsVec = (IN_ITEMS_VEC&)args->arg1;
    int inc;
    while (itemsVec.size() > (unsigned int)currentLocation) {
        checkError(pthread_mutex_lock(&locationMutex), "ExecMap");
        inc = min(CHUNK_SIZE, (const int &)itemsVec.size()-currentLocation);
        auto in = itemsVec.begin() + currentLocation;
        currentLocation += inc;
        checkError(pthread_mutex_unlock(&locationMutex), "ExecMap");
        for (int i = 0; i < inc; i++) {
            (args->arg2)->Map(in[i].first, in[i].second);
        }
    }
    return nullptr;
}


void Emit2 (k2Base* k, v2Base* v){
    checkError(pthread_mutex_lock(&pthreadToContainer[pthread_self()]._mutex),
               "Emit2");
    pthreadToContainer[pthread_self()]._pairsVector.push_back(mid_pair(k, v));
    checkError(pthread_mutex_unlock(&pthreadToContainer[pthread_self()]._mutex),
               "Emit2");
    checkError(sem_post(&items_semaphore), "Emit2");

}

bool EmptyPthreadContainers (void){
    bool is_all_empty = true;
    for (auto &thread_it : pthreadToContainer) {
        if (thread_it.second._pairsVector.size() > 0){
            is_all_empty = false;
            checkError(pthread_mutex_lock(&thread_it.second._mutex), "Shuffle");
            vector<mid_pair> cp(thread_it.second._pairsVector.size());
            copy(thread_it.second._pairsVector.begin(),
                 thread_it.second._pairsVector.end(), cp.begin());
            for (auto &pair : cp){
                shuffleMap[pair.first].push_back(pair.second);
            }
            thread_it.second._pairsVector.clear();
            checkError(pthread_mutex_unlock(&thread_it.second._mutex),
                       "Shuffle");
        }
    }
    return is_all_empty;
}

void *Shuffle(void *){
    while (true) {
        bool is_all_empty = true;
        checkError(sem_wait(&items_semaphore), "Shuffle");
        is_all_empty = EmptyPthreadContainers();
        if (is_all_empty){
            return nullptr;
        }
    }
}


void *ExecReduce(void *arguments){
    checkError(pthread_mutex_lock(&shuffleMap_mutex), "ExecReduce");
    checkError(pthread_mutex_unlock(&shuffleMap_mutex), "ExecReduce");
    struct reduceArgumentStruct *args = (reduceArgumentStruct *) arguments;
    auto shuffleItems = (vector<pair<k2Base*,vector<v2Base*>>>&)args->arg1;
    while (shuffleItems.size() > (unsigned int)currentLocation)
    {
        checkError(pthread_mutex_lock(&locationMutex), "ExecReduce");
        int inc = min(CHUNK_SIZE,
                      (const int &) shuffleItems.size() - currentLocation);
        auto in = shuffleItems.begin() + currentLocation;
        currentLocation += inc;
        checkError(pthread_mutex_unlock(&locationMutex), "ExecReduce");
        for (int i = 0; i < inc; i++) {
            (args->arg2)->Reduce(in[i].first, in[i].second);
        }
    }
    return nullptr;
}


void Emit3 (k3Base* k, v3Base* v){
    checkError(pthread_mutex_lock(&reduceContainers[pthread_self()]._mutex),
               "Emit3");
    reduceContainers[pthread_self()]._pairsVector.
            push_back(pair<k3Base*,v3Base*>(k,v));
    checkError(pthread_mutex_unlock(&reduceContainers[pthread_self()]._mutex),
               "Emit3");
}


void DeleteDataPairs(bool autoDelete) {
    if (autoDelete) {
        for (auto &t_v:shuffleVector) {
            for (auto &pair:t_v.second){
                delete pair;
            }
            delete t_v.first;
        }
        for (auto tid=*reduceContainers.begin(); false;) {
            for (auto &pair:tid.second._pairsVector){
                delete pair.second;
                delete pair.first;
            }
        }
    }
}


void MutexDeleter(){
    checkError(pthread_mutex_destroy(&locationMutex), "MutexDeleter");
    checkError(pthread_mutex_destroy(&pthreadToContainer_mutex), "MutexDeleter");
    checkError(pthread_mutex_destroy(&shuffleMap_mutex), "MutexDeleter");
    for(auto &pid:pthreadToContainer){
        checkError(pthread_mutex_destroy(&pid.second._mutex), "MutexDeleter");
    }
    for(auto &f:reduceContainers){
        checkError(pthread_mutex_destroy(&f.second._mutex), "MutexDeleter");
    }
    checkError(pthread_mutex_destroy(&logFile_mutex), "MutexDeleter");
}

string getTime(){
    time_t timeNow;
    struct tm *info;
    char buffer[80];
    time(&timeNow);
    info = localtime(&timeNow);
    strftime(buffer, 80, "[%d.%m.%Y %X]", info);
    return buffer;
}

void ExecLogger(ofstream &logFile, string func_name){
    checkError(pthread_mutex_lock(&logFile_mutex), "ExecLogger");
    logFile << "Thread " << func_name << " created " << getTime() << "\n";
    checkError(pthread_mutex_unlock(&logFile_mutex), "ExecLogger");
}

void ExecTerminator(ofstream &logFile, string func_name){
    checkError(pthread_mutex_lock(&logFile_mutex), "ExecLogger");
    logFile << "Thread " << func_name << " terminated " << getTime() << "\n";
    checkError(pthread_mutex_unlock(&logFile_mutex), "ExecLogger");
}

void Took(ofstream &logFile, string func_name, double time){
    checkError(pthread_mutex_lock(&logFile_mutex), "ExecLogger");
    logFile << func_name << " took " << time << "ns\n";
    checkError(pthread_mutex_unlock(&logFile_mutex), "ExecLogger");
}


void untilShuffleStage(ofstream &logFile, MapReduceBase &mapReduce,
                       IN_ITEMS_VEC& itemsVec, int multiThreadLevel){
    struct timespec time;
    clock_gettime(CLOCK_REALTIME, &time);
    pthread_t threads[multiThreadLevel];
    pthread_t shuffleThread;
    // set a thread and a semaphore for shuffle part
    checkError(sem_init(&items_semaphore, 0, 0), "RunMapReduceFramework");
    checkError(pthread_create(&shuffleThread, NULL, Shuffle, (void *) NULL),
               "RunMapReduceFramework");
    ExecLogger(logFile, "Shuffle");
    struct mapArgumentStruct arguments;
    arguments.arg1 = itemsVec;
    arguments.arg2 = &mapReduce;
    mid_data t;
    // Create threads for map multithreading
    checkError(pthread_mutex_lock(&pthreadToContainer_mutex),
               "RunMapReduceFramework");
    for (int i = 0; i < multiThreadLevel; i++) {
        checkError(pthread_create(&threads[i], NULL, ExecMap, &arguments),
                   "RunMapReduceFramework");
        ExecLogger(logFile, "ExecMap");
        t = mid_data();
        t._mutex = PTHREAD_MUTEX_INITIALIZER;
        t._pairsVector = vector<mid_pair>();
        pthreadToContainer[threads[i]] = t;
    }
    // set time for log file
    gettimeofday(&timer, nullptr);
    double startTime = (timer.tv_sec*pow(10,9))+timer.tv_usec*pow(10,3);
    checkError(pthread_mutex_unlock(&pthreadToContainer_mutex),
               "RunMapReduceFramework");

    // join all threads
    void *retVal;
    for (int i = 0; i < multiThreadLevel; i++) {
        pthread_join(threads[i], &retVal);
        ExecTerminator(logFile, "ExecMap");
        if (retVal != 0) {
            cerr << "MapReduceFramework Failure: RunMapReduceFramework failed."
                 << endl;
            exit(1);
        }
    }

    checkError(sem_post(&items_semaphore), "Main2"); // last call to shuffle
    pthread_join(shuffleThread, &retVal); // join the shuffle thread
    ExecTerminator(logFile, "Shuffle");
    if (retVal != 0) {
        cerr << "MapReduceFramework Failure: RunMapReduceFramework failed."
             << endl;
        exit(1);
    }
    EmptyPthreadContainers();
    gettimeofday(&timer, nullptr);
    double nTime = (timer.tv_sec*pow(10,9))+timer.tv_usec*pow(10,3);
    Took(logFile, "Map and Shuffle", nTime - startTime);
    // destroy the semaphore
    sem_destroy(&items_semaphore);
}

void finish(ofstream &logFile, MapReduceBase &mapReduce, int multiThreadLevel){
    void* retVal;
    pthread_t threads[multiThreadLevel];
    currentLocation = 0;
    for (auto i = shuffleMap.begin(); i != shuffleMap.end(); i++) {
        shuffleVector.push_back((*i));
    }
    checkError(sem_init(&items_semaphore, 0, 0), "RunMapReduceFramework");

    struct reduceArgumentStruct reduceArgs;
    reduceArgs.arg1 = shuffleVector;
    reduceArgs.arg2 = &mapReduce;
    // Create threads for reduce multithreading
    checkError(pthread_mutex_lock(&shuffleMap_mutex),
               "RunMapReduceFramework");
    for (int i = 0; i < multiThreadLevel; i++) {
        reduceContainers[pthread_self()]._pairsVector = OUT_ITEMS_VEC();
        checkError(pthread_create(&threads[i], NULL, ExecReduce, &reduceArgs),
                "RunMapReduceFramework");
        ExecLogger(logFile, "ExecReduce");
    }
    // set time for log file
    gettimeofday(&timer, nullptr);
    startTime = (timer.tv_sec*pow(10,9))+timer.tv_usec*pow(10,3);
    checkError(pthread_mutex_unlock(&shuffleMap_mutex),
               "RunMapReduceFramework");

    // join all threads
    for (int i = 0; i < multiThreadLevel; i++) {
        pthread_join(threads[i], &retVal);
        ExecTerminator(logFile, "ExecReduce");
        if (retVal != 0) {
            cerr << "MapReduceFramework Failure: RunMapReduceFramework"
                    " failed." << endl;
            exit(1);
        }
    }
}


ofstream& CreateLogFile(ofstream &logFile, int multiThreadLevel){
    logFile << "RunMapReduceFramework started with " << multiThreadLevel
            << " threads\n";
    return logFile;
}


OUT_ITEMS_VEC RunMapReduceFramework(MapReduceBase& mapReduce,
                                    IN_ITEMS_VEC& itemsVec,
                                    int multiThreadLevel, bool autoDeleteV2K2) {
    ofstream logFile(".MapReduceFramework.log", fstream::out | fstream::app);
    CreateLogFile(logFile, multiThreadLevel);
    untilShuffleStage(logFile, mapReduce, itemsVec, multiThreadLevel);
    finish(logFile, mapReduce, multiThreadLevel);
    MutexDeleter();
    OUT_ITEMS_VEC out;

    for (auto it = reduceContainers.begin();
         it != reduceContainers.end(); ++it) {
        for (auto it2 = (*it).second._pairsVector.begin();
             it2 != (*it).second._pairsVector.end(); ++it2) {
            out.push_back(*it2);
        }
    }
    DeleteDataPairs(autoDeleteV2K2);
    struct OutComparator{
        bool operator()(const OUT_ITEM &o1, const OUT_ITEM &o2){
            return *(o1.first) < *(o2.first);
        }
    };
    sort(out.begin(), out.end(), OutComparator());
    gettimeofday(&timer, nullptr);
    double nTime = (timer.tv_sec*pow(10,9))+timer.tv_usec*pow(10,3);
    Took(logFile, "Reduce", nTime - startTime);
    logFile << "RunMapReduceFramework finished\n";
    logFile.close();
    return out;
}


