import os
from .utils import envoyer_email
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from .form import *
from Articles.models import Article
from weasyprint import HTML # type: ignore

# Create your views here.


def creer_commande(request):
   # montant_commande = Commande.objects.get(id=1)
    #total = montant_commande.montant_total()
    if request.method == "POST":
        commande_form = CommandeForm(request.POST)
        formset = ArticleCommandeFormSet(request.POST)

        if commande_form.is_valid() and formset.is_valid():
            client_obj = commande_form.cleaned_data['client']
            request.session['commande_data'] = {
                'client_id': client_obj.id
            }
            #print(client_obj)
            # Stocker les articles commandés
            articles_data = []
            for form in formset:
                    if form.cleaned_data:
                        article = form.cleaned_data['article']
                        quantite = form.cleaned_data['quantite']
                        articles_data.append({
                            'article_id': article.id,
                            'article_nom': article.nom_article,
                            'quantite': quantite
                        })
            request.session['articles_data'] = articles_data

            return redirect("verification_commande")

        else:
            print("Commande erreurs :", commande_form.errors)
            print("Formset erreurs :", formset.errors)

    else:
        commande_form = CommandeForm()
        formset = ArticleCommandeFormSet()

    return render(request, 'Commandes/creer_commande.html', {
        'commande_form': commande_form,
        'formset': formset
    })



def verification_commande(request):
    commande_data = request.session.get('commande_data')  # {'client_id': ...}
    articles_data = request.session.get('articles_data')  # liste d’articles

    print(commande_data)
    print(articles_data)

        # 2. Sécurité : redirection si données manquantes
    if not commande_data or not articles_data:
        return redirect('creer_commande')

    # Récupération du client
    try:
        client = Client.objects.get(id=commande_data['client_id'])
    except Client.DoesNotExist:
        return redirect('creer_commande')

    # Construction des lignes articles avec prix
    articles = []
    total = 0
    for item in articles_data:
        try:
            article_obj = Article.objects.get(id=item['article_id'])
            quantite = item['quantite']
            sous_total = article_obj.prix_unitaire * quantite
            total += sous_total

            articles.append({
                'nom_article': article_obj.nom_article,
                'quantite': quantite,
                'prix_unitaire': article_obj.prix_unitaire,
                'sous_total': sous_total
            })
        except Article.DoesNotExist:
            continue  # ou gérer autrement

    context = {
        'client': client,
        'articles': articles,
        'total': total
    }

    return render(request, 'Commandes/verification_commande.html',context )



def confirmer_commande(request):
    # 1. Récupération des données en session
    commande_data = request.session.get('commande_data')
    articles_data = request.session.get('articles_data')

    # 2. Sécurité : redirection si données manquantes
    if not commande_data or not articles_data:
        return redirect('creer_commande')

    # 3. Création de la commande
    try:
        client = Client.objects.get(id=commande_data['client_id'])
    except Client.DoesNotExist:
        return redirect('creer_commande')

    commande = Commande.objects.create(client=client)

    # 4. Enregistrement des articles liés
    for item in articles_data:
        try:
            article_obj = Article.objects.get(id=item['article_id'])
            quantite = item['quantite']
            ArticleCommande.objects.create(
                commande=commande,
                article=article_obj,
                quantite=quantite
            )
        except Article.DoesNotExist:
            continue  # Ignore ou log si besoin    

    # 5. Nettoyage de la session
    request.session.pop('commande_data', None)
    request.session.pop('articles_data', None)

    # 6. Affichage de la confirmation
    return render(request, 'Commandes/confirmation_commande.html', {
        'commande': commande
    })


def liste_commandes(request):
    liste_commandes = Commande.objects.all().order_by('-date_commande')

    query = request.GET.get("query", "").strip()

    liste_commandes = Commande.objects.all().order_by('-date_commande')

    if query:
        liste_commandes = liste_commandes.filter(client__nom_client__icontains=query)


    tableau = []

    for commande in liste_commandes:
        ligne = {
            'matricule': commande.matricule_commande,
            'client': commande.client.nom_client,
            'date': commande.date_commande,
            'articles': [],
            'total': commande.montant_total,
            'id': commande.id,
            'statut': commande.statut,
            'date_retrait': commande.date_retrait,
        }
         
        for item in commande.articles_commande.all():
                ligne['articles'].append({
                'nom': item.article.nom_article,
                'prix': item.article.prix_unitaire,
                'quantite': item.quantite,
                'sous_total': item.article.prix_unitaire * item.quantite
            })

        tableau.append(ligne)  


    return render(request, 'Commandes/liste_commandes.html', {
        'commandes': tableau
    })


def generer_facture(request,commande_id):
    commande = Commande.objects.get(id=commande_id)
    articles = commande.articles_commande.all()

    total = sum(item.sous_total for item in commande.articles_commande.all())

    context = {
        'commande': commande,
        'articles': articles,
        'total': total,
    }

    template = get_template('facture_pdf.html')
    html_string = template.render(context)

    CHEMIN_FACTURE = r"C:\Users\MEN ELECTRONICS\OneDrive\Documents\Factures"
    if not os.path.exists(CHEMIN_FACTURE):
        os.makedirs(CHEMIN_FACTURE)

    filename = f'facture_{commande.matricule_commande} - {commande.client.nom_client}.pdf'
    filepath = os.path.join(CHEMIN_FACTURE, filename)

    HTML(string=html_string).write_pdf(filepath)

    # Envoie l'email
    envoyer_email(commande, commande.client.email, filepath)

    # Générer le PDF et l'envoyer dans le dossier indiqué dans le chemin d'accès
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)


def retrait_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    print(commande)
    if request.method == 'POST':
        form = RetraitCommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('liste_commandes')
        else:
            print(form.errors)
    else:
        form = RetraitCommandeForm(instance=commande)
    
    if 'annuler' in request.POST:
        return redirect('liste_commandes')     #annuler la modification et rediriger vers la page d'ajout NB: necessite un bouton annuler avec name='annuler'
    return render(request, 'Commandes/retrait_commande.html', {"form":form, "commande":commande})