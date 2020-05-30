# EMA - Demo (Event Manager Application)
Event Manager Application with RESTful APIs

## Overview

This Demo is a RESTful Application for Basic Event Manager.
This project is responsible to handle the backed service and data model for event signups.

# How to start? (MacOS Only)

This application runs with Python >= 3.6, please be sure to have this in your machine.
Open preferred terminal and run the following comand to check python version:

```shell
python3 --version
```
```shell
Python 3.7.3
```

## Download Repo

Cloning repo using **ssh** (this options needs public key):

```shell
git clone git@github.com:BeentageBand/ema.git ema-demo
```

Cloning repo using **https** (These option needs login):

```shell
git clone https://github.com/BeentageBand/ema.git ema-demo
```

## Initial Setup (Development

Open preferred terminal and go to the project directory
Run the following steps to setup the entire development environment for python3:


```shell
python3 -m venv venv

source ./venv/bin/activate

python3 -m pip install --user --upgrade pip

python3 -m pip install -r requirements.txt
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

## API Documentation

It is possible to access API documentation while the server is running.  
**Swagger UI**: http://127.0.0.1:8000/doc/


---

# Use Case

The event manager is able handle signups and cancellations from a user (email address) to available events.

### Use Case 1: List Available Events

As a user, 
I want to look at the available events in the application 
so that I can choose which ones I want signup with an email address.

### Use Case 2: Sign Up for an Event

As a user, 
I want to signup my email address to an specific event
so that I can be 

### Use Case 2: Cancel Sign Up for an Event

As a user, 
I want to cancel my signup  to an specific event
so that my email address no longer appears related to the event

### Use Case 3: Accept Email Address for Event Once During Sign Up

As the back-end system (EMA),
I want receive a specific email address once per available  to an event 
so that user can know the emails was signed up to the event

### Use Case 3: Send email to User's Email Address for Event

As the back-end system (EMA),
I want to send an email to user's email address after user signed up to an event 
so that user can know the emails was signed up to the event
