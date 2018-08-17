#include <iostream>
#include <cstring>
#include <netdb.h>
#include <unistd.h>
#include <map>
#include <set>
#include <sstream>
#include <algorithm>
#include <arpa/inet.h>
#include <vector>

using namespace std;

#define MAX_CLIENTS 30
#define MAX_NAME 30
#define MAX_MSG_LENGTH 1024
#define IP "127.0.0.1"
#define ERROR_MSG(a,b) cout << "ERROR " << a << b << ".\n"


class Server {
private:
    int serverSockfd;
    fd_set clientsfds;
    fd_set readfds;
    map<int, string> clients;
    map<string, set<int>> groups;

    // ----------------------------Messages-------------------------------------
    int read_data(int sock, char* buff){
        int read_bytes, counter=0;
        do {
            read_bytes = read(sock, buff, MAX_MSG_LENGTH);
            if (read_bytes == 0){
                return -1;
            }
            if (read_bytes < 0){
                // error reading bytes
                ERROR_MSG("read ", errno);
            }
            counter += read_bytes;
        } while (buff[counter-1] != '\n');
        return counter;
    }

    int write_data(int fd, const char *buf, size_t n) {
        size_t bcount; /* counts bytes read */
        ssize_t br; /* bytes read this pass */
        bcount = 0;
        br = 0;
        while (bcount < n) { /* loop until full buffer */
            br = write(fd, buf, n - bcount);
            if (br > 0) {
                bcount += br;
                buf += br;
            }
            if (br < 1) {
                ERROR_MSG("write ", errno);
                return -1;
            }
        }
        return 0;
    }

    ssize_t sendOutputs(int sockfd, const char *msg1, size_t len1,
                     const char *msg2, size_t len2){
        int r2;
        write_data(STDOUT_FILENO, msg1, len1);
        r2 = write_data(sockfd, msg2, len2);
        return (r2 == 0);
    }

    void sendRegisterMessage(bool succ, int sockfd, string client_name){
        string client_msg, server_msg;
        if (succ) {
            client_msg = "Connected successfully.\n";
            server_msg = string(client_name) + " " + "connected.\n";
        }
        else {
            client_msg = "Client name is already in use.\n";
            server_msg = "";
        }
        sendOutputs(sockfd, server_msg.c_str(), server_msg.size(),
                    client_msg.c_str(), client_msg.size());
    }

    void sendGroupMessage(bool succ, int sockfd, string client_name,
                          string group_name){
        string client_msg, server_msg;
        ostringstream msg;
        if (succ){
            msg << "Group \"" << group_name
                << "\" " << "was created successfully.\n";
        }
        else {
            msg << "ERROR: failed to create group "
                << "\"" << group_name << "\".\n";
        }
        client_msg = msg.str();
        server_msg = string(client_name) + ": " + client_msg;
        sendOutputs(sockfd, server_msg.c_str(), server_msg.size(),
                    client_msg.c_str(), client_msg.size());
    }

    void sendSendMessage(bool succ, int sockfd, string client_name,
                          string sendto, string message){
        string client_msg, server_msg;
        ostringstream s;
        if (succ){
            s << client_name << ": \"" << message
              << "\" was sent successfully to " << sendto << ".\n";
            client_msg = "Sent successfully\n";
        }
        else{
            s << client_name << ": ERROR: failed to send \"" << message
              << "\" to " << sendto << ".\n";
            client_msg = "ERROR: failed to send\n";
        }
        server_msg = s.str();
        sendOutputs(sockfd, server_msg.c_str(), server_msg.size(),
                    client_msg.c_str(), client_msg.size());
    }

    void sendWhoMessage(bool succ, int sockfd, string sender_client_name,
                        string ret_clients_names){
        string client_msg, server_msg;
        if (succ){
            client_msg = ret_clients_names;
        }
        else{
            client_msg =
                    ": ERROR: failed to receive list of connected clients\n";
        }
        server_msg = sender_client_name +
                ": Requests the currently connected client names.\n";
        sendOutputs(sockfd, server_msg.c_str(), server_msg.size(),
                    client_msg.c_str(), client_msg.size());
    }

    void sendExitMessage(int sockfd, string client_name){
        string client_msg = "Unregistered successfully.\n";
        string server_msg = client_name + ": " + client_msg;
        sendOutputs(sockfd, server_msg.c_str(), server_msg.size(),
                    client_msg.c_str(), client_msg.size());
    }

    // ------------------------End Messages-------------------------------------


    int establish(unsigned short portnum) {
//        char servername[MAX_NAME + 1];
        int s;
//        struct sockaddr_in sa;
//        struct hostent *hp;

        //hostnet initilization
//        gethostname(servername, MAX_NAME);
//        hp = gethostbyname(servername);
//        if (hp == NULL)
//            return (-1);
//        //sockaddrr_in initlization
//        memset(&sa, 0, sizeof(struct sockaddr_in));
//        sa.sin_family = hp->h_addrtype;
//        /* this is our host address */
//        memcpy(&sa.sin_addr, hp->h_addr, hp->h_length);
//        /* this is our port number */
//        sa.sin_port = htons(portnum);

        struct sockaddr_in my_addr;
        my_addr.sin_family = AF_INET;
        my_addr.sin_port = htons(portnum);
        inet_aton(IP, &(my_addr.sin_addr));
        memset(&(my_addr.sin_zero), '\0', 8);

        /* create socket */
        if ((s = socket(AF_INET, SOCK_STREAM, 0)) < 0)
            return (-1);
        if (bind(s, (struct sockaddr *) &my_addr, sizeof(struct
                sockaddr_in)) < 0) {
            close(s);
            return (-1);
        }
        listen(s, 10); /* max # of queued connects */
        return (s);
    }

    void terminateServer() {
        cout << "EXIT command is typed: server is shutting down" << endl;
        exit(0);
    }

    void connectNewClient(int serversocket) {
        int t; /* socket of connection */
        if ((t = accept(serversocket, NULL, NULL)) < 0)
            exit(1); // error
        FD_SET(t, &clientsfds);
        FD_CLR(serversocket, &readfds);
    }

    void serverStdInput() {
        char buf[1024+1] = "";
        if(read_data(STDIN_FILENO, buf) == -1)
            return;
        if (string(buf) == "EXIT\n") {
            int res;
            for (auto &c:clients) {
                res = close(c.first);
                if (res < 0)
                    ERROR_MSG("close", errno);
            }
            if(close(serverSockfd) < 0)
                ERROR_MSG("close", errno);
            terminateServer();
        }
    }

    int findFDByClientName(string client_name){
        for (auto it:clients){
            if (it.second == client_name){
                return it.first;
            }
        }
        return -1;
    }

    void handleRegisterRequest(int sockfd, string name){
        // check name not already in use
        if ((findFDByClientName(name) == -1) &
                (groups.find(name) == groups.end())){
            clients[sockfd] = name;
            sendRegisterMessage(true, sockfd, name);
        }
        else {
            sendRegisterMessage(false, sockfd, name);
        }
    }

    void handleCreateGroupRequest(int sockfd, char *buf) {
        // skip the command type
        strtok(buf, " ");

        string group_name = string(strtok(NULL, " "));
        // check if not a unique name
        if ((groups.find(group_name) != groups.end()) |
                (findFDByClientName(group_name) != -1)){
            // error, group name already exists
            sendGroupMessage(false, sockfd, clients[sockfd], group_name);
            return;
        }

        char* client_name;
        set<int> group_members;
        int memberFD;

        group_members.insert(sockfd); // add current client to members set
        while ((client_name = strtok(NULL, ",")) != NULL) {
            memberFD = findFDByClientName(string(client_name));
            if (memberFD < 0){
                // error - member was not found
                sendGroupMessage(false, sockfd, clients[sockfd], group_name);
                return;
            }
            group_members.insert(memberFD);
        }

        if (group_members.size() < 2){
            // error
            sendGroupMessage(false, sockfd, clients[sockfd], group_name);
            return;
        }
        // Success
        groups[group_name] = group_members;
        sendGroupMessage(true, sockfd, clients[sockfd], group_name);
    }


    void handleSendRequest(int sockfd, char *buf) {
        // pass the command type
        strtok(buf, " ");

        // check if client contains current client (current socket FD)
        // if not this message (is the first one) contains the client's name
        if (clients.find(sockfd) == clients.end()){
            handleRegisterRequest(sockfd, string(strtok(NULL, " ")));
            return;
        }
        string name = string(strtok(NULL, " "));
        string message = string(strtok(NULL, "")); // get the rest of message
        // check if name is client name
        if (groups.find(string(name)) == groups.end()){
            // name is client name
            if ((name == clients[sockfd]) | (findFDByClientName(name) == -1)){
                // error - try to send message to himself ot client is not exists
                sendSendMessage(false, sockfd, clients[sockfd], name, message);
            }
            else{
                string all_msg = clients[sockfd] +": " + message + "\n";
                bool sent = write_data(findFDByClientName(name),
                                       all_msg.c_str(),all_msg.size()) == 0;
                sendSendMessage(sent, sockfd, clients[sockfd], name, message);
            }

        }
        else{
            // check if client is a member in 'name' group
            set<int> members = groups[name];
            if (members.find(sockfd) == members.end()){
                sendSendMessage(false, sockfd, clients[sockfd], name, message);
            }
            else{
                bool allSent = true;
                // send every one in the group the message
                for (auto it: members){
                    if (it != sockfd){
                        string all_msg = clients[sockfd] +": " + message + "\n";
                        if(write_data(it, all_msg.c_str(),
                                      all_msg.size()) == -1)
                            allSent = false;
                    }
                }
                sendSendMessage(allSent, sockfd,
                                clients[sockfd], name, message);
            }
        }
    }

    void handleWhoRequest(int sockfd, char *buf) {
        string s_connected_clients = "";
        vector<string> conn_clients;
        for(auto client: clients){
            conn_clients.push_back(client.second);
        }
        sort(conn_clients.begin(), conn_clients.end());
        bool first_time = true;
        for(auto &client : conn_clients){
            if(first_time){
                first_time = false;
                s_connected_clients += client;
            } else
                s_connected_clients += "," + client;
        }
        s_connected_clients += "\n";
        sendWhoMessage(true, sockfd, clients[sockfd], s_connected_clients);
    }

    void handleExitRequest(int sockfd, char *buf) {
        string client_name = clients[sockfd];
        clients.erase(sockfd);
        for (auto &group : groups)
            group.second.erase(sockfd);
        sendExitMessage(sockfd, client_name);
        FD_CLR(sockfd, &clientsfds);
        // close the socket
        int res = close(sockfd);
        if (res < 0)
            ERROR_MSG("close", errno);
    }

    bool handleClientRequest(int sockfd) {
        // Assume valid input
        char buf[MAX_MSG_LENGTH+1]="";
        ssize_t len = read_data(sockfd, buf);
        if(len == -1)
            return false;
        len--;
        buf[len] = 0;
//        ssize_t len = read(sockfd, buf, MAX_MSG_LENGTH);
        // save buffer
        char copy_buf[MAX_MSG_LENGTH+1] = "";
        memcpy(copy_buf, buf, sizeof(buf));

        char* command = strtok(buf, " ");
        if (command == NULL){
            return false; // NO message
        }
        if (len < 0){
            cout << "Error reading" << endl;
        }
        string s_command = string(command);
        if (s_command == "create_group") {
            handleCreateGroupRequest(sockfd, copy_buf);
        } else if (s_command == "send") {
            handleSendRequest(sockfd, copy_buf);
        } else if (s_command == "who") {
            handleWhoRequest(sockfd, copy_buf);
        } else if (s_command == "exit") {
            handleExitRequest(sockfd, copy_buf);
            return false;
        }
        return true;
    }

public:
    Server(int argc, char *argv[]){
        unsigned short portnum = (unsigned short) atoi(argv[1]);
        serverSockfd = establish(portnum);
        if (serverSockfd < 0)
            exit(-1);

        FD_ZERO(&clientsfds);
        FD_SET(serverSockfd, &clientsfds);
        FD_SET(STDIN_FILENO, &clientsfds);
    }
    ~Server(){}

    int runServer(){
        int numSockToHandle;
        while (1) {
            readfds = clientsfds;
            if ((numSockToHandle = select(MAX_CLIENTS + 1, &readfds,
                                          NULL, NULL, NULL)) < 0) {
                ERROR_MSG("select ", errno);
                exit(1);
            }
            if (FD_ISSET(serverSockfd, &readfds)) {
                connectNewClient(serverSockfd);
            }
            if (FD_ISSET(STDIN_FILENO, &readfds)) {
                serverStdInput();
            }


            // check every file descriptor for an action
            for (int fd = 4; (fd < 3+MAX_CLIENTS) &
                    (numSockToHandle > 0); ++fd) {
                if ((fd != STDIN_FILENO) & (fd != serverSockfd) &
                        (FD_ISSET(fd, &readfds))) {
                    if (handleClientRequest(fd)) {
                        FD_SET(fd, &clientsfds);
                    }
                    numSockToHandle--;
                }
            }
        }
    }
};


int main(int argc, char* argv[]) {
    if (argc != 2){
        cout << "Usage: whatsappServer portNum" << endl;
        exit(0);
    }
    Server s(argc, argv);
    return s.runServer();
}

