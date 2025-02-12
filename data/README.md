# Installation Instructions
There are 2 steps for the AOMM FastAPI project/application installation. 
The application provides the end to end complete functionality for navigation menu, user management, login, dashboard and analysis data display and Self Assessment Form submission.

## Pre-requisites
1. Microsoft VS Code installed with Python 3.12 or higher
2. PostgreSQL and pgAdmin software is installed locally
3. pip is installed on Windows

## How to Install PIP on Windows ?
PIP is a powerful package management system used to install and manage software packages and libraries written in Python. PIP stands for “Preferred Installer Program” or “Pip Installs Packages.” To use PIP, you must install Python on your Windows machine.

This article provides a step-by-step guide on how to install and configure PIP on Windows, along with tips for managing Python packages effectively.

### Checking if Python is Installed
Before installing PIP, you need to ensure that Python is already installed on your system. You can check this by running the following command in the command prompt
```python
python --version
```
If it is installed, You will see something like this:
```python
Python 3.12.3
```
If it is not installed, you can install it with the help of this article: [How to install Python on Windows](https://www.geeksforgeeks.org/how-to-install-python-on-windows/). 

### Installing Python PIP on Windows
Installing pip in Windows is very easy. You just need to follow the given steps to install pip and some additional steps to finally use it. By these steps, we can see how to pip install on Windows. To ensure proper installation and use of pip we need to tick this checklist to install pip Python:

   1 Download PIP
   2 Install PIP
   3 Verify Installation 

#### Step 1: Download PIP & Install Python pip using Python cURL
Curl is a UNIX command that is used to send the PUT , GET, and POST requests to a URL. This tool is utilized for downloading files, testing REST APIs, etc.

It downloads the get-pip.py file.

Follow these instructions to pip windows install: 

Instruction 1: Open the cmd terminal

Instruction 2: In python, a curl is a tool for transferring data requests to and from a server. Use the following commands to request:  
```python
https://bootstrap.pypa.io/get-pip.py
```

```python
python get-pip.py
```
Instruction 3: Now wait through the installation process. Voila! pip is now installed on your system.

#### Step 2: Verification of the Installation Process
One can easily verify if the pip has been installed correctly by performing a version check on the same. Just go to the command line and execute the following command: 
```python
pip -V
```
or
```python
pip --version
```

#### Step 3: Add the PIP directory to PATH variable under System Variables (Windows Environment Variables)

### How to Upgrad Pip On Windows?

pip can be upgraded using the following command. 

```python
python -m pip install -U pip
```

## Install the FastAPI-template project

### Unzip the FastAPI AOMM application (FastAPI-AOMM.zip) file
Download and copy the zip file to a local folder e.g. C:\workspace and unzip all its content.
Or download from github
### Open command prompt and change directory to the FastAPI-template project.
```shell
cd fastapi-aomm
```

### Open VS Code.
```shell
code .
```

### Create database in PostgreSQL using pgAdmin tool.
Open pgAdmin and create local database "aomm-data"

Open db-query window in pgAdmin after selecting the database "aomm-data".

Copy and paste the content of file \fastapi-aomm\postgres\setup_db.sql to the query window and execute.

Next, copy and paste the content of file \fastapi-aomm\postgres\setup_schema.sql to the query window and execute.

Voila! Database schema is created. 

Add data to the tables using the insert_csv.py utility

```python
python insert_csv.py
```

```sql
SELECT * FROM public.operation_sub_group_map;
```

Sample data for operations and operation_sub_group and other data is populated.

Now back to VS Code...

### Install FastAPI libraries
Open a new Terminal window in VS Code - from fastapi-aomm project root and execute the following command.
```shell
pip install -r requirements.txt
```

### Start and test the application
```shell
uvicorn main:app --reload
```

Create new user by going to URL http://localhost:8000/signup

The password is stored in encrypted format (one way ecryption) and is only known to the actual user.

