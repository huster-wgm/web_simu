from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Post


def index(request):
    latest_posts = Post.objects.order_by('-date')[:5]
    context = {'latest_posts': latest_posts}
    return render(request, 'blog/index.html',context)
    
def about(request):    
    
    return render(request, 'blog/about.html')
    
def contact(request):
    return render(request, 'blog/contact.html')



