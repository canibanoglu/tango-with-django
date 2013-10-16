from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. of likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    pages_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = pages_list

    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ',  '_')

    # Render the response and send it back!
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    return render_to_response('rango/about.html', None, context)

def category(request, category_name_url):
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = category_name_url.replace('_', ' ')

    # Buil dup the dictionary we will use as our template context dictionary.
    context_dict = {'category_name': category_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raise a DoesNotExist exception.
        # So the .get() method return one model instance or raises an exception.
        category = Category.objects.get(name = category_name)
        context_dict['category'] = category

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category = category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('rango/category.html', context_dict, context)
