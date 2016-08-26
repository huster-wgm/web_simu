from django.db import models

# Create your models here.

class Article(models.Model):
    def __init__(self):
        print ("hello ")
        
        
        
class Comment(models.Model):
    def __init__(self):
        print ("world ")
        