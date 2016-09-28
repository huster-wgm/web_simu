from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    posts = Post.objects.live().order_by('-first_published_at')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.paginator(paginator.num_pages)
    context = {'post_list': post_list}
    return render(request, 'blog/index.html',context)
    
def categories(request):    
    
    return render(request, 'blog/categories.html')
    
def portfolio(request):
    return render(request, 'blog/portfolio.html')
    
def contact(request):
    return render(request, 'blog/contact.html')
