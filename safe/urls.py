from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('add_password/',add_password,name="add-password"),
    path('show_password/<int:id>',show_password,name="show-password"),
    path('delete_password/<int:id>',delete_password,name="delete-password"),
    path('update_password/<int:id>',update_password,name="update-password")
]