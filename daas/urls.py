"""market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import home
from webapp import views

urlpatterns = [
    url(r'^$', home.index, name='index'),
    url(r'^api/v1/user/create$', views.create_user, name='user'),
    url(r'^api/v1/user/all$', views.all_user, name='user'),
    url(r'^api/v1/user/[0-9]*$', views.inspect_user),
    url(r'^api/v1/drone/create$', views.create_drone, name='drone'),
    url(r'^api/v1/drone/all$', views.all_drone, name='drone'),
    url(r'^api/v1/drone/[0-9]*$', views.inspect_drone),
    (r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
]
