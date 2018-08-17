#include <iostream>
#include <cstring>
#include <netdb.h>
#include <unistd.h>
#include <regex>


#define MAX_MSG 1024
#define NAME 1
#define IP 2
#define PORT 3
#define NAME_REGEX "^[a-zA-Z0-9]*$"
#define USED_NAME "Client name is already in use.\n"



using namespace std;

class Client{
    int clientFD;
    string myname;

    void connect_failure(){
        cout << "Failed to connect the server";
        exit(1);
    }

    void tryConnect(char *name, char *hostname, int portnum, int namelen){
        struct sockaddr_in sa;
        struct hostent *hp;
        int s, err;

        if ((hp = gethostbyname(hostname)) == NULL) {
            sysCallERR("gethostbyname", errno);
        }
        memset(&sa,0,sizeof(sa));
        memcpy((char *)&sa.sin_addr, hp->h_addr, hp->h_length);
        sa.sin_family = hp->h_addrtype;
        sa.sin_port = htons((u_short)portnum);
        if ((s = socket(hp->h_addrtype, SOCK_STREAM,0)) < 0) {
            connect_failure();
        }
        if ((err = connect(s, (struct sockaddr *)&sa , sizeof(sa))) < 0) {
            close(s);
            connect_failure();
        }
        clientFD = s; // sets the file descriptor
        myname = name;
        // send to the server message with the name
        char buff[MAX_MSG+1] = "send ";
        strcpy(&buff[5], name);
        send(buff, strlen(buff));
    }

    void printCreateGroupError(string group_name){
        cout << "ERROR: failed to create group "
             << "\"" << group_name << "\".\n";
    }

    void printSendError(){
        cout << "ERROR: failed to send.\n";
    }

    void printWhoError(){
        cout << "ERROR: failed to receive list of connected clients.\n";
    }

    void printExitError(){
        cout << "ERROR: failed to exit.\n";
    }

    void sysCallERR(string sysFunc, int errnum){
        cout << "ERROR: " << sysFunc << " " << errnum <<".\n";
        exit(1);
    }

    void process_create_group(char* buff, int len) {
        char copy_buff[MAX_MSG+1];
        memcpy(copy_buff, buff, len);
        // check valid gruop name and list group names
        regex name_regex(NAME_REGEX);
        
        // skip command
        strtok(buff, " ");

        char* group_name = strtok(NULL, " ");
        char* name;

        // check names are valid
        if (!regex_match(group_name, name_regex)) {
            // error - group name not valid form
            printCreateGroupError(group_name);
            return;
        }
        while ((name = strtok(NULL, ",")) != NULL) {
            if (!regex_match(name, name_regex)) {
                printCreateGroupError(group_name);
                return;
            }
        }
        send(copy_buff, len);
    }

    void send(char* buff, int msglen){
        msglen++;
        buff[msglen-1] = '\n';
        ssize_t count = 0, res;
        while (count < msglen) {
            res = write(clientFD, buff, (size_t) (msglen));
            if (res < 0)
                sysCallERR("write", errno);
            count += res;
            buff += res;
        }
        if (res < 0){
            sysCallERR("write", (int) res);
        }
    }

    void readPrintResponse(){
        char buff[MAX_MSG+1] = "";
        int read_bytes, counter=0;
//        char *b = buff;
//        read_bytes = read(clientFD, b, MAX_MSG);
        do {
            read_bytes = read(clientFD, buff, MAX_MSG);
            if (read_bytes == 0){
                // server terminated
                exit(1);
            }
            if (read_bytes < 0){
                // error reading bytes
                sysCallERR("read", errno);
            }
            counter += read_bytes;
        } while (buff[counter-1] != '\n');
        cout << buff;
        fflush(STDIN_FILENO);
        if (strcmp(buff, USED_NAME) == 0){
            exit(1);
        }
    }

    void process_send(char* buff, int len) {
        char copy_buff[MAX_MSG+1];
        memcpy(copy_buff, buff, len);
        // skip command
        strtok(buff, " ");

        //check tosend name and message
        char* tosend = strtok(NULL, " ");
        char* message = strtok(NULL, " ");
        if ((tosend != NULL) & (message != NULL)) {
            regex name_regex(NAME_REGEX);
            if ((strcmp(tosend, myname.c_str()) != 0) &
                    (regex_match(tosend, name_regex) != 0)) {
                send(copy_buff, len);
            }
            else {
                printSendError();
            }
        }
        else {
            printSendError();
        }
    }

    void process_who(char* buff, int len) {
        char copy_buff[MAX_MSG+1];
        memcpy(copy_buff, buff, len);

        // skip command
        strtok(buff, " ");
        if (strtok(NULL, " ") != NULL) { //check no more characters
            printWhoError();
        } else {
            send(buff, len);
        }
    }

    void process_exit(char* buff, int len) {
        char copy_buff[MAX_MSG+1];
        memcpy(copy_buff, buff, len);

        // skip command
        strtok(buff, " ");
        if (strtok(NULL, " ") != NULL) { //check no more chars
            printExitError();
        } else {
            send(buff, len);
            readPrintResponse();
            if (close(clientFD)< 0)
                sysCallERR("close", errno);
            exit(0);
        }
    }

    void handleSTDInput(){
        char buff[1024] = "";
        char copy_buff[1024] = "";
        read(STDIN_FILENO, &buff, 1024);
        // save buff
        memset(copy_buff, 0, sizeof(copy_buff));
        memcpy(copy_buff, buff, sizeof(buff));

        int msglen=strlen(buff)-1;
        copy_buff[msglen] = 0; // delete '\n'
        buff[msglen] = 0; // delete '\n'
        char* command = strtok(buff, " ");
        if (string(command) == "create_group") {
            process_create_group(copy_buff, msglen);
        } else if(string(command) == "send") {
            process_send(copy_buff, msglen);
        } else if (string(command) == "who") {
            process_who(copy_buff, msglen);
        } else if(string(command) == "exit") {
            process_exit(copy_buff, msglen);
        } else {
            cout << "ERROR: Invalid input.\n";
        }
    }


public:
    Client(char *name, char *hostname, char *port){
        int int_port = atoi(port);
        tryConnect(name, hostname, int_port, (int) strlen(name));
    }
    ~Client(){}

    void runClient(){
        fd_set readfds;
        fd_set copy_set;
        FD_ZERO(&copy_set);
        FD_SET(clientFD, &copy_set);
        FD_SET(STDIN_FILENO, &copy_set);
        while(1){
            readfds = copy_set;
            if (select(4, &readfds, NULL, NULL, NULL) < 0) {
                sysCallERR("select", errno);
            }
            if (FD_ISSET(clientFD, &readfds)) {
                readPrintResponse();
            }
            if (FD_ISSET(STDIN_FILENO, &readfds)) {
                handleSTDInput();
            }
        }
    }

};

int main(int argc, char *argv[]){
    if (argc != 4){
        cout << "Usage: whatsappClient clientName serverAddress serverPort";
        exit(0);
    }
    Client c(argv[NAME], argv[IP], argv[PORT]);
    c.runClient();
}
