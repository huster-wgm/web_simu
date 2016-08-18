from django.conf.urls import url

from . import views

app_name = 'simulator'
urlpatterns=[
	# ex: /
	url(r'^$',views.home,name="home"),
	# ex: /tools
	url(r'^tools$',views.tools,name="tools"),
	# ex: /results
	url(r'^result$',views.result,name="result"),

]
