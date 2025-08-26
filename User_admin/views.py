#from django.contrib.auth.models import User

# Create your views here.
from django.contrib.auth.views import LoginView
from .forms import BootstrapLoginForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class MonLoginView(LoginView):
    template_name = 'User_admin/login.html'
    authentication_form = BootstrapLoginForm








