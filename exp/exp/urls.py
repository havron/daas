"""exp URL Configuration

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
from daasapp import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home.index, name='index'),
    url(r'^hi/$', views.hi, name='hi'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^auth/$', views.check_auth, name='check_auth'),
    url(r'^product-details/(?P<drone_id>\d+)$', views.productdetails),
    url(r'^userprofile/(?P<user_id>\d+)$', views.userprofile),
    url(r'^listing/(?P<listing_id>\d+)$', views.listing),
    url(r'^listing/create/$', views.create_listing),
    #url(r'^shop/$', views.featured_items, name='featured_items'),
    url(r'^my-drones/$', views.my_drones),
]

