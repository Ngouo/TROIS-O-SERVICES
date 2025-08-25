from django.urls import path
from Commandes.views import creer_commande, verification_commande, confirmer_commande, liste_commandes, generer_facture, retrait_commande

urlpatterns = [
    path('creer_commande', creer_commande, name='creer_commande'),
    path("verification_commande", verification_commande, name="verification_commande"),
    path('confirmer_commande', confirmer_commande, name='confirmer_commande'),
    path('liste_commandes', liste_commandes, name='liste_commandes'),
    path('generer_facture/<int:commande_id>/', generer_facture, name='generer_facture'),
    path("retrait_commande/<int:commande_id>/", retrait_commande, name='retrait_commande'),
]