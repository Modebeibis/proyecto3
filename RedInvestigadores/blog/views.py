from django.shortcuts import render
from django.utils import timezone
from .models import Post

def log_in(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/log_in.html')

def home(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/home.html')
