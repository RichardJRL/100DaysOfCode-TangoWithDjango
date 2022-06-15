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

## Create Webpages for Each Item in a Model
To create a webpage that can display each item in a model that matches a particular instance of another model which will have the URL format `/appname/modelname/model-item-name`, the following must be done.
Or in the context of the Rango app, it is desired that there be a page for each individual category stored in the category model, and each of these category pages will display a list of items from the Page model that are associated with that particular category.
1. Import the model containing the items to be displayed on each page in to the Python app's views.py
2. Create a new view in views.py named `show_[modelname].py`. It's second argument should be te parameter use to query the model. 
3. The category model can be queried for an item matching a string, e.g. `category = Category.objects.get(slug=category_name_slug)`.
4. The returned Category item can then be used to select items from the Page model that reference that particular category item. E.g. `pages = Page.objects.filter(category=category)`
5. The returned `pages` can then be passed to the return render request as part of the context_dictionary to render the items retrieved in the appropriate view. 
6. Add an HTML template in `templates/[app_name]/` to display the view. It can make use of Django's template tags `{% ... %}` to include logic such as if statements and for loops to check if a category exists and iterate over objects to display the list of objects (exposed using template variable syntax `{{ ... }}`) that is required for the webpage.
7. Update the Python app's `urls.py` to map the new view to an URL. This is complicated by part of the URL being a slug string drawn from one of the models. This can be accomodated with syntax such as: `path('category/<slug:category_name_slug>/', views.show_category, name='show_category')`

# Summary of Chapter 7
## Workflow for Form Creation
1. Create `forms.py` within the Django App's directory to store form-related classes.
2. Create a `ModelForm` class for each model/database that is to be represented.
3. Customise each form.
4. Create or update a view to handle the form
   1. How to display the form.
   2. How to save the form data.
   3. How to alert the user to input errors.
5. Crate or update a template to display the form.
6. Add an `urlpattern` to map to the new view.

## Create `ModelForm` Classes
Within the Django app's `forms.py` file, the `ModelForm` class will be used as the class to inherit from when creating new forms. `ModelForm` is a helper class that provides a pre-existing model for forms that can be built upon. It can be used after `from django import forms` is declared.
Data fields on the form are declared as variables e.g. `name = forms.CharField(max_length=128, help_text='foo')` and they are based upon a `...Field` member of the `ModelForm` class that helps insure the input is correct.
The class then contains a `Meta` sub-class (Meta being short for metadata) which links the ModelForm to a particular model/database. e.g.
```
class Meta:
   model = Category
   fields = ('name')
```
## Create Views that use Forms
In the Django app's `views.py`, import the previously created form from `forms.py` then create a view that makes use of it
```
from rango.forms import CategoryForm
from django.shortcuts import redirect
...
def add_category(request):
   form = CategoryForm()
   if request.method == 'POST':
      form = CategoryForm(request.POST)
      if form.is_valid():
         form.save(commit=True)
         return redirect('/index/')
   else:
      print(form.errors)
   return render(request, 'rango/add_category.html', {'form': form})
```
## Create a Template for the Form
In the templates directory for the Django app, create a new HTML file to hold the form template. One quirk of HTML forms is that the form must include separate sections for **both** *visible* **and** *invisible* fields. Invisible fields being ones where the user is not required to make their own input, but may still be needed to set default values (if defaults are not set in the model itself, for example). An example of a form template is:
```
<form id="category_form" method="post" action="/rango/add_category/">
   {% csrf_token %}
   {% for hidden in form.hidden_fields %}
      {{ hidden }}
   {% endfor %}
   {% for field in form.visible_fields %}
      {{ field.errors }}
      {{ field.help_text }}
      {{ field }}
   {% endfor %}
   <input type="submit" name="submit" value="Create Category" />
</form>
```
## Map the Form View to an URL
This is the final step to adding a form - mapping the form view to an URL and this is accomplished as earlier.

# Summary of Chapter 8
## HTML Templates
The concept behind HTML template files is to repeat as little HTML content as possible. Common page elements, (e.g. title, sidebar, menu, footer) can be broken out into template files and a link to the template file is then included in every invidual webpage which then do not need to repeat (and keep up-to-date) common HTML elements.
## HTML Base Template
This should be the template which brings together all the various elements common to every page on the website - title, header etc... and is the only one that needs to begin with `<!DOCTYPE html>`. That first line should be followed with `{% load staticfiles %}`.
Thereafter, it should also contain all the common HTML elements from the opening <HTML> tag to the closing <HTML> tag. Within the common elements, Django template tags that delineate blocks of HTML that will be replaced when individual site pages are composed should be located. These are the `block` template tags such as `{% block body_block %} ... {% endblock %}` They may be empty or contain default elements that will be displayed if an individual page does not override them with custom content defined in its own identically named `block` template tag section.
## Individual Page Templates
Other pages that are to make use of the base HTML template must begin with a template tag such as `{% extends 'site/base.html' %}` which informs Django that this HTML file is a customisation for the base template which is named within the `extends` tag. The elements of the base template that are to be replaced are defined within the same `block` tags that the base template possesses.
`{% load staticfiles %}` should also be present at the top of each HTML file, regardless of whether the base template also includes it.
## Relative URLs in Templates
It is also convenient to use labels for own-site URLs instead of actual paths. For example replacing a link such as `<a href="/site/about/">About</a>` with a label like `<a href="{% url 'site:about' %}">About</a>`. This relies on the `app_name = site` variable being used in the Django app's `urls.py`
## Using `render()` as the Return Function in Views
The preferred method of generating a view is the `render()` method, which is used as follows
```
def my_view():
   ...
   return render(request, `URL`, context=context_dictionary)
```
# Summary of Chapter 9
## User Accounts
foo bar
## Enabling Authentication
To allow authentication to work, the project's `settings.py` file must include the following in the `INSTALLED_APPS` array:
- `django.contrib.admin`
- `django,contrib.auth`

PyCharm should include these by default. If not, it will be necessary to follow the database migration procedure described previously in order to add the modules' tables to the database.
## Password options
In `settings.py`, there are several options that are either present by default when a Django project is created in PyCharm, or which can be added to increase the robustness of password creation and storage. 
### Password Hashing
The `PASSWORD_HASHERS` list can be used to alter the hashing algorithm from the default of PBKDF3. The first hashing algorithm found in the list will be used by Django, for it is a list of descending preference. I added `BCryptSHA256PasswordHasher` but it did not work because `bcrypt` was not yet added to the projects `requirements.txt` file. 
To add Python modules to the virtual environment and the list of project requirements in PyCharm:
1. `Ctrl+Alt+S` to bring up the settings window.
2. Expand the `Projet [project_name]` section on the left of the window
3. Select `Python Interpreter`
4. Click the `+` icon above the list of already-installed requirements.
5. Use the search function in the window that appears to find the package you need to add.
6. Check and numerate `Specify version` and `Add options` boxes if or as required.
7. Click `install` to add the module to the virtual envionment
8. Add the module, along with any required version to the `requirements.txt` project file because the process above only ensures it is tracked and maintained within the Python virtual environment.
The way to do this without PyCharm is `python -m pip install [packagename]`
### Password Validating
AUTH_PASSWORD_VALIDATORS is present (*but does not appear to work by default on user-created forms*) to provide methods for enforcing password strength and quality.
## User Accounts
Django provides a User model that can be used as the basis of all user accounts in apps. It is imported from `django.contrib.auth.models.User`. The user model contains basic attributes such as
- username
- password
- email address
- first name
- surname
as well as attributes to set privileges such as
- is_active
- is_staff
- is_superuser
## Adding Additional User Attributes
Additional user attributes can be created either by creating a new User class that inherits Django's User class **OR** by creating a new UserProfile class, each instance of which can be linked to an instance of a User object byt a one-to-one mapping. E.g inside the UserProfile class definition include `user = models.OneToOneField(User, on_delete=models.CASCADE)`.
After adding user accounts to the application, it is necessary to migrate the database again so that new tables can be added to represent the app's users.
## Adding User Creation
- Create a UserProfile model.
- Create UserForm and UserProfileForm forms.
- Create a view to handle new user creation.
- Create a template to display the UserForm and UserProfileForm
- Map an URL to the view.
### Create the New User Creation View
Logic must be added to handle `get` or `post` HTML requests. The first will display the form, the second will register a new user. 
## Create a Login Page
The process here is similar to the user creation process described above. The view must still contain logic to differentiate between HTTP `post` and `get` requests. A view, template and URL mapping must be created, but there is NO form required. (Why?)
## Restrict Access to Views with Python Decorators
A Python decorator is a kind of tag that can dynamically alter the behaviour of a function. It is placed before the function, method or class and obviates the need to edit the source code of whatever it placed in front of.
A decorator begins with an `@` symbol and Python modules have many built-in ones that can be used. The one used here is called `@login_required` and is used to automatically restrict access to particular views to only logged-in users. It is part of `django.contrib.auth.decorators` and it is simply placed on the line above the `def [viewname](...):` line.
# Summary of Chapter 10
## Cookies and Sessions
Because HTTP is a stateless protocol and there is no persistent connection to old session state, cookies can be used to store data a webserver and a client wish to maintain over a certain period of time. This may be such information as whether a user is logged-in to a site or a list of items in a shopping cart.
## Session ID
A common use for a cookie is to hold a "Session ID" which is a unique string of characters to identify a unique session between a particular client and a webserver. This means that only the Session ID need be stored on the client, and other information such as usernames, passwords etc. can be maintained on the server and no longer needs to be transmitted between the server and client with each new web request.

An alternative to using a Session ID cookie is to encode the Session ID within the URL - often as a seemingly random string after a `?` character.
## Sessions and Django
Django should already be providing a Session ID cookie for logged-in users to the Rango application as it already stands. This can be checked using Chrome's developer tools.
1. Right click on the webpage
2. Select `Developer Tools` --> `Inspect`
3. Select `Application` from the top-most menu in the Inspection Dialogue that appears
4. Select `Storage` --> `Cookies` from the left-hand menu
5. Chose the host and then the cookie to inspect. As long as a user is logged-in to Rango, a Session ID cookie should be present.
The session functionality is implemented via the `MIDDLEWARE` list in `settings.py` and the inclusion of the `django.contrib.sessions.middleware.SessionMiddleware` module. The `SessionMiddleware` module is highly adaptable but the most straightforward approach is to have keep track of session data in a Django model/database. This is done by ensuring 'django.contrib.sessions' is present in `INSTALLED_APPS`. Caching sessions may provide better performance - see the Django documentation for details of this approach.
## Interacting with Cookies
Django's `request` object provides several methods for interacting with cookies:
- `set_test_cookie`
- `test_cookie_worked`
- `delete_test_cookie`

**N.B.** Two different views are required for testing cookies because the server has to wait and see if the client's browser accepted/allowed the cookie.

**N.B.** When querying a cookie in Python/Django, all values are returned as strings. It is necessary to typecast the output to an integer (or typecast for whatever other types stored in cookies that are being retrieved).

## Session Data