from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views, get_user_model

from users import forms


class SignupView(CreateView):
    
    success_url = reverse_lazy('dashboard:networks')
    form_class = forms.SignupForm
    model = get_user_model()
    template_name = 'users/signup.html'

    
#TODO: figure out redirect logic and optimize
class LoginView(auth_views.LoginView):
    
    success_url = reverse_lazy('dashboard:networks')
    
    model = get_user_model()
    form_class = forms.LoginForm
    fields = ['username', 'password']
    template_name = 'users/login.html'
    
    def get_success_url(self) -> str:
        return self.success_url
    
    
class LogoutView(auth_views.LogoutView):
    
    http_method_names = ['get']
    template_name = 'users/logout.html'