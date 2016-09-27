Apella App 
==========

Prerequisites
------------
* git
* virualenvwrapper


Development instructions
------------------------

## Backend installation
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
4. Clone `APIMAS` repo and checkout the appropriate branch.
Then install the package with virtualenv activated
```
$ git clone ssh://phab-vcs-user@phab.dev.grnet.gr:222/diffusion/APIMAS/apimas.git
$ cd apimas
$ python setup.py install

```

4. Initialize database and run server
```
$ python manage.py makemigrations apella
$ python manage.py migrate
```
5. If you want to initialize database with dummy data, run
```
$ python run_transcript.py test/trascript.json
```

6. Run server
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
