from django.http import HttpResponse

def index(request):
    return HttpResponse('Rango says "Hello World!"')

def about(request):
    return HttpResponse('Rango says: Here is the about page.')
