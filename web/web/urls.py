"""web URL Configuration

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
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.contrib import admin
from . import home
from daasapp import views

handler404 = 'views.t404'
urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', home.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^product-details/(?P<drone_id>\d+)/$', views.productdetails, name='product-details'),
    url(r'^product-details/$', views.productdetails, name='product-details_noargs'),
    url(r'^user/(?P<user_id>\d+)/$', views.userprofile, name='userprofile'),
    url(r'^user/$', views.userprofile, name='userprofile_noargs'),
    #url(r'^blog/$', views.blog, name='blog'),
    #url(r'^blog-single/$', views.blogsingle, name='blog-single'),
    url(r'^t404/$', views.t404, name='t404'),
    url(r'^hi/$', views.hi, name='hi'),
    url(r'^lets-grade/$', views.letsgrade, name='lets-grade'),
    url(r'^contact-us/$', views.contactus, name='contact-us'),
    url(r'^listing/(?P<listing_id>\d+)/$', views.listing, name='listing-details'),
    url(r'^listing/$', views.listing, name='listing_noargs'),
    url(r'^create-listing/$', views.create_listing, name='create-listing'),
    ###url(r'^search-results/$', views.search_results, name='search-results'),
] # + staticfiles_urlpatterns()

