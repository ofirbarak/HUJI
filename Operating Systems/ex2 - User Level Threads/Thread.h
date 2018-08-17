#ifndef _THREAD_H_
#define _THREAD_H_

#include <algorithm>
#include <pthread.h>
#include <cstdlib>
#include <bits/sigthread.h>
#include <setjmp.h>
#include <signal.h>
#include <vector>
#include <list>


typedef unsigned long address_t;
#define JB_SP 6
#define JB_PC 7
#define STACK_SIZE (4096)

using namespace std;

class Thread{
public:
    enum State{
        BLOCKED,
        READY,
        RUNNING,
        TERMINATED
    };
    Thread(int tid, void(*f)(void)) :
            tid(tid), stack_size(STACK_SIZE){
        address_t sp, pc;
        sp = (address_t)stack + STACK_SIZE - sizeof(address_t);
        pc = (address_t)f;
        sigsetjmp(env, 1);
        (env->__jmpbuf)[JB_SP] = translate_address(sp);
        (env->__jmpbuf)[JB_PC] = translate_address(pc);
        sigemptyset(&env->__saved_mask);
        state = READY;
        quantums = 0;
    }
    ~Thread (){}

    address_t translate_address(address_t addr)
    {
        address_t ret;
        asm volatile("xor    %%fs:0x30,%0\n"
                "rol    $0x11,%0\n"
        : "=g" (ret)
        : "0" (addr));
        return ret;
    }
    State get_state() const
    {
        return state;
    }
    void set_state(State state1)
    {
        state = state1;
    }
    int get_id() const
    {
        return tid;
    }
    pthread_t& get_thread()
    {
        return thread;
    }
    /*void terminating()
    {
        pthread_cancel(thread);
    }
*/
    sigjmp_buf& get_env()
    {
        return env;
    }

    void raise_quantums()
    {
        quantums ++;
    }

    int get_quantums()
    {
        return quantums;
    }
    int add_to_sync(int tid)
    {
        sync.push_back(tid);
    }
//    void remove_from_sync(int tid){
//        if(appear_in_sync_list(tid)){
//            sync.erase(tid);
//        }
//    }
    bool appear_in_sync_list(int tid)
    {
        return (find(sync.begin(), sync.end(), tid) != sync.end());
    }
private:
    vector<int> sync;
    int quantums;
    State state;
    char stack[STACK_SIZE];
    sigjmp_buf env;
    pthread_t thread;
    int tid;
    int stack_size;


};

#endif

