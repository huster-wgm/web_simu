"""simu_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail.wagtailadmin import urls as wagtail_admin_urls
from wagtail.wagtailcore import urls as wagtail_urls


urlpatterns = [
    url(r'^', include('blog.urls')),
    url(r'^portfolios/', include('portfolios.urls')),
    url(r'^admin', include(wagtail_admin_urls)),
    url(r'^posts/', include(wagtail_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

