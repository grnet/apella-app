Apella App 
==========

Prerequisites
------------
* git
* virualenvwrapper


Development instructions
------------------------

1. Clone this repo and checkout to devlop branch
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
$ python manage.py runserver
```




