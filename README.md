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

Generate a graphviz graph of app models
---------------------------------------

1. For mac users:
```
$ brew install graphviz
```
2. If needed, reinstall python packages
```
$ pip install -r requirments.txt
```
3. Export apella_db.png
```
$ python manage.py graph_models -a -o apella_db.png
```
