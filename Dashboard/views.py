from django.shortcuts import render
from Clients.models import Client
from Commandes.models import Commande
from Articles.models import Article
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def nombre_clients(request):
    clients = Client.objects.count()
    commandes_reglee = Commande.objects.filter(date_retrait__isnull=False)
    nbre_commandes_reglee = commandes_reglee.count()
    nbre_articles = Article.objects.count()
    commandes = Commande.objects.count()
    montant_caisse = sum([cmd.montant_total for cmd in commandes_reglee])
    historique = Commande.objects.select_related("client").prefetch_related("articles_commande__article").order_by('-date_commande')


    context = {
        "clients":clients, 
        "nbre_commandes_reglee":nbre_commandes_reglee,
        "nbre_articles": nbre_articles,
        "commandes":commandes,
        "montant_caisse": montant_caisse,
        'historique': historique,
    }

    return render(request, 'Dashboard/dashboard.html', context)





