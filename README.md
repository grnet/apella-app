Apella App 
==========

Prerequisites
------------
* git
* virualenvwrapper


Development instructions
------------------------

## Backend installation
1. Clone this repo and checkout to develop branch
2. Create a virtualenv for your project
```
$ cd apella_app
$ mkvirtualenv apella
```
3. Install python dependencies
```
pip install -r requirements.txt
```
4. Initialize database and run server
```
$ python manage.py makemigrations apella
$ python manage.py migrate
```
5. If you want to initialize database with dummy data, run
```
$ python run_transcript.py trascript.json
```
6. Add the following line in .bashrc, .zshrc or your shell's configuration
file. Replace ~/apella/ with the path of the repo in your system.
```
export APELLA_SETTINGS_DIR=~/apella
export APELLA_PASSWORD_FROM_JSON=~/apella/users.json
```
7. Create a file named settings.conf in the root folder of the repo and add the
following lines (IP and all ~/apella paths should be changed):
```
DATA_DIR = '~/apella/data'
RESOURCES_DIR = '~/apella/resources'
LOGFILE = '~/apella/apella.log'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['SERVICE.IP.HERE']
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = DATA_DIR
```
8. Create a file named users.json in the root folder of the repo and add all users
to be created. e.g.
```
{
    "helpdeskadmin": "12345",
    "helpdeskuser": "12345",
    "manager": "12345",
    "assistant": "12345",
    "candidate": "12345",
    "professor": "12345",
    "committee": "12345",
    "assistant2": "12345",
    "manager2": "12345",
    "assistant2": "12345",
    "assistant3": "12345"
}
```
9. Create a file named evaluators_allow_addr in the root folder of the repo and add the
service ip as shown:
```
["SERVICE.IP.HERE", "127.0.0.1"]
```
10. Create a file named evaluators_auth_token in the root folder of the repo and add the
following token:
```
1234567890
```
11. Run server
```
$ python manage.py runserver
```
You can now view your api at http://127.0.0.1:8000/api/

## Frontend installation

1. Install node and bower dependencies
```
$ cd ui
$ npm install && bower install
```

2. Build static files
```
$ ember build --watch --environment=development
```

You can now view the full app at http://127.0.0.1:8000/
