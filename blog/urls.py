# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 21:42:28 2016

@author: husterwgm
"""

from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    # ex:/blog/
    url(r'^$', views.index, name="index"),
    # ex: /blog/contact
    url(r'^contact$', views.contact, name="contact"),
    # ex: /blog/categories
    url(r'^categories$', views.categories, name="categories"),
    # ex: /blog/portfolios
    url(r'^portfolios$', views.portfolios, name="portfolios"),
]
