from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('like/', views.like),
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name='register'),
    path('profile/<int:pk>/',views.profileView,name='profile'),
    path('follow/<int:pk>/',views.follow,name='follow'),
    path('following/', views.following,name='following'),
    path('edit/',views.edit,name='edit'),
    path('comment/<int:pk>',views.commentHandle,name='comment')
    
]