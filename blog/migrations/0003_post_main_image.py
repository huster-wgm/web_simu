# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0013_make_rendition_upload_callable'),
        ('blog', '0002_auto_20160906_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
