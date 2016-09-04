from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import BlogPage


def index(request):
    
    return render(request, 'blog/index.html')
def about(request):    
    
    return render(request, 'blog/about.html')
    
def post(request):

    return render(request, 'blog/post.html')

def contact(request):
    return render(request, 'blog/contact.html')



