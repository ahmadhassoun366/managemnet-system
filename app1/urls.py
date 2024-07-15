# app1/urls.py
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('spaces/', list_spaces, name='list_spaces'),
    path('spaces/add/', create_update_space, name='add_space'),
    path('spaces/<int:space_id>/delete/', delete_space, name='delete_space'),
    path('spaces/<int:space_id>/edit/', create_update_space, name='edit_space'),
    path('spaces/<int:space_id>/reserve/', make_reservation, name='make_reservation'),
    path('reservations/<int:reservation_id>/service/', request_service, name='request_service'),
    # login and register
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

]
