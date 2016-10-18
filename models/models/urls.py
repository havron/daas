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
import daasapp
from daasapp import views
from . import home, apiposts
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home.index),
    url(r'^api/v1/populate$', apiposts.populate),

    url(r'^api/v1/user/create/$', views.create_user, name = 'create_user'), 
    url(r'^api/v1/user/login/$', views.login_user, name = 'login_user'), 
    url(r'^api/v1/user/logout/$', views.logout_user, name = 'logout_user'), 
    url(r'^api/v1/user/auth/$', views.check_auth_user, name = 'check_auth_user'), 
    url(r'^api/v1/user/all/$', views.all_users, name = 'view_user'),
    url(r'^api/v1/user/recent_givers/$', views.recent_givers, name = 'recent_givers'),
    url(r'^api/v1/user/(?P<user_id>\d+)/updater/$', apiposts.updateUser),
    url(r'^api/v1/user/(?P<user_id>\d+)/update/$', views.update_user, name = 'update_user'),
    url(r'^api/v1/user/(?P<user_id>\d+)?/$', views.inspect_user, name = 'inspect_user'),

    url(r'^api/v1/drone/create/$', views.create_drone, name='create_drone'),
    url(r'^api/v1/drone/all/$', views.all_drones, name='view_drone'),
    url(r'^api/v1/drone/recent/$', views.recent_drones, name = 'recent_drones'),
    url(r'^api/v1/drone/(?P<drone_id>\d+)/updater/$', apiposts.updateDrone),
    url(r'^api/v1/drone/(?P<drone_id>\d+)/update/$', views.update_drone, name = 'update_drone'),
    url(r'^api/v1/drone/(?P<drone_id>\d+)/$', views.inspect_drone, name = 'inspect_drone'),

    url(r'^api/v1/listing/create/$', views.create_listing, name='create_listing'),
    url(r'^api/v1/listing/all/$', views.all_listing, name='view_listing'),
    # url(r'^api/v1/drone/recent/$', views.recent_drones, name = 'recent_drones'),
    #url(r'^api/v1/drone/(?P<drone_id>\d+)/updater/$', apiposts.updateDrone),
    #url(r'^api/v1/drone/(?P<drone_id>\d+)/update/$', views.update_drone, name = 'update_drone'),
    #url(r'^api/v1/drone/(?P<drone_id>\d+)/$', views.inspect_drone, name = 'inspect_drone'),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#from django.contrib.staticfiles import views
#urlpatterns += [
#  url(r'^/daasapp/static/(?P<path>.*)$', views.serve),
#]

# more on how ?P<> works:
# https://www.webforefront.com/django/accessurlparamsviewmethods.html 
