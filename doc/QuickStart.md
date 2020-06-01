# Quick Start (Install)

### How to start? (MacOS Only)

This application runs with Python >= 3.6, please be sure to have this in your machine.
Open preferred terminal and run the following comand to check python version:

```shell
python3 --version
```
```shell
Python 3.7.3
```

### Download Repo

Cloning repo using **ssh** (this options needs public key):

```shell
git clone git@github.com:BeentageBand/ema.git ema-demo
```

Cloning repo using **https** (These option needs login):

```shell
git clone https://github.com/BeentageBand/ema.git ema-demo
```

## Initial Setup (Development)

Open preferred terminal and go to the project directory
Run the following steps to setup the entire development environment for python3:


```shell
python3 -m venv venv

source ./venv/bin/activate

python3 -m pip install --user --upgrade pip

python3 -m pip install -r requirements.txt
```

## Configure Setup

Configurations as in ``setup.cfg``. Review and update configuration as needed before launching server.

### Email SMTP setup

```shell
[EmailSetup] ## Email Server Setup
host = localhost ## Server host
port =1025 ## Server port. Check port is SSL or TLS
ssl = False ## flag to determine if connection is SSL (True) or TLS (False)
username= <username> ## Email Server Username authentication
password= <password> ## Email Server Password authentication
emailAddress = example@example.com ## Default email to fwd any emails sent from the App
```

## Launch REST Server

Server can be launch if setup was done successfully. This server need Django and REST framework to be launched.
Run the following command to bring up the service:

```shell
python3 manage.py runserver
```

Expect the following output when server is launched successfully:

```shell

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 27, 2020 - 03:12:05
Django version 3.0.6, using settings 'restserver.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
