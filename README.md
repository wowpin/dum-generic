# dum-generic has been re-designed, improved and moved to https://github.com/wowpin/dumserver - new repository, actively developed and properly tracked.










# dum-generic
A modern MU* engine

## What is it?
DUM is a hobby project attempting to develop a feature-rich Python codebase for a MUD style game. It is building on brillinat work by Mark Frimston, be sure to check out his Mud-Pi project (https://github.com/Frimkron/mud-pi).

> Note: A **dev server** running `dum-generic` has been deployed! Feel free to get in touch via email (bartek.radwanski@gmail.com) if you'd like to try it out!

## Features
Check out http://dumengine.wikidot.com/dum-v0-1-feature-summary for a longer description of currently implemented features. The Wiki page will hopefully help you understand how certain things have been designed. I did try my best to comment the code in a coherent manner, many comments come from the original project by Mark Frimston - I would highly recommend familiarising yourself with his work (https://github.com/Frimkron/mud-pi) for improved understanding of basic design decisions I have expanded on. In summary following concepts have so far been implemented:
* Rooms
* Player chat
* NPCs
* Basic inventory, character sheet and items
* Environmental actors
* PvE and PvP combat
* Database
* Player authentication
* 256 ANSI color support on compatible MUD clients

## Running the Server
Any environment capable of running Python3 + MySQL will do. My own development environment is as follows:
- Google Cloud Instance running Ubuntu 18.04.1 LTS
- Python3 3.6.5-3ubuntu1
- Mysql-server 5.7.23-0ubuntu0.18.04.1

Follow steps below to get things up and running. Somewhere down my TODO list is asome sort of an automated batch, which would install all the prerequisites, set up the database etc. I'm always happy to help if you need a hand or get stuck at any point.

1. Spin up an Ubuntu instance
2. `sudo apt-get update`
3. `sudo apt-get upgrade`
4. Install MySQL environment:
	https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04
5. Install Python3 environment (Step 1 only):
	https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04
6. Install PyMysql:
	`sudo pip3 install pymysql`
7. Create 'dumdb' user in MySQL and grant all privileges:
  ```
	CREATE USER '<database_user>'@'localhost' IDENTIFIED BY '<database_password>';
	GRANT ALL PRIVILEGES ON * . * TO 'dumdb'@'localhost';
	FLUSH PRIVILEGES;
  ```
8. Create dum database and select it:
  ```
	CREATE DATABASE <database_name>;
	USE <database_name>;
  ```
9. Import the database structure by pasting database-dump.sql into mysql prompt.
10. Place the following files in a directory of your choice:
  ```
	simplemud-generic.py
	mudserver.py
	functions.py
	cmsg.py
  ```
11. Configure database connection details in the Database section in `config.ini`:
```
[Database]
Hostname: localhost
Port: 3306
User: <user>
Pass: <password
DB: <db name>
```
12. Run `simplemud-generic.py` using `python3`. You will be greeted by some log entries:
```
13/09/2018 11:51:39 [Server Boot] 
13/09/2018 11:51:39 [info] Rooms loaded: 6
13/09/2018 11:51:39 [info] State Save interval: 10 seconds
13/09/2018 11:51:39 [info] Connecting to database
13/09/2018 11:51:39 [info] NPCs loaded: 3
13/09/2018 11:51:39 [info] Environment Actors loaded: 2
13/09/2018 11:51:39 [info] Items loaded: 2
13/09/2018 11:51:39 [info] Closing database connection
```
13. You can now connect to the server via Telnet on port 35123 (port nubmer is configurable in `mudserver.py`)

## What now?
I'd love to carry on developing this, it has been pretty fun so far. IF anyone feels like they want to take it even further, feel free to get in touch.

## Get in touch
Bartek.Radwanski@gmail.com

