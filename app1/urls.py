# urls.py
from django.urls import path
from .views import list_spaces, make_reservation, list_reservations,profile,change_password, login, logout, register, confirm_reservation, cancel_reservation, get_time_slots, about, home,reservation_detail

urlpatterns = [
    path('spaces/', list_spaces, name='list_spaces'),
    path('spaces/<int:space_id>/reserve/', make_reservation, name='make_reservation'),
    path('spaces/<int:space_id>/time_slots/', get_time_slots, name='get_time_slots'),
    path('reservations/', list_reservations, name='list_reservations'),
    path('reservations/<int:reservation_id>/confirm/', confirm_reservation, name='confirm_reservation'),
    path('reservations/<int:reservation_id>/cancel/', cancel_reservation, name='cancel_reservation'),
    path('reservations/<int:reservation_id>/', reservation_detail, name='reservation_detail'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('profile/change_password/', change_password, name='change_password'),

]
