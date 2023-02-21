
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

| Syntax | Description |
| --- | ----------- |
| Usage: c &#124; \<username\> | Create an account. |
| Usage: l &#124; \<username\>  | Log into an account. |
| Usage: u | List all users and their activity status. | 
| Usage: s &#124; \<recipient_username\> &#124; \<message\> | Send a message to a user. | 
| Usage: d &#124; \<confirm_username\> | Delete an account. | 
| Usage: f &#124; \<filter_regex\> | Filter accounts using a wildcard. | 
| Usage: h | Print a list of all the commands. |
