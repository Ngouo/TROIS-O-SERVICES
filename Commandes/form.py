from django import forms
from django.forms import inlineformset_factory
from .models import Commande, ArticleCommande, Client



class CommandeForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        empty_label="Choisissez votre Client",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Commande
        fields = ['client']

class ArticleCommandeForm(forms.ModelForm):
    class Meta:
        model = ArticleCommande
        fields = ['article', 'quantite']


ArticleCommandeFormSet = inlineformset_factory(     #ici on utilise formset pour pouvoir selectionner plusieurs articles et leurs quantités
    Commande, ArticleCommande,
    form=ArticleCommandeForm,
    extra=3  # nombre de formulaires affichés par défaut
)


class RetraitCommandeForm(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ['date_retrait']
        widgets = {
            'date_retrait': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }


    def clean(self):
        cleaned_data = super().clean()
        date_commande = self.instance.date_commande
        date_retrait = cleaned_data.get('date_retrait')

        if date_commande and date_retrait and date_retrait < date_commande:
            self.add_error('date_retrait', "La date de retrait doit être postérieure à la date de commande.")


