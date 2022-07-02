from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from rango.bing_search import run_query
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['boldmessage'] = 'This is the Tango with Django demonstration app'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    "Rango says hey there partner! For more information about Rango please click on <a href='/rango/about/'>About</a>"
    # request.session.set_test_cookie()

    # Obtain our Response object early so we can add cookie information
    response = render(request, 'rango/index.html', context=context_dict)

    # return render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED")
    #     request.session.delete_test_cookie()
    # print(f"Request method:", request.method)
    # print(f"Requesting user:", request.user)
    visitor_cookie_handler(request)
    context_dict = {'boldmessage': 'RichardJRL'}
    context_dict['visits'] = int(request.session['visits'])
    response = render(request, 'rango/about.html', context=context_dict)
    # return render(request, 'rango/about.html', context=context_dict)
    return response


def show_category(request, category_name_slug):
    # Create a context dictionary wich we can pass
    # to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list>
        pages = Page.objects.filter(category=category).order_by('-views')
        # pages.order_by('views')

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    result_list = []
    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
            context_dict['result_list'] = result_list
            context_dict['query'] = query

    # Go render the response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)


@login_required()
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            print(cat, cat.slug)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            # return redirect('/rango/')
            return redirect(reverse('rango:index'))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
            # return redirect('/rango/')
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required()
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except category.DoesNotExist:
        category = None
    # You cannot add a page to a category that does not exist
    if Category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        # Have we been provided with a valid form
        if form.is_valid():
            if category:
                # Save the new page to the database.
                # QUESTION: Why is the commit False here; when it was True for the Category form save?
                # ANSWER: It is to stop Django from saving the data to the database until page.save is called later.
                #           It is used when two models are drawn upon in a single form.
                page = form.save(commit=False)
                # print(page, page.slug)
                page.category = category
                page.views = 0
                page.save()
                # Now that the page is saved, we could confirm this.
                # For now, just redirect the user back to the index view.
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                return redirect('/rango/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
            # Will handle the bad form, new form, or no form supplied cases.
            # Render the form with error messages (if any).
            # return redirect('/rango/')
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
    # return render(request, 'rango:restricted')
    # return redirect(reverse('rango:restricted'))


# @login_required
# def user_logout(request):
#     # Since we know the user is logged in (thanks to the decorator), we ca now just log them out.
#     logout(request)
#     # Take the user back to the homepage.
#     return redirect(reverse('rango:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is cast to an integer.
    # If the cookie doesn't exist, the n the default value of 1 is used.

    # Old client-side method
    # visits = int(request.COOKIES.get('visits', '1'))
    # New server-side method
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # Old client-side method
    # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    # New server-side method
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        # Update the last visit cookie now that we have updated the count
        # Old client-side method
        # response.set_cookie('last_visit', str(datetime.now()))
        # New server-side method
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        # Old client-side method
        # response.set_cookie('last_visit', last_visit_cookie)
        # New server-side method
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    # Old client-side method
    # response.set_cookie('visits', visits)
    # New server-side method
    request.session['visits'] = visits


# def search(request):
#     result_list = []
#     query = ''
#
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
#             # Run our Bing function to get the results list!
#             result_list = run_query(query)
#
#     return render(request, 'rango/search.html', {'query': query, 'result_list': result_list})


def goto_url(request):
    page_id = None
    if request.method == 'GET':
        page_id = request.GET['page_id'].strip()
        # This is equivalent to the method above - two ways of doing the same thing
        page_id = request.GET.get('page_id')


        # • In the view, get() the Page with an id of page_id (from the GET request).
        try:
            page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))

        page.views += 1
        page.save()

        return redirect(page.url)


