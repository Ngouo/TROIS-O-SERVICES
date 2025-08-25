from django import forms
from .models import Article




class ArticleForm(forms.ModelForm):
    nom_article = forms.CharField( max_length=2000, label="Nom", widget=forms.TextInput(attrs={
    'placeholder': "Nom de l'Article ",
    'class': 'form-control-lg', 
  }))
    prix_unitaire = forms.IntegerField(label="Prix",max_value=100000000, widget=forms.TextInput(attrs={
    'placeholder': 'Prix de votre Article',
    'class': 'form-control-lg', 
  }))
    
    class Meta:
        model = Article
        fields = ['nom_article', 'prix_unitaire']