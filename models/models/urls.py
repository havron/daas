"""models URL Configuration

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
from daasapp import views
from . import home, apiposts

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home.index),
    url(r'^api/v1/populate$', apiposts.populate),

    url(r'^api/v1/user/create$', views.create_user),
    url(r'^api/v1/user/all$', views.all_users),
    url(r'^api/v1/user/recent_givers$', views.recent_givers),
    url(r'^api/v1/user/(?P<user_id>\d+)/updater$', apiposts.updateUser),
    url(r'^api/v1/user/(?P<user_id>\d+)/update$', views.update_user),
    url(r'^api/v1/user/(?P<user_id>\d+)$', views.inspect_user),

    url(r'^api/v1/drone/create$', views.create_drone, name='drone'),
    url(r'^api/v1/drone/all$', views.all_drones, name='drone'),
    url(r'^api/v1/drone/recent$', views.recent_drones),
    url(r'^api/v1/drone/(?P<drone_id>\d+)/updater$', apiposts.updateDrone),
    url(r'^api/v1/drone/(?P<drone_id>\d+)/update$', views.update_drone),
    url(r'^api/v1/drone/(?P<drone_id>\d+)$', views.inspect_drone),
]

# more on how ?P<> works:
# https://www.webforefront.com/django/accessurlparamsviewmethods.html 
