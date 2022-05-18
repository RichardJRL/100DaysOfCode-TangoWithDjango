# Summary of Chapter 3:
## Create a New Django Project
"To create the project run;
`python django-admin.py startproject <name>`,
where `<name>` is the name of the project you wish to create."
This is handled by PyCharm; File -> New Project... Django Project
## Create a New Django App Inside a Project
1. PyCharm does not have a menu option for creating an app (e.g. `rango`) inside the project (e.g. `tangowithdjango`) and its own documentation recommends the same as the book:
`python manage.py startapp <appname>`
2. Inform the Django project about the new app by adding it to the `INSTALLED_APPS` tuple in the project's `settings.py` file
3. In the Django project's `urls.py` file, add a mapping to the app such as `path('rango/', include('rango.urls'))`
4. In the app's subdirectory, create `urls.py` to direct incoming URL strings to app views
5. In the app's `views.py` create the required views, ensuring they each return a `HttpResponse` object.

**Notes:** So far, this assumes that the app is using a subdirectory of the domain, not a subdomain. I.e. we are using http://tangowithdjango/rango/... rather than http://rango.tangowithdjango.com/...

## How to Get the Tango With Django Unit Tests Working
In the main Django project settings.py file make the following alterations:
1. add `import os`
2. edit `'NAME': BASE_DIR / 'db.sqlite3',` to instead read `'NAME': os.path.join(BASE_DIR / 'db.sqlite3'),`
Credit for this solution inevitably goes to [Stack Overflow](https://stackoverflow.com/questions/64634674/django-typeerror-argument-of-type-posixpath-is-not-iterable)!