from django import forms
from .models import Client
from phonenumber_field.formfields import PhoneNumberField



class FormClient(forms.ModelForm):
    nom_client = forms.CharField(max_length=2000,label="Nom et Prenom", widget=forms.TextInput(attrs={
    'placeholder': 'Nom et Prenom du Client',
    'class': 'form-control', 
  }))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={
    'placeholder': 'Email du Client',
    'class': 'form-control-lg', 
  }))
    num_telephone = PhoneNumberField(region='CM')


    class Meta:
        model = Client
        fields = ("nom_client", "email", "num_telephone")
    