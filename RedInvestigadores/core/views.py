from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def log_in(request):
    return render(request, 'core/log_in.html')

def research(request):
    return render(request, 'core/researcher.html')

def about_of(request):
    return render(request, 'core/about_of.html')

def search_view(request):
    return render(request, 'core/search_view.html')
