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
3. In the app's `views.py`
    1. Add `from django.http import HttpResponse` to the top of the file.
    2. Create the required views, ensuring they each return a `HttpResponse` object. E.g. `def index(request): return HttpResponse("Hello World")`
4. For basic URL handling, in the Django project's `urls.py` file
    1. Add `from rango import views` at the head of the file
    2. Add a `path` to the `urlpatterns` list to map an URL to the `index` view in the rango app. E.g. `path('', views.index, name='index')`
5. For better URL handling it is better let the app handle its own URL mappings as this is a more portable approach than letting the project urls.py handle everything for all the apps. To do this;
   1. Edit the *Django project's* `urls.py` and 
      1. Add `from django.urls import include`
      2. Add a mapping to the *app's* `urls.py` such as `path('rango/', include('rango.urls'))` 
   2. Edit  the app's `urls.py` and
      1. Add `from django.urls import path`
      2. Add `from rango import views`
      3. Set the variable `app_name` to `rango`
      4. Add path entries to the `urlpatterns` variable. E.g. `path('', views.index, name='index')`

**Notes:** So far, this assumes that the app is using a subdirectory of the domain, not a subdomain. I.e. we are using http://tangowithdjango/rango/... rather than http://rango.tangowithdjango.com/...

## How to Get the Tango With Django Unit Tests Working
In the main Django project settings.py file make the following alterations:
1. add `import os`
2. edit `'NAME': BASE_DIR / 'db.sqlite3',` to instead read `'NAME': os.path.join(BASE_DIR / 'db.sqlite3'),`
Credit for this solution inevitably goes to [Stack Overflow](https://stackoverflow.com/questions/64634674/django-typeerror-argument-of-type-posixpath-is-not-iterable)!

**Notes:** The `django.tests` module uses the standard Python library `unittest`.

# Summary of Chapter 4:
## Create an HTML Template For a Webpage
1. Create the template and save it to the `template` directory created in the Django project root using either or both of the following to allow the insertion of dynamically generated content
   1. Use Django template variables `{{ variable_name }}` or
   2. Use Django template tags `{% tag_name %}`
2. Edit or create a new view within an application's `views.py` file.
   1. Add `from django.shortcuts import render` to the top of the file
   2. Add any specific dynamic logic to the view. E.g. querying a database for values and storing them in a list.
   3. Within the view, construct a dictionary object to pass to the template engine as part of the template's context. E.g. `context_dict = {'price': '£4.99'}`
   4. Use the `render()` function to generate an HttpResponse object as the view's return value. E.g. `render(request, 'rango/index.html', context=context_dict)`
3. Map the view, *if it is a new one*, to an URL by modifying the Django project's `urls.py` file OR the application's `urls.py` file as required.

## Serving a Static Media File on a Webpage
1. In the Django project's `settings.py` file, create variables for
   1. The static media directory. E.g. `STATIC_DIR = os.path.join(BASE_DIR, 'static')`
   2. Add the variable name of the static media directory to the special Django variable `STATICFILES_DIRS` so Django knows where to look for the static files. E.g. `STATICFILES_DIRS = [STATIC_DIR, ]`
   3. Define the subdirectory of the URL that static media will appear to be in. E.g. `STATIC_URL = '/static/'`
2. Save the static media file to the Django project's `static` directory (or a subdirectory thereof).
3. Open the HTML template file the media is to be added to and
   1. Add the Django template tag `{% load staticfiles %}` at the top of the file, just *below* the `<!DOCTYPE html>` line (which must always be the first line, just like `#!/bin/bash` should be in a script)
   2. Add a reference to the static media file inside an HTML `<IMG>` tag. E.g. `<img src="{% static 'images/rango.jpg' %}" alt="Picture of Rango" />`

## Serving a Dynamic Media File on a Webpage
pg. 62