from django.urls  import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('home', views.home),
    path('login', views.login),
    path('logout', views.logout),
    path('new/<int:userId>', views.new, name='new'),
    path('home/create', views.create, name='create'),
    path('Add_Wish', views.Add_Wish, name='Add_Wish'),
    path('Remove_Wish/<int:itemId>', views.Remove_Wish),
    path('Delete_Wish/<int:itemId>', views.Delete_Wish),
    path('home/<int:itemId>/show', views.show),
]
