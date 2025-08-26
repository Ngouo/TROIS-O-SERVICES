#from django.contrib.auth.models import User

# Create your views here.
from django.contrib.auth.views import LoginView
from .forms import BootstrapLoginForm

class MonLoginView(LoginView):
    template_name = 'User_admin/login.html'
    authentication_form = BootstrapLoginForm








