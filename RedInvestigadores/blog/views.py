from django.shortcuts import render


def home(request):
    return render(request, 'blog/home.html')

def log_in(request):
    return render(request, 'blog/log_in.html')
