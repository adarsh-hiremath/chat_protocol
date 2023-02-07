#include <iostream>
#include <string>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <netdb.h>
#include <sys/uio.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <fstream>
#include <map>
using namespace std; 

class AccountManager{
    map<char*, vector<char*>> pending;

    void deleteAccount(char* uuid) {
        pending.erase(uuid);
    }

    void createAccount(char* uuid) {
        for (auto it = pending.begin(); it != pending.end(); it++) {
            if (it->first == uuid) {
                cout << "Error: Account already exists." << endl;
                return;
            }
        }
        pending[uuid]; 
    }
};

int main (int argc, char *argv[]) {
  if (argc != 2) {
    cerr << "./server port" << endl; 
    exit(1);
  }  

  int port = atoi(argv[1]);
  char messages[1500];

  sockaddr_in serverAddr;
  bzero((char*)&serverAddr, sizeof(serverAddr));

  serverAddr.sin_family = AF_INET;
  serverAddr.sin_addr.s_addr = INADDR_ANY;
  serverAddr.sin_port = htons(port);

  int serverSd = socket(AF_INET, SOCK_STREAM, 0);
  if (serverSd < 0) {
    cerr << "Error establishing the server socket" << endl;
    exit(0);
  }

  int bindStatus = bind(serverSd, (struct sockaddr*) &serverAddr, sizeof(serverAddr));

  if (bindStatus < 0) {
    cerr << "Error binding socket to local address" << endl;
    exit(0);
  }

  cout << "Waiting for a client to connect..." << endl;




};