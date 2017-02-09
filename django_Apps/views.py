# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 15:27:56 2016

@author: husterwgm
"""
from django.shortcuts import render


def index(request):
    return render(request, 'django_Apps/index.html')