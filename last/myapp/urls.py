from django.contrib import admin
from django.urls import *
from . import views

urlpatterns = [
    path('main/', views.main_page),
    path('register/', views.register),
    path('signupchef/', views.signupchef),
    path('signupcustomer/', views.signupcustomer),
    path('login/', views.login),
    path('loginchef/', views.loginchef),
    path('logincustomer/', views.logincustomer),
    path('updatechef/', views.updatechef),
    path('updatedetail/', views.updatedetail),
    path('addmeal/', views.addmeal),
    path('addmealpage/', views.addmealpage),
    path('deletemeal/', views.deletemeal),
    path('changepage/', views.changepage),
    path('meal/<int:id>/', views.meal),
    path('order/', views.order),
    path('chefprof/', views.chefprof),
    path('vieworder/', views.vieworder),


    path('header/', views.header),
    path('menu/', views.menu),
    path('user_profile/', views.user_profile),
    path('process/', views.process),
    path('editprofile/', views.edit_profile_chef),
    path('set/', views.set),
    path('new/', views.new),
    path('test/', views.test),
    path('old/', views.old),
    path('phone/', views.phone),
    path('cart/', views.cart),
]