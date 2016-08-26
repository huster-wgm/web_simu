# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 21:42:28 2016

@author: husterwgm
"""

from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns=[
	# ex: /blog/
	url(r'^$',views.index,name="index"),
	# ex: /blog/1
	url(r'^post$',views.post,name="post"),
    # ex: /blog/contact
	url(r'^contact$',views.contact,name="contact"),
    # ex: /blog/about
	url(r'^about$',views.about,name="about"),
]