from django.urls import path
from django.contrib.auth.views  import LoginView, LogoutView
from User_admin.views import MonLoginView


urlpatterns = [
    #path('login', connexion, name="login"),
    #path('logout', deconnexion, name='logout'),
    path('', MonLoginView.as_view(), name=''),
    path('logout/', LogoutView.as_view(), name='logout'),
]