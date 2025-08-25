from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .form import ArticleForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def ajout_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_articles')
    return render(request, "Articles/ajout_articles.html", {"form":form})

@login_required
def liste_articles(request):
    articles = Article.objects.order_by("nom_article")
    return render(request, "Articles/liste_articles.html", {"articles":articles})

@login_required
def update_article(request, my_id):
    article = get_object_or_404(Article, id=my_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('liste_articles')  # ou autre page
    else:
        form = ArticleForm(instance=article) 
    if 'annuler' in request.POST:
        return redirect('ajout_articles')     #annuler la modification et rediriger vers la page d'ajout NB: necessite un bouton annuler avec name='annuler'
    return render(request, "Articles/update_articles.html", {"article":article, "form":form})
