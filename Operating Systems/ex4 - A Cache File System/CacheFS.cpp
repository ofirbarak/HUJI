#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cstring>
#include <vector>
#include <cmath>
#include <map>
#include "CacheFS.h"
#include <algorithm>

#define SUCCESS 0
#define FAILURE -1

using namespace std;

int blksize;
int cache_hits = 0;
int cache_missed = 0;
typedef struct block
{
    block(int file_id, size_t size, char *buf, off_t offset,
          const char* pathname)
    {
        id = (int) (offset / blksize);
        data = (char*)malloc(strlen(buf) + 1);
        strcpy(data, buf);
        times_used = 0;
        block_path = (char*)malloc(strlen(pathname) + 1);
        strcpy(block_path, pathname);
    }
    ~block(){}
    char *data;
    char* block_path;
    int id;
    int times_used; // How many the file was used
}block;




class CacheFS
{
private:
    vector<block*> fbr_blocks;
    int newPartStart, oldPartEnd;
    vector<block*> blocks;
    int blocks_num;
    double f_old;
    double f_new;
    cache_algo_t cache_algo;
    int block_size;
    void add_block_to_partitions(block* block1){
        // add block to new partition
        fbr_blocks.push_back(block1);
        updateIndices();
    }
    void updateIndices(){
        newPartStart = floor(((double)fbr_blocks.size() -
                f_new*fbr_blocks.size())*fbr_blocks.size());
        oldPartEnd = (int)floor(f_old*fbr_blocks.size());
    }
    void remove_block_from_old(){
        block* to_del = *fbr_blocks.begin();
        auto it = fbr_blocks.begin();
        for (; *it != fbr_blocks[oldPartEnd]; ++it){
            if(to_del->times_used > (*it)->times_used){
                to_del = *it;
            }
        }
        delete_fbr_block(to_del);
        updateIndices();
    }
    void delete_fbr_block(block* b){
        for(size_t i=0; i < fbr_blocks.size(); i++){
            if(fbr_blocks[i] == b){
                fbr_blocks.erase(fbr_blocks.begin()+i);
                return;
            }
        }
        updateIndices();
    }
    bool isBlockInNewPart(block* b){
        for (size_t i=newPartStart; i < fbr_blocks.size(); i++){
            if(fbr_blocks[i] == b)
                return true;
        }
        return false;
    }
public:
    CacheFS(int num_blocks, cache_algo_t algo, double fold, double fnew,
    int blksize) :
            fbr_blocks(), newPartStart(0), oldPartEnd(0), blocks(),
            blocks_num(num_blocks), f_old(fold), f_new(fnew),
            cache_algo(algo), block_size(blksize)
    {}
    ~CacheFS(){}
    int get_size()
    {
        return block_size;
    }

    int search_block(int file_id, const char* path_name, size_t count,
                     int id, off_t offset, char* cache_buffer)
    {
        off_t new_offset = offset / blksize * blksize;
        int number_of_bytes_read = 0;
        struct stat st;
        fstat(file_id, &st);
        int size = (int) st.st_size;
        if ((int)count > size)
        {
            count = (size_t) size;
        }
        int currentLocation = 0;
        int counter = 0;
        for (auto temp : blocks)
        {
            if ((strcmp(temp->block_path, path_name) ==0) & (id == temp->id)) {
                counter++;
                cache_buffer += number_of_bytes_read;
                number_of_bytes_read = min((int)count, blksize);
                memcpy(cache_buffer, temp->data + offset - new_offset ,
                       number_of_bytes_read);
                currentLocation += number_of_bytes_read;
                if (cache_algo == FBR and !isBlockInNewPart(temp)) {
                    temp->times_used++;
                }
                if (cache_algo == LFU)
                {
                    temp->times_used ++;
                }
                remove_block(temp, true);
                add_block(temp);
                break;
            }
        }
        if (counter >= 1)
        {
            return currentLocation;
        }
        return FAILURE;
    }

    void add_block(block *block1)
    {
        if ((int)blocks.size() >= blocks_num)
        {
            call_cache_deleter_algorithm();
        }
        blocks.push_back(block1);
        if(cache_algo == FBR) {
            add_block_to_partitions(block1);
        }
    }

    void call_cache_deleter_algorithm()
    {
        switch(cache_algo) {
            case LRU:
                LRU_deleter();
                break;
            case LFU:
                LFU_deleter();
                break;
            case FBR:
                FBR_deleter();
                break;
        }
    }

    void remove_block(block* block1, bool flag)
    {
        for (size_t i=0; i < blocks.size(); i++){
            if (blocks[i] == block1){
                blocks.erase(blocks.begin()+i);
                if (!flag) {
                    free(block1->block_path);
                    free(block1->data);
                    delete block1;
                }
            }
        }
        if (cache_algo == FBR)
        {
            delete_fbr_block(block1);
        }
    }

    void LRU_deleter()
    {
        remove_block(*blocks.begin(), false);
    }
    void LFU_deleter() {
        block* to_del = *blocks.begin();
        auto it = blocks.begin();
        for (; it != blocks.end(); it++){
            if (to_del->times_used > (*it)->times_used){
                to_del = *it;
            }
        }
        remove_block(to_del, false);
    }
    void FBR_deleter()
    {
        remove_block_from_old();
    }


    int print_cache(ofstream &logFile){
        if (cache_algo == FBR){
            std::vector<block*>::reverse_iterator rit = fbr_blocks.rbegin();
            for (; rit!= fbr_blocks.rend(); ++rit)
                if ((*rit)->times_used > 0) {
                    logFile << (*rit)->block_path << " " << (*rit)->id << endl;
                }
        }
        else if(cache_algo == LRU) {
            std::vector<block*>::reverse_iterator rit = blocks.rbegin();
            for (; rit != blocks.rend(); ++rit) {
                if ((*rit)->times_used > 0) {
                    logFile << (*rit)->block_path << " " << (*rit)->id << endl;
                }
            }
        }
        else if(cache_algo == LFU)
        {
            std::sort(std::begin(blocks), std::end(blocks),
                      [](block* _lhs, block* _rhs){
                          return _lhs->times_used > _rhs->times_used;});
            for(auto temp: blocks)
            {
                if(temp->times_used > 0)
                {
                    logFile << temp->block_path << " " << temp->id << endl;
                }
            }
        }
        return 0;
    }
    void delete_all_blocks()
    {
        for(size_t i = 0; i < blocks.size(); i++)
        {
            blocks.erase(blocks.begin() + i);
        }
        for (size_t i = 0; i < fbr_blocks.size(); i++)
        {
            fbr_blocks.erase(fbr_blocks.begin() + i);
        }
    }
};


CacheFS *cache;
map<int, pair<const char*, size_t >> fd_to_path;
int CacheFS_init(int blocks_num, cache_algo_t cache_algo,
                 double f_old , double f_new)
{
    struct stat fi;
    stat("/tmp", &fi);
    blksize = (int) fi.st_blksize;
    if (blocks_num <= 0)
    {
        return FAILURE;
    }
    if (cache_algo == FBR)
    {
        if (f_old > 1 or f_old < 0 or f_new < 0 or f_new > 1 or
            f_old + f_new > 1)
        {
            return FAILURE;
        }
    }
    cache = new CacheFS(blocks_num, cache_algo, f_old, f_new, blksize);
    if (cache != nullptr)
    {
        return SUCCESS;
    }
    return FAILURE;
}

int CacheFS_destroy()
{
    cache->delete_all_blocks();
    delete cache;
    cache_hits = 0;
    cache_missed = 0;
    return SUCCESS;
}

int CacheFS_open(const char *pathname)
{
    if (strncmp(pathname, "/tmp", 4))
    {
        return FAILURE;
    }
    int fd = open(pathname, O_RDONLY | O_DIRECT | O_SYNC);
    if (fd == FAILURE)
    {
        return FAILURE;
    }
    struct stat statbuf;
    if (stat(pathname, &statbuf) == -1) {
        return FAILURE;
    }
    fd_to_path[fd] = make_pair(pathname, statbuf.st_size);
    return fd;


}

int CacheFS_close(int file_id)
{
    if (close(file_id) < 0)
    {
        return FAILURE;
    }
    fd_to_path.erase(file_id);
    return SUCCESS;
}

int CacheFS_pread(int file_id, void *buf, size_t count, off_t offset)
{
    if (count + offset > fd_to_path[file_id].second)
    {
        count = fd_to_path[file_id].second - offset;
    }
    off_t new_offset = offset / blksize * blksize;
    char *general_buffer = (char*)buf;
    int number_bytes_read = 0;
    void *temp_buf = aligned_alloc((size_t) cache->get_size(),
                                   (size_t) cache->get_size());
    int currLocation = 0;
    while (currLocation  < (int)count) {
        lseek(file_id, new_offset + currLocation, SEEK_SET);
        char *cache_buffer = (char*)malloc(count * sizeof(char) + 1);
        number_bytes_read = cache->search_block(file_id,
                                                fd_to_path[file_id].first,
                                                count - currLocation,
                                                (offset + currLocation)/blksize,
                                                offset + currLocation,
                                                cache_buffer);
        if (number_bytes_read != -1) // ON THE CACHE
        {
            cache_hits++;
            memcpy(general_buffer, cache_buffer, number_bytes_read);
            general_buffer += number_bytes_read;
            currLocation += number_bytes_read;
            free(cache_buffer);
            continue;
        }
        free(cache_buffer);
        cache_missed++;
        number_bytes_read = (int) read(file_id, temp_buf, blksize);
        if (number_bytes_read < 0) {
            return FAILURE;
        }
        if (number_bytes_read == 0) {
            return currLocation;
        }
        if ((int)count - currLocation < number_bytes_read)
        {
            number_bytes_read = count - currLocation;
        }
        block *block1 = new block(file_id, number_bytes_read, (char*)temp_buf,
                                  new_offset + currLocation,
                                  fd_to_path[file_id].first);
        block1->times_used++;
        cache->add_block(block1);
        memcpy(general_buffer, (char *) temp_buf+ offset - new_offset,
               number_bytes_read);
        general_buffer += number_bytes_read;
        currLocation += number_bytes_read;
    }
    return currLocation;
}

int CacheFS_print_cache (const char *log_path)
{
    ofstream logFile;
    logFile.open(log_path, fstream::out | fstream::app);
    cache->print_cache(logFile);
    logFile.close();
    return SUCCESS;
}

int CacheFS_print_stat (const char *log_path)
{
    ofstream logFile;
    logFile.open(log_path, fstream::out | fstream::app);
    logFile << "Hits number: " << cache_hits << ".\n"\
                "Misses number: " << cache_missed << ".\n";
    logFile.close();
    return SUCCESS;
}
