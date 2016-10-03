from django.shortcuts import render

def index(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/index.html', context)
def login(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/login.html', context)

def checkout(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/checkout.html', context)

def cart(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/cart.html', context)

def shop(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/shop.html', context)

def productdetails(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/product-details.html', context)

def blog(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/blog.html', context)

def blogsingle(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/blog-single.html', context)

def t404(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/t404.html', context)

def contactus(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/contact-us.html', context)

###
#    url(r'^checkout/$', views.checkout, name='checkout'),
#    url(r'^cart/$', views.cart, name='cart'),
#    url(r'^shop/$', views.shop, name='shop'),
#    url(r'^product-details/$', views.product-details, name='product-details'),
#    url(r'^blog/$', views.blog, name='blog'),
#    url(r'^blog-single/$', views.blog-single, name='blog-single'),
#    url(r'^404/$', views.404, name='404'),
#    url(r'^contact-us/$', views.contact-us, name='contact-us'),
# 404.html*	   cart.html*	     index.html		    sendemail.php
# blog.html*	   checkout.html*    login.html*	    shop.html*
# blog-single.html*  contact-us.html*  product-details.html*
