= Apella App =

== Prerequisites ==
* git
* virtualenvwrapper


== Development instructions ==
=== Backend installation ===
==== Getting the repo and installing dependencies ====
* Clone this repo and checkout to develop branch
* Create a virtualenv for your project
```
$ mkvirtualenv apella
```
* Install python dependencies
```
pip install -r requirements.txt
```

==== Configuration ====
* You must create a settings.conf file. The default path for it is /etc/apella. You can override the path by setting the APELLA_SETTINGS_DIR shell variable. This file overrides Django's settings.py and it should contain at least the following lines (change IP accordingly):
```
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['SERVICE.IP.HERE']
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = DATA_DIR
```
* Create a file named evaluators_allow_addr in the same folder as settings.conf and add the service ip as shown:
```
["SERVICE.IP.HERE", "127.0.0.1"]
```
* Create a file named evaluators_auth_token in the root folder of the repo and add the following token in it:
```
1234567890
```
* You must create an apella.log file. The default path for it is /var/lib/apella/apella.log. You can override the path by setting the LOGFILE shell variable.
* You must create a data folder for the uploaded files and sent emails. The default path for it is /var/lib/apella/data. You can override the path by setting the APELLA_DATA_DIR shell variable.
* The service also expects a resources directory at /usr/lib/apella/resources. Those resources can be found in the resources directory in the root folder of the repo. You can override the path by setting the APELLA_RESOURCES_DIR shell variable.

==== Database initialization ====
* Initialize database and run the migrations
```
$ python manage.py makemigrations apella
$ python manage.py migrate
```

==== Adding dummy data ====
* If you would like to add dummy data to the database you should first create a filename named users.json and add the following data (format is username: password):
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
* Then run the following commands (changing the path):
```
$ export APELLA_PASSWORD_FROM_JSON=/PATH/TO/users.json
$ python run_transcript.py trascript.json
```

==== Running the server ====
* Use the following command:
```
$ python manage.py runserver
```
You can now view your api at http://127.0.0.1:8000/api/

== Frontend installation ==

* Install node and bower dependencies
```
$ cd ui
$ npm install && bower install
```

* Build static files
```
$ ember build --watch --environment=development
```

You can now view the full app at http://127.0.0.1:8000/
