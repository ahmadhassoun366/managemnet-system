from django.urls import path
from .views import list_spaces, make_reservation, list_reservations, get_time_slots, login, logout, register

urlpatterns = [
    path('spaces/', list_spaces, name='list_spaces'),
    path('spaces/<int:space_id>/reserve/', make_reservation, name='make_reservation'),
    path('reservations/', list_reservations, name='list_reservations'),
    path('spaces/<int:space_id>/time_slots/', get_time_slots, name='get_time_slots'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]
1