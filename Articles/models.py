from django.db import models

# Create your models here.


class Article(models.Model):
    nom_article = models.CharField(max_length=500)
    prix_unitaire = models.IntegerField(max_length=5000)


    def __str__(self):
        return self.nom_article

