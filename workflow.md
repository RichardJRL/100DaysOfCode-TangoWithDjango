# Summary of Chapter 3:
## Create a New Django Project
"To create the project run;
`python django-admin.py startproject <name>`,
where `<name>` is the name of the project you wish to create."
This is handled by PyCharm; File -> New Project... Django Project
## Create a New Django App Inside a Project
1. PyCharm does not have a menu option for creating an app (e.g. `rango`) inside the project (e.g. `tangowithdjango`) and its own documentation recommends the same as the book:
`python manage.py startapp <appname>`
2. Inform the Django project about the new app by adding it to the `INSTALLED_APPS` tuple in the project's `settings.py` file. It works with `rango` but both PyCharm and the official Django tutorials suggest it should be `rango.apps.RangoConfig`.
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

## Serve a Static Media File on a Webpage
1. In the Django project's `settings.py` file, create variables for
   1. The static media directory. E.g. `STATIC_DIR = os.path.join(BASE_DIR, 'static')`
   2. Add the variable name of the static media directory to the special Django variable `STATICFILES_DIRS` so Django knows where to look for the static files. E.g. `STATICFILES_DIRS = [STATIC_DIR, ]`
   3. Define the subdirectory of the URL that static media will appear to be in. E.g. `STATIC_URL = '/static/'`
2. Save the static media file to the Django project's `static` directory (or a subdirectory thereof).
3. Open the HTML template file the static media is to be added to and
   1. Add the Django template tag `{% load staticfiles %}` at the top of the file, just *below* the `<!DOCTYPE html>` line (which must always be the first line, just like `#!/bin/bash` should be in a script)
   2. Add a reference to the static media file inside an HTML `<IMG>` tag. E.g. `<img src="{% static 'images/rango.jpg' %}" alt="Picture of Rango" />`

## Serve a Dynamic Media File on a Webpage
1. Create a `media` directory in the Django project's root
2. In the Django project's `settings.py`
   1. Define the media directory's location using the `MEDIA_DIR` variable. E.g. `MEDIA_DIR = os.path.join(BASE_DIR, 'media')`
   2. Add the variable name of the dynamic media directory to the special Django variable `MEDIA_ROOT`. E.g. `MEDIA_ROOT = MEDIA_DIR`
   3. Define the subdirectory of the URL that dynamic meda will appear to be in. E.g. `MEDIA_URL = '/media/'`
3. Open the HTML template file the dynamic media ist to be added to and
   1. Add a reference to the dynamic media file inside an HTML `<IMG>` tag. E.g. `<img src="{{ MEDIA_URL }}cat.jpg" alt="Picture of a cat" />`

# Summary of Chapter 5
## Create a Database
The Django project's `settings.py` should already have a `DATABASES` section configured to use SQLite as the database engine.
1. In the Django application's `models.py` file:c
   1. create classes for each database table with each one inheriting from `models.Model`
   2. Populate the classes with appropriate variables representing each database table field.
   3. Add the `def __str__(self) return self.title` method to show the name of the object when `print()` is called upon it.
   4. The `Meta` class and its useful properties can be inherited as a sub-class of the parent class. This adds useful metadata options to the class such as default ordering by a particular member variable of the class.
2. Run `python manage.py migrate` to initialise the database for the Django project. This creates the standard set of tables necessary to support the project as a whole. It does not create tables for any apps within the project. 
3. Create an administrative user to manage the database by running `python manage.py createsuperuser`.
4. Now and every subsequent time that `models.py` is changed, run `python manage.py makemigrations rango` to create a migrations file
5. Then run `python manage.py migrate` again to apply the changes recorded in the migrations file to the database itself.
6. Optionally, to view the underlying SQL that Django uses to apply the migrations, run `manage.py sqlmigrate <app_name> <migration_number>`
## Configure the Admin Interface
1. Start the development server with `manage.py runserver` and navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
2. Log in with the previously set admim user credentials. I have used:
   - username: RichardJRL
   - password: tangowithdjango
## Create a Population Script for the Database
Create a script to populate your database with realistic and credible data
See the `populate_rango.py` script for more information. It is also a good introduction to Python's list and dictionary data structures.

# Summary of Chapter 6
## Create a Data-Driven Webpage
The goal is to create a webpage that incorporates information sourced from a database query. There are five main steps to accomplish this in Django.
1. `import` the models to be used into `views.py`. E.g. `from rango.models import Category`.
2. In the view function, query the model to obtain the data needed for customising the webpage. E.g. `most_liked_cats = Category.objects.order_by('-likes')[:5]`
3. In the view function, pass the query results into the template's context. This will involve adding the data obtained from the model to a context dictionary.
4. Create or modify the html template to display the data sourced from the model/database query. Use Django template tags to enclose logic e.g. `{% for category in categories }%` and Django template variables e.g. `{{ category.name }}` to display data sourced from the model/database. 
5. Map an URL to the view created.
## Add Slug Fields to Models to Create Readable URLs
The `slugify()` function in Python takes a sentence and replaces the spaces in it with hyphens. This makes the sentence suitable for use in URLs without the need to "percent encode" the whitespace that would otherwise exist as spaces are not permitted in URLs.
1. Import the slugify function `from django.template.defaultfilters import slugify`
2. Add a data member to the model to hold the slugified text. E.g. `slug = models.SlugField()`
3. Overload the default `save` method to automatically update the slug data member every time a model item is updated.
```
def save(self, *args, *kwargs):
   self.slug = slugify(self.name)
   super(Category, self).save(*args, *kwargs)
```
4. To prevent the slug data field from being user-created and have it always auto-generated from another data member, add the following to the app's `admin.py` file
```
class CategoryAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug':('name',)}
# Not forgetting to update the register command with the new class as follows
admin.site.register(Category, CategoryAdmin)
```
5. Now the database migration and updating procedure from Chapter 5 should be carried out to add the slug field to every object in the model.
6. After, *and only after*, updating the database, alter the `slug` data member to be unique with `slug = models.SlugField(unique=true)`

# Create Webpages for Each Item in a Model
