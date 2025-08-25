from django.urls import path
from Dashboard.views import *


urlpatterns = [
    path('home', nombre_clients, name='home'),
]