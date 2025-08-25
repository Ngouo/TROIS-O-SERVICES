from django.db import models 
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.



class Client(models.Model):
    nom_client = models.CharField(max_length=500)
    email = models.EmailField(default="client@Emailfield")
    num_telephone = PhoneNumberField(blank=True)
    date_ajout = models.DateField(auto_now_add=True)


    class Meta:
        ordering = ('-date_ajout', )

    def __str__(self):
        return self.nom_client
