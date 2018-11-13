from django.shortcuts import render


def home(request):
    return render(request, 'blog/home.html')

def log_in(request):
    return render(request, 'blog/log_in.html')

def research(request):
    return render(request, 'blog/researcher.html')

def about_of(request):
    return render(request, 'blog/about_of.html')
