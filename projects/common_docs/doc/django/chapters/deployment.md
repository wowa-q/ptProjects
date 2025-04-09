# Overview

Read additional material: 
1. [Slides from Maximilian Schwarzmüller](https://github.com/academind/django-practical-guide-course-code/tree/deployment-zz-extra-files/slides) - gives a quick overview of topics (see also [Academy community](https://academind.com/community/))
2. [django-deployment guide](https://www.saaspegasus.com/guides/django-deployment/) - **you must read** to make correct decisions and good planning.
3. [Hosting providers comparison](https://djangostars.com/blog/top-django-compatible-hosting-services/) - pricing model and recommendations


- sqlite is fine, but there are servers, which erase everything as soon you deploy a new version.
- settings need to be updated
- collect static files, that these are available on server. We can't rely on automatic serving the static files, like it was done with the development server (like user uploaded files).
- Handle statis & uploaded files serving: Static file are not served automatically
- Choose a Host + Deploy: dive into servers specific docu

## Database

sqlite holds one file. Downsite: it can be slow in some situations (many users at the same time). Data is lost if the file is deleted.

Is SQL or noSQL database?
With Django SQL is prefered, since model is made for SQL.
SQL options is MySQL or Postgres. 

## Webserver

Django is not a webserver, but just a framework. Listening for incoming requests or handling other server tasks.
You should install a webserver SW for production. => `asgi.py` or `wsgi.py` to be used. They are entry point for the webserver. These files kickof the entire Django application. Most commonly `wsgi.py` is used, but this depends on the webserver. 

## serving static filles

Static files are not handled by Django. Development server, does serve static files for more convinience during the development. For production you have following options:

### Options

1. configure handling static files in `urls.py`:
``` python
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blog.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
This is ok for smaller apps, but it is not efficient performance.

2. Configure the webserver to serve static files and Django app: 
Same server and device but separate processes => better for performance.

3. Use a dedicated service / server to serve the static files: Initial setup is complex, but the performance is the best, because the services are specialized for serving the static files.

## Host selection

Digital ocean provide good documentation. [example](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)

AWS, biggest cloud provider offers hosting web-apps services. You can start for free, even you need a credit card to sign in. It has a good balance between you can configure a lot, but you don't need to configure a lot. 
**check the pricing**

# Deploy

> Make sure before deployment that you run your migrations!

> Also create a superuser

## settings.py 

1. SECRET_KEY
``` python
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'l1s5h%-io2b)u&4__&ms1g=x@b0v+!a!o2z6#sl!t$l45$ah^6'
SECRET_KEY = getenv("SECRET_KEY")
```
This key is generated, when the project was created and is used by Django internally. It must be random and 32 digits long. The key must be kept secret. **DON'T push it to git** Environment variable can be used instead. 

2. DEBUG

``` python
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# better 
# locally IS_DEVELOPMENT is not set -> True. On server you set it to False
DEBUG = getenv("IS_DEVELOPMENT", True) 
```
Set Debug to False. 


3. ALLOWED_HOSTS

Hosting address of the server, which will host this application. Sometimes it is known in advance, but sometimes not. Environment variable shall be used in order to provide the name after the deployment.

``` python
from os import getenv
...

ALLOWED_HOSTS = [
    getenv("APP_HOST") # the name of ENV_VAR can be choosen
]
```
It holds the allowed hosts (The domain under which we host the application)  for the application.


4. DATABASE

```python
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
Here the data base is configured, which shall be used.

Other settings should work per default. 


## Collecting static files

Static files are all, which are provided by you together with the Django application.
```python
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
```
`STATICFILES_DIRS` tells Django the location of the static files. This is useful during the development and in production this can be used to **collect** the them. In production you may collect all the static files, from all Apps and put them into one folder.
`STATIC_ROOT` here the static files can be collected and later be served. 

> You shouldn't mix user uploaded files and own static files. The static file must not be changed by any user.

`manage.py collectstatic` can then be used to collect the static files and copy them into the `staticfiles` folder as configured in `STATIC_ROOT`.

The original files shall be maintained on its original place and before deploying a new version, the command shall be repeated.


## start deploying

1. lockk in the dependencies, which are used (Python packages, incl. Django which were used in the project). We must make sure those packages are installed on the host, too. How this is done, depends on the host. Most support Requirements.txt. 
2. Make sure the Environment variables are used in the settings, as shown above.
3. Configure the Web-Server e.g. AWS Cloud - Elastic Beanstalk:
    1. Click on crerate Application and give it a name
    2. Choose Platform: Python
    3. Upload own application code - the code needs to be prepared for it

### Prepare code for deployment

1. create a `.ebextensions` folder (this is Elastic Beanstalk specific folder name
2. add `django.config` file into this folder
3. create configuration exactly like this:

```
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: PROJECTNAME.wsgi:application
```
Replace the PROJECTNAME with the folder name of the project.
4. Create a zip file, of all the files, which need to be deployd. **Put only those files and folders, which needs to be uploaded**
5. Upload the zip-File and click on _Configure more options_.
6. Scrl to the Environment settings and add the Environment variables as those are used in the `settings.py`. You can add the place holder for `APP_HOST` if you upload the App first time.
7. Click on _Create application_ and the environment will be setup.
8. Click on the link to the App -> loading will fail, because `APP_HOST` is not set and needs to be updated. Click on _Configure_ and update the `APP_HOST` with the link. 

> It is always host specific how to setup SSL or custom domain and is often not for free. Look for host documentation. 

## Choose another database

You can use a sql-server MySQL or PosgreSQL. check the Django documentation if your SQL is supported and install the coresponding Python package. 
AWS provides database service, RDS. You can use this and configure it in settings: 
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': '<your-rds-db-username>',
        'PASSWORD': '<your-rds-db-user-password>',
        'HOST': '<your-rds-db-host>',
        'PORT': '5432'
    }
}
```
> Don't forget to execute the migration and create a superuser after new database is created!
> Take care the secure group is exposed to the internet and not only for local host 
In reality you'll maintain two databases, one for development and one productive.

## serving the static files - not from Django

### Use the web server

Same web-server.
1. create `static-files.config` in `.ebextensions` folder (this is Elastic Beanstalk specific folder name
2. Remove the url config
3. create configuration exactly like this:
```
option_settings:
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: staticfiles
    /files: uploads
```

- `/static` = STATIC_URL: should point to _staticfiles_ folder
- `/files` = MEDIA_URL: should point to _uploads_ folder

### Use a dedicated service
Then the files are not stored anymore in the project, but on the other server. 


## Additional information

- Make Docker Container for Django [guide](https://www.docker.com/blog/how-to-dockerize-django-app/)
- 