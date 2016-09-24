from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Post


def index(request):
    latest_posts = Post.objects.live().order_by('-first_published_at')[:5]
    context = {'latest_posts': latest_posts}
    return render(request, 'blog/index.html',context)
    
def categories(request):    
    
    return render(request, 'blog/categories.html')
    
def portfolio(request):
    return render(request, 'blog/portfolio.html')
    
def contact(request):
    return render(request, 'blog/contact.html')
