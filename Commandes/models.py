import random
from django.db import models
from Clients.models import Client
from Articles.models import Article

# Create your models here.


def generate_matricule():
    return f"Com-{random.randint(10000, 99999)}"


class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, related_name='commandes')
    matricule_commande = models.CharField(max_length=50, unique=True, default=generate_matricule)
    date_commande = models.DateField(auto_now_add=True)
    date_retrait = models.DateField(null=True, blank=True)

    @property
    def statut(self):
        return "Payée" if self.date_retrait else "Impayé" 

    def save(self, *args, **kwargs):
        if not self.matricule_commande:
            self.matricule_commande = f"CMD{self.date_commande.year}-{self.pk or ''}"
        super().save(*args, **kwargs)
                                                                #bloc permettant d'afficher le matricule dans la BD
    def __str__(self):
        return self.matricule_commande


    @property
    def montant_total(self):
        total = sum(
            item.article.prix_unitaire * item.quantite
            for item in self.articles_commande.all()
        )
        return total



class ArticleCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='articles_commande')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.commande.matricule} - {self.article.nom} x{self.quantite}"
    
    @property
    def sous_total(self):
        return self.article.prix_unitaire * self.quantite

