
<h1 align="center">
  Client-Server Chat Application
  <br>
</h1>

<h4 align="center">Authored by Adarsh Hiremath and Andrew Palacci</h4>

<p align="center">
  <a href="#key-features">Overview</a> •
  <a href="#how-to-use">Setup</a> •
  <a href="#download">How to Use</a> 
</p>

## Key Features

* We implemented an end-
to-end client-server chat application, first with our
own wire protocol and later with gRPC. 
* As currently implemented, our chat
application supports the following:
- Account creation, login, deletion, and deactivation.
- Sending messages between accounts, even when
some accounts are offline.
- Listing or filtering all users who have created
accounts.
* The source code for our chat application can be
found here. The gRPC implementation is in grpcApp. 
* You can also find our project writeup at template.pdf
* All setup and usage functionality will be for the non-gRPC version of our app.  
  
## Setup

To clone and run this application, you'll need [Python 3.7.2](https://www.python.org/downloads/release/python-372/). We have a list of requirements which you can find in the requirements.txt file. To install these requirements, run the following in your command line: 

```bash
$ pip install -r requirements.txt
```

Next, you'll need to set the appropriate IP address and port. 

## How to Use


