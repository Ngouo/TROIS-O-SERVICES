from django.urls import path
from Clients.views import liste_clients, ajout_clients, update_clients, delete,relance_client

urlpatterns = [
    path('liste_clients', liste_clients, name='liste_clients'),
    path('ajout_clients', ajout_clients, name='ajout_clients'),
    path('<int:my_id>/update_clients', update_clients, name='update_clients'),
    path('<int:my_id>/delete', delete, name='delete'),
    path('<int:client_id>/relance_client', relance_client, name='relance_client')
]