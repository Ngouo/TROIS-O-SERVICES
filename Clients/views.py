from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .form import FormClient
from .utils import relance_email
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def liste_clients(request):
    Clients = Client.objects.all()
    return render(request, 'Clients/liste_clients.html', {"Clients": Clients})


@login_required
def ajout_clients(request):

    form = FormClient(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("liste_clients")
    return render(request, 'Clients/ajout_clients.html', {"form":form})

@login_required
def update_clients(request, my_id):
    client = get_object_or_404(Client, id=my_id)
    if request.method == 'POST':
        form = FormClient(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')  # ou autre page
    else:
        form = FormClient(instance=client) 
    if 'annuler' in request.POST:
        return redirect('ajout_clients')     #annuler la modification et rediriger vers la page d'ajout NB: necessite un bouton annuler avec name='annuler'
    return render(request, "Clients/update_clients.html", {"client":client, "form":form})

@login_required
def delete(request, my_id):
  client = get_object_or_404(Client, id=my_id)
  client.delete()
  return redirect('liste_clients')

@login_required
def relance_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    relance_email(client.email)
    return redirect('home')

