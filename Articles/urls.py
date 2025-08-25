from django.urls import path
from Articles.views import ajout_article, liste_articles, update_article

urlpatterns = [
    path('ajout_article', ajout_article, name='ajout_article'),
    path('liste_articles', liste_articles, name='liste_articles'),
     path('<int:my_id>/update_article', update_article, name='update_article'),
]