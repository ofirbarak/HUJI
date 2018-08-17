#include <iostream>
#include "Thread.h"
#include <vector>
#include <pthread.h>
#include <thread>
#include <signal.h>
#include <setjmp.h>
#include <sys/time.h>
#include <unistd.h>
#include <list>

using namespace std;

#define SUCCESS (0)
#define SECOND 1000000
#define MAX_THREAD_NUM (100)
#define FAILURE (-1)
#define MAIN_TID (0)


Thread *currentThread;
vector<Thread*> threads;
vector<Thread*> ready_threads;
vector<Thread*> blocked_threads;
sigset_t set;
int available_ids[MAX_THREAD_NUM];

int quantum;
struct itimerval timer;
int total_quantum;

void block_sig()
{
    sigemptyset(&set);
    sigaddset(&set, SIGVTALRM);
    sigprocmask(SIG_SETMASK, &set, NULL);
}

void unblock_sig()
{
    sigemptyset(&set);
    sigaddset(&set, SIGVTALRM);
    sigprocmask(SIG_UNBLOCK, &set, NULL);
}



void running_thread(int sigNum) {
    block_sig();
    total_quantum++;
    if (currentThread->get_state() == Thread::RUNNING) {
        currentThread->set_state(Thread::READY);
        Thread *t = ready_threads.front();
        ready_threads.push_back(currentThread);
        ready_threads.erase(ready_threads.begin());
        int ret = sigsetjmp(currentThread->get_env(), 1);
        if (ret == 1) {
            unblock_sig();
            return;
        }
        currentThread = t;
        currentThread->set_state(Thread::RUNNING);
        t->raise_quantums();
    }
    if (currentThread->get_state() == Thread::BLOCKED) {

        Thread *t = ready_threads.front();
        ready_threads.erase(ready_threads.begin());
        int ret = sigsetjmp(currentThread->get_env(), 1);
        if (ret == 1) {
            unblock_sig();
            return;
        }
        currentThread = t;
        currentThread->set_state(Thread::RUNNING);
        t->raise_quantums();
    }
    if (currentThread->get_state() == Thread::TERMINATED)
    {
        //Add all dependent threads to ready_threads vector
        int currentId = currentThread->get_id();
        for (auto it=threads.begin(); it != threads.end(); ++it){
            if((*it)->appear_in_sync_list(currentId)){
                ready_threads.push_back(*it);
            }
        }

        Thread *t = ready_threads.front();
        ready_threads.erase(ready_threads.begin());
        int ret = sigsetjmp(currentThread->get_env(), 1);
        if (ret == 1) {
            unblock_sig();
            return;
        }
        currentThread = t;
        currentThread->set_state(Thread::RUNNING);
        t->raise_quantums();
    }
    unblock_sig();
    siglongjmp(currentThread->get_env(), 1);
}
int clock_set()
{
    int seconds = quantum / SECOND;
    int usecs = quantum - seconds*SECOND;
    timer.it_value.tv_sec = seconds;
    timer.it_value.tv_usec = usecs;
    timer.it_interval.tv_sec = seconds;
    timer.it_interval.tv_usec = usecs;
    // Start a virtual timer. It counts down whenever this process is executing.
    if (setitimer (ITIMER_VIRTUAL, &timer, NULL)) {
        cerr << "system error: setitimer error.";
        return FAILURE;
    }
    return SUCCESS;
}

int uthread_init(int quantum_usecs)
{
    block_sig();
    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sa.sa_handler = &running_thread;
    if (sigaction(SIGVTALRM, &sa,NULL) < 0) {
        cerr << "system error: sigaction error.";
        return FAILURE;
    }
    total_quantum = 1;
    quantum = quantum_usecs;
    currentThread = new Thread(0,0);
    currentThread->set_state(Thread::RUNNING);
    threads.push_back(currentThread);
    if (quantum <= 0)
    {
        return FAILURE;
    }
    if (clock_set() == SUCCESS)
    {
        return SUCCESS;
    }
    unblock_sig();
    return FAILURE;
}



int check_for_tid()
{
    for (size_t i = 1; i < MAX_THREAD_NUM; i++)
    {
        if (available_ids[i] == 0)
        {
            available_ids[i] = 1;
            return i;
        }
    }

}

int uthread_spawn(void (*f)(void))
{
    block_sig();
    if (threads.size() + 1 == MAX_THREAD_NUM)
    {
        return FAILURE;
    }
    int tid = check_for_tid();
    Thread *t = new Thread(tid, f);
    ready_threads.push_back(t);
    threads.push_back(t);
    unblock_sig();
    return tid;
}

bool valid_tid(int tid)
{
    int length = threads.size();
    for (size_t i = 0; i < length; i++)
    {
        if (tid == threads[i]->get_id())
        {
            return true;
        }
    }
    return false;
}

void deleter(int tid)
{
    int length = threads.size();
    for (size_t i = 0; i < length ; i++)
    {
        if (threads[i]->get_id() == tid)
        {
            threads.erase(threads.begin() + i);
        }
    }
    length = ready_threads.size();
    for (size_t i = 0; i < length; i++)
    {
        if (ready_threads[i]->get_id() == tid)
        {
            ready_threads.erase(ready_threads.begin() + i);
        }
    }
}

int uthread_terminate(int tid)
{
    block_sig();
    if (tid == MAIN_TID)
    {
        exit(0);
    }
    else if (!valid_tid(tid))
    {
        cerr << "thread library error: invalid id for termination";
        return FAILURE;
    }
    if (tid == currentThread->get_id())//todo: why just the current thread
    {
        deleter(tid);
        clock_set();
        currentThread->set_state(Thread::TERMINATED);
        unblock_sig();
        running_thread(SIGVTALRM);
    }
    unblock_sig();
    return SUCCESS;
}

Thread* find_thread(int tid)
{
   int length = threads.size();
   for (size_t i = 0; i < length; i++)
   {
       if (threads[i]->get_id() == tid)
       {
           return threads[i];
       }
   }
    return nullptr;
}

/*
 * Returns thread id is waiting for current thread finish
 */
int getDependentThread(int tid){
    Thread *waitingThread = find_thread(tid);
    if (waitingThread == nullptr) {
        return -1;
    }
    for (size_t i=0; i < threads.size(); i++){
        if (waitingThread->appear_in_sync_list(currentThread->get_id())){

        }
    }
}


void ready_to_blocked(Thread* t)
{
    int length = threads.size();
    for (size_t i = 0; i < length; i++)
    {
        if (ready_threads[i]->get_id() == t->get_id())
        {
            ready_threads.erase(ready_threads.begin() + i);
        }
    }
}


int uthread_block(int tid)
{
    block_sig();
    if (tid == MAIN_TID)
    {
        cerr << "thread library error: trying to block main thread";
        return FAILURE;
    }
    if (!valid_tid(tid))
    {
        cerr << "thread library error: trying to block unreal thread";
        return FAILURE;
    }
    Thread* t = find_thread(tid);
    t->set_state(Thread::BLOCKED);
    ready_to_blocked(t);
    if (tid == currentThread->get_id()) // NEED TO RESET CLOCK FOR NEW THREAD
    {
        clock_set();
        unblock_sig();
        running_thread(SIGVTALRM);
    }
    unblock_sig();
    return SUCCESS;
}

int uthread_resume(int tid)
{
    block_sig();
    if (!valid_tid(tid))
    {
        cerr << "thread library error: trying to resume unreal thread";
        return FAILURE;
    }
    Thread* t = find_thread(tid);
    if (t->get_state() == Thread::READY || t->get_state() == Thread::RUNNING)
    {
        return SUCCESS;
    }
    t->set_state(Thread::READY);
    ready_threads.push_back(t);
    unblock_sig();
    return SUCCESS;
}


int uthread_sync(int tid)
{
    if (!valid_tid(tid))
    {
        cerr << "thread library error: trying to sync unexisting thread";
        return FAILURE;
    }
    if (tid == MAIN_TID)
    {
        cerr << "thread library error: main called sync";
        return FAILURE;
    }
//    Thread* waitFor = find_thread(tid);
    currentThread->add_to_sync(tid);
    return uthread_block(currentThread->get_id());
//    uthread_block(currentThread.get_id());
}

int uthread_get_tid()
{
    return currentThread->get_id();
}

int uthread_get_total_quantums()
{
    return total_quantum + 1;
}

int uthread_get_quantums(int tid)
{
    if (!valid_tid(tid))
    {
        cerr << "thread library error: calculating quantums for unreal thread";
        return FAILURE;
    }
    Thread *t = find_thread(tid);
    if (tid == currentThread->get_id())
    {
        return t->get_quantums() + 1;
    }
    return t->get_quantums();
}


